#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
import gtk
import gobject
import time
import signal
import subprocess
import traceback
import random
import socket
import thread
import threading
import BaseHTTPServer
import SimpleHTTPServer
import SocketServer
import share
import archive
import timer
import log
import convert
import drawingarea
import lock

def encrypt_path(path):
	ext = os.path.splitext(convert.get_unicode(path))[1] or ".none"
	return path.encode("hex")+convert.get_str(ext)

def decrypt_path(enc_path):
	return os.path.splitext(enc_path)[0].decode("hex")

class HTTPHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		if self.path.startswith("/req="):
			path = decrypt_path(self.path[5:])
		else:
			self.send_error(404)
			return
		data = archive.read(path, share.KEY)
		if data:
			self.send_response(200)
			self.send_header("Content-type", "audio/basic")
			self.send_header("Content-Length", str(len(data)))
			self.end_headers()
			try:
				self.wfile.write(data)
			except:
				pass
		else:
			self.send_error(404)
	
	def translate_path(self, path):
		return path
	
	def log_message(self, format, *args):
		return

class HTTPServer(BaseHTTPServer.HTTPServer):
	def process_request_thread(self, request, client_address):
		try:
			self.finish_request(request, client_address)
			self.close_request(request)
		except:
			self.handle_error(request, client_address)
			self.close_request(request)
	
	def process_request(self, request, client_address):
		timer.timeout_add(
			0,
			self.process_request_thread,
			request,
			client_address,
		)

def http_server(server):
	try:
		server.handle_request()
	except:
		log.err(traceback.format_exc())
	return True

def start_http_server():
	log.msg("Start player server on (127.0.0.1:%d)"%share.PORT)
	server = HTTPServer(("127.0.0.1", share.PORT), HTTPHandler)
	server.timeout = 0
	timer.timeout_add(share.HTTP_HANDLE_INTERVAL, http_server, server)

class ThreadingHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
	pass

def StartThreadingHttpServer():
	if share.PLAYER_THREAD:
		return
	log.msg("Start threading player server on (127.0.0.1:%d)"%share.PORT)
	server = ThreadingHTTPServer(("127.0.0.1", share.PORT), HTTPHandler)
	share.PLAYER_THREAD = threading.Thread(target=server.serve_forever, args=())
	share.PLAYER_THREAD.setDaemon(True)
	share.PLAYER_THREAD.start()

class Mplayer:
	#mplayer -input cmdlist
	BaseArg = (
		"-slave",
		"-really-quiet",
		"-msglevel",
		"global=5", 
		"-input",
		"nodefault-bindings",
		"-noconfig",
		"all",
	)
	
	def __init__(self, args=()):
		self.args = Mplayer.BaseArg+args
		if os.name == "posix":
			self.exec_path = share.MPLAYER_POSIX_PATH
		elif os.name == "nt":
			self.exec_path = share.MPLAYER_NT_PATH
		self.proc = None
		self.volume = 1.0
		self.loop_count = 1
		self.run_end_timeout = []
	
	def get_volume(self):
		return self.volume
	
	def set_volume(self, volume):
		self.volume = max(min(volume, 1), 0)
	
	def alive(self):
		return (self.proc and (self.proc.poll() == None))
	
	def kill(self):
		if not self.proc:
			return
		self.proc.kill()
		os.kill(self.proc.pid, signal.SIGQUIT)
		os.kill(self.proc.pid, signal.SIGKILL)
		self.proc = None
	
	def close(self):
		if not self.alive():
			return
		self.proc.stdin.write("quit\n")
		self.proc.wait() #safely end when output std** with subprocess.PIPE
		self.proc = None
		#timer.timeout_add(1000, self.kill)
	
	def spawn(self, path):
		self.close()
		cmd = (self.exec_path,)+self.args+(
			"-loop",
			str(int(self.loop_count)),
			"-volume",
			str(int(self.volume*100)),
			path,
		)
		log.msg("spawn", cmd)
		self.proc = subprocess.Popen(
			cmd,
			stdin=subprocess.PIPE,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			close_fds=(not subprocess.mswindows),
		)
	
	def run_end_timer(self, run_end, args):
		if self.alive():
			return True
		run_end(*args)
	
	def run_end(self, run_end, args=()):
		timer.timeout_list_clear(self.run_end_timeout)
		timer.timeout_list_append(
			self.run_end_timeout,
			share.PLAYER_RUN_END_DELAY,
			self.run_end_timer,
			run_end,
			args,
		)
	
	def wait(self):
		while self.alive():
			time.sleep(share.GLOBAL_WAIT_DELAY)

class StandardPlayer(Mplayer):
	def __init__(self, args=()):
		Mplayer.__init__(self, args)
	
	def playing(self):
		return self.alive()
	
	def play(self, path, loop=False):
		self.stop()
		self.loop_count = 0 if loop else 1
		if convert.get_unicode(path).find(">") != -1:
			if share.KEY:
				self.spawn(
					"http://127.0.0.1:%d/req=%s"%(share.PORT, encrypt_path(path))
				)
			else:
				self.spawn(
					convert.get_str(convert.get_unicode(path).replace(">", "/"))
				)
		elif os.path.isfile(path):
			self.spawn(path)
		else:
			raise IOError("%s not exist"%path)
	
	def stop(self):
		self.close()

class Player(StandardPlayer):
	def __init__(self):
		StandardPlayer.__init__(self)

class MoviePlayer(StandardPlayer, drawingarea.DrawingArea):
	def __init__(self, width, height, color="#000"):
		drawingarea.DrawingArea.__init__(self, width, height, color)
		StandardPlayer.__init__(self, ("-fixed-vo", "-fs", "-wid", 0))
		self.connect("destroy", self.on_destroy)
		#colormap must be rgb_colormap
		self.set_colormap(gtk.gdk.Screen().get_rgb_colormap())
	
	def get_id(self):
		with share.GTK_LOCK:
			if self.window:
				if os.name == "nt":
					return self.window.handle
				else:
					return self.window.xid
			else:
				return 0
	
	def play(self, path, *args, **argv):
		self.args = self.args[:-1]+(convert.get_str(self.get_id()),)
		StandardPlayer.play(self, path, *args, **argv)
	
	def on_destroy(self, *args):
		self.stop()
