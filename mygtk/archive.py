#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
import hashlib
import zipfile
import threading
import traceback
import share
import convert
import log
import rijndael
import struct

class IOData:
	def __init__(self, path, data):
		self.path = path
		self.data = data

class Key(rijndael.rijndael):
	def __init__(self, s):
		self.lock = threading.RLock()
		rijndael.rijndael.__init__(
			self,
			hashlib.sha256(hashlib.sha512(s).digest()).digest(),
			block_size=32,
		)

def posix_path(path):
	return convert.get_str(convert.get_unicode(path).replace("\\", "/"))

def pack_long_int(i):
	return struct.pack(">Q", i)

def unpack_long_int(s):
	return struct.unpack(">Q", s)[0]

def rijndael_encode(string, rijndael_obj):
	if not string:
		raise ValueError("not string")
	string_size = len(string)
	string += "\x00"*(32-len(string)%32)
	code = ""
	with rijndael_obj.lock:
		for i in xrange(len(string)/32):
			code += rijndael_obj.encrypt(string[i*32:i*32+32])
	code_size = len(code)
	return pack_long_int(string_size)+code

def rijndael_decode(code, rijndael_obj):
	if not code:
		raise ValueError("not code")
	string_size = unpack_long_int(code[:8])
	if (len(code)-8) % 32:
		raise ValueError("(len(code)-4) % 32 != 0")
	string = ""
	with rijndael_obj.lock:
		for i in xrange(len(code)/32):
			string += rijndael_obj.decrypt(code[i*32+8:i*32+40])
	return string[:string_size]

def encode(s, r):
	if share.USE_ZLIB:
		s = s.encode("zlib")
	return rijndael_encode(s[:share.ENCODE_BYTES], r)+s[share.ENCODE_BYTES:]

def decode(c, r):
	cl = share.ENCODE_BYTES+(32-share.ENCODE_BYTES%32)+8
	s = rijndael_decode(c[:cl], r)+c[cl:]
	if share.USE_ZLIB:
		s = s.decode("zlib")
	return s

def pack(path_src, path_zip, key):
	zip_obj = zipfile.ZipFile(path_zip, "w", zipfile.ZIP_STORED)
	for root, dirs, files in os.walk(path_src):
		for dir_name in dirs:
			zip_obj.write(
				os.path.join(root, dir_name),
				os.path.join(root, dir_name)[len(path_src)+1:],
			)
		for file_name in files:
			string = open(os.path.join(root, file_name), "rb").read()
			if key:
				code = encode(string, key)
			else:
				code = string
			zip_obj.writestr(
				os.path.join(root, file_name)[len(path_src)+1:],
				code,
			)
	zip_obj.close()

def exist(arc_path, zip_path, key):
	if os.path.isdir(arc_path):
		return os.path.exists(os.path.join(arc_path, zip_path))
	elif os.path.isfile(arc_path):
		zip_obj = zipfile.ZipFile(arc_path, "r")
		ret = True
		try:
			p = zip_obj.open(arc_path)
		except:
			print traceback.format_exc()
			ret = False
		zip_obj.close()
		return ret
	else:
		return False

def read_from_archive(arc_path, zip_path, key):
	zip_obj = zipfile.ZipFile(arc_path, "r")
	try:
		code = zip_obj.read(zip_path)
		string = decode(code, key)
	except KeyError, e:
		raise IOError("read [%s -> %s] error: %s"%(
			arc_path,
			zip_path,
			e,
		))
	finally:
		zip_obj.close()
	return string

def read_from_path(path, key):
	path_split = map(convert.get_str, convert.get_unicode(path).split(">"))
	if len(path_split) > 1:
		arc_path = path_split[0]
		zip_path = path_split[1]
		if exist(share.PATCH_ARCHIVE, zip_path, key):
			arc_path = PATCH_ARCHIVE
		if os.path.isdir(arc_path):
			data = open(os.path.join(arc_path, zip_path), "rb").read()
		elif os.path.isfile(arc_path):
			data = read_from_archive(arc_path, zip_path, key)
		else:
			raise IOError("archive %s not exist"%arc_path)
	else:
		data = open(path, "rb").read()
	return data

def read_from_buffer(path, key, without_buffer=False):
	if without_buffer or not share.USE_DATA_BUFFER:
		return read_from_path(path, key)
	for i, iodata in enumerate(share.IODATA_BUFFER):
		if iodata.path == path:
			share.IODATA_BUFFER.pop(i)
			share.IODATA_BUFFER.append(iodata)
			return iodata.data
	else:
		iodata = IOData(path, read_from_path(path, key))
		share.IODATA_BUFFER.append(iodata)
	for i in xrange(len(share.IODATA_BUFFER)-share.MAX_IODATA_BUFFER):
		share.IODATA_BUFFER.pop(0)
	#log.msg(IODATA_BUFFER)
	return iodata.data

def read(path, key):
	#log.msg("read", path)
	with share.ARCHIVE_READ_LOCK:
		return read_from_buffer(
			posix_path(path),
			key,
			path.startswith("__"),
		)