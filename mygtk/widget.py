#!/usr/bin/env python
# -*- coding:utf-8 -*-
import gtk
import share
import log
import pango
import traceback
import time
import timer

class Widget(gtk.Widget):
	def __init__(self):
		self.x = 0
		self.y = 0
		self.real_x = 0
		self.real_y = 0
		self.w = 0
		self.h = 0
		self.real_w = 0
		self.real_h = 0
		self.event_list = {}
		self.use_event = True
		self.layer = None
		self.layer_name = ""
		self.window_obj = None
		self.move_id_list = []
		self.run_id_list = []
		self.running = 0
		self.set_events(share.EVENT_MASK)
	
	def show(self):
		gtk.Widget.show(self)
	
	def hide(self):
		gtk.Widget.hide(self)
	
	def get_visible(self):
		return gtk.Widget.get_property(self, "visible")
	
	def set_visible(self, value):
		gtk.Widget.get_property(self, "visible", bool(value))
	
	def set_bg(self, color):
		gtk.Widget.modify_bg(self, 0, gtk.gdk.color_parse(color))
	
	def set_base(self, color):
		gtk.Widget.modify_base(self, 0, gtk.gdk.color_parse(color))
	
	def set_fg(self, color):
		gtk.Widget.modify_fg(self, 0, gtk.gdk.color_parse(color))
	
	def set_font(self, name, size):
		size = int(size*(share.WIDTH_ZOOM_SCALE+share.HEIGHT_ZOOM_SCALE)*0.5)
		gtk.Widget.modify_font(self, pango.FontDescription("%s %s"%(name, size)))
	
	def set_font_color(self, color):
		gtk.Widget.modify_text(self, 0, gtk.gdk.color_parse(color))
	
	def set_coord(self, x, y):
		try:
			self.x = int(x)
			self.y = int(y)
			self.real_x = int(x*share.WIDTH_ZOOM_SCALE)
			self.real_y = int(y*share.HEIGHT_ZOOM_SCALE)
		except:
			log.err(repr(self), x, y, traceback.format_exc())
	
	def get_coord(self):
		return self.x, self.y
	
	def get_real_coord(self):
		return self.real_x, self.real_y
	
	def set_size(self, w, h):
		self.w = int(w)
		self.h = int(h)
		self.real_w = int(w*share.WIDTH_ZOOM_SCALE)
		self.real_h = int(h*share.HEIGHT_ZOOM_SCALE)
		self.set_size_request(self.real_w, self.real_h)
	
	def set_real_size(self, real_w, real_h):
		self.w = int(float(real_w)/share.WIDTH_ZOOM_SCALE)
		self.h = int(float(real_h)/share.HEIGHT_ZOOM_SCALE)
		self.real_w = int(real_w)
		self.real_h = int(real_h)
		self.set_size_request(self.real_w, self.real_h)
	
	def get_size(self):
		#in gtk, get_width and get_height be used
		return self.w, self.h
	
	def get_real_size(self):
		return self.real_w, self.real_h
	
	def _event(self, *args):
		if not self.get_event_enable():
			return
		function, run_after, pass_arg_count = args[-3:]
		ret = None
		try:
			ret = function(*args[pass_arg_count:-3])
		except:
			log.err(repr(self), args, traceback.format_exc())
		if run_after:
			try:
				run_after[0](*run_after[1:])
			except:
				log.err(repr(self), args, traceback.format_exc())
		if ret:
			if ret == share.EVENT_RETURN_NONE:
				return None
			elif ret == share.EVENT_RETURN_FALSE:
				return False
			elif ret == share.EVENT_RETURN_TRUE:
				return True
		#break event
		return True
	
	def _bind_event(self, event_name, gtk_event_name, *args):
		if gtk_event_name in self.event_list:
			self.disconnect(self.event_list[gtk_event_name])
			self.event_list.pop(gtk_event_name)
		if args[-3]: #if function
			self.event_list[gtk_event_name] = self.connect(
				gtk_event_name,
				self._event,
				*args
			)
	
	def bind_event(self, event_name, function, *args):
		event_info = share.EVENT_LIST.get(event_name)
		if event_info:
			gtk_event_name = event_info[0]
			pass_arg_count = event_info[1]
			if len(event_info) > 2:
				run_after = event_info[2:]
			else:
				run_after = None
			args = args + (function, run_after, pass_arg_count)
			self._bind_event(event_name, gtk_event_name, *args)
		else:
			log.err(repr(self), "event %s not exist"%event_name)
	
	def enable_event(self):
		self.use_event = True
	
	def disable_event(self):
		self.use_event = False
	
	def get_event_enable(self):
		if not self.use_event:
			return False
		if isinstance(self, window.Window):
			return self.use_event
		l = self.layer
		while l:
			if not l.use_event:
				return False
			else:
				l = l.master
		return True
	
	def stop(self):
		timer.timeout_list_clear(self.move_id_list)
		timer.timeout_list_clear(self.run_id_list)
		self.running = 0
	
	def push_running(self):
		self.running += 1
	
	def pop_running(self):
		self.running -= 1
		if self.running < 0:
			log.err(self, "running =", running)
			self.running = 0
	
	def get_running(self):
		return self.running
	
	def wait(self):
		while self.get_running():
			time.sleep(share.GLOBAL_WAIT_DELAY)

import window
