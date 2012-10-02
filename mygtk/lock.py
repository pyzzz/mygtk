#!/usr/bin/env python
# -*- coding:utf-8 -*-
import gtk
import os
import log
import share
import threading

def remove_file(path):
	try:
		os.remove(path)
	except:
		log.err("lock.remove_file", path, traceback.format_exc())

def create_file(path, content=""):
	try:
		p = open(path, "wb")
		p.write(content)
		p.close()
	except:
		log.err("lock.create_file", path, traceback.format_exc())

def check_lock():
	if not os.path.exists(share.LOCK_PATH):
		create_file(share.LOCK_PATH)
	if share.MAIN_WINDOW and os.path.exists(share.RESTORE_PATH):
		remove_file(share.RESTORE_PATH)
		try:
			share.MAIN_WINDOW.present()
		except:
			log.err("lock.check_lock", traceback.format_exc())
	return True

class GtkLock(threading._RLock):
	def __enter__(self):
		threading._RLock.__enter__(self)
		if self._RLock__count == 1:
			gtk.gdk.threads_enter()
	def __exit__(self, *args):
		threading._RLock.__exit__(self, *args)
		if self._RLock__count == 0:
			gtk.gdk.threads_leave()
share.GTK_LOCK = GtkLock() #not work for windows
