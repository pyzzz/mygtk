#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
import gtk
import traceback
import widget
import layer
import share
import log
import event
import image
import button
import effect
import timer

class Window(gtk.Window, widget.Widget):
	def __init__(self, title="", width=None, height=None, main_window=True):
		#set share
		if share.USE_FULLSCREEN:
			share.REAL_WIDTH = share.SCREEN_WIDTH
			share.REAL_HEIGHT = int(
				share.SCREEN_WIDTH*(
				share.STD_HEIGHT*1.0/share.STD_WIDTH))
		else:
			if width: share.REAL_WIDTH = width
			if height: share.REAL_HEIGHT = height
		share.WIDTH_ZOOM_SCALE = share.REAL_WIDTH*1.0/share.STD_WIDTH
		share.HEIGHT_ZOOM_SCALE = share.REAL_HEIGHT*1.0/share.STD_HEIGHT
		share.WINDOW_TITLE = title
		#set window
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		widget.Widget.__init__(self)
		self.set_resizable(False)
		self.set_app_paintable(True)
		if share.USE_FULLSCREEN:
			self.modify_bg(0, gtk.gdk.color_parse("#333"))
			self.set_decorated(False)
			self.set_size_request(share.SCREEN_WIDTH, share.SCREEN_HEIGHT)
		else:
			self.set_size_request(share.REAL_WIDTH, share.REAL_HEIGHT)
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_title(title)
		#self.set_events(share.EVENT_MASK)
		#enable rgba support
		#gtk.gdk.Screen().get_rgb_colormap()
		#gtk.gdk.Screen().get_rgba_colormap()
		self.color_map = self.get_screen().get_rgba_colormap() #rgba support
		if self.color_map:
			gtk.widget_set_default_colormap(self.color_map)
			self.set_colormap(self.color_map)
		#set layer
		self.layer_list = {}
		if share.USE_FULLSCREEN:
			self.layer_list["__BASE__"] = layer.Layer("__BASE__")
			self.layer_list["__SCREEN__"] = layer.Layer("__SCREEN__")
			self.layer_list["__SCREEN__"].put(
				self.layer_list["__BASE__"],
				0,
				(share.SCREEN_HEIGHT-share.REAL_HEIGHT)/2,
			)
			self.add(self.layer_list["__SCREEN__"])
		else:
			self.layer_list["__BASE__"] = layer.Layer("__BASE__")
			self.add(self.layer_list["__BASE__"])
		#set event
		self.bind_event("exit", event.exit)
		self.bind_event("destroy", lambda *args: True)
		self.show_all()
		#set main window
		if main_window:
			share.MAIN_WINDOW = self
			share.set_gtk_font(share.GLOBAL_GTK_FONT_NAME, share.GLOBAL_GTK_FONT_SIZE)
			self.hide()
	
	def layer_add(self, layer_name, x=0, y=0, show=True, master_name="__BASE__"):
		try:
			if layer_name in self.layer_list:
				raise Exception("layer_name exist")
			l = layer.Layer(layer_name)
			l.set_coord(x, y)
			l.master = self.layer_list[master_name]
			l.master_name = master_name
			show and l.show()
			l.master.put(l, l.real_x, l.real_y)
			self.layer_list[layer_name] = l
		except:
			log.err(repr(self), layer_name, traceback.format_exc())
	
	def layer_del(self, layer_name):
		try:
			l = self.layer_list[layer_name]
			l.master.remove(l)
			l.master = None
			l.master_name = ""
			self.layer_list.pop(layer_name)
		except:
			log.err(repr(self), layer_name, traceback.format_exc())
	
	def layer_show(self, layer_name):
		try:
			self.layer_list[layer_name].show()
		except:
			log.err(repr(self), layer_name, traceback.format_exc())
	
	def layer_hide(self, layer_name):
		try:
			self.layer_list[layer_name].hide()
		except:
			log.err(repr(self), layer_name, traceback.format_exc())
	
	def layer_move(self, layer_name, x, y):
		try:
			l = self.layer_list[layer_name]
			l.set_coord(x, y)
			l.master.move(l, l.real_x, l.real_y)
		except:
			log.err(repr(self), layer_name, traceback.format_exc())
	
	def layer_active(self, layer_name):
		try:
			l = self.layer_list[layer_name]
			l.master.remove(l)
			l.master.put(l, l.real_x, l.real_y)
		except:
			log.err(repr(self), layer_name, traceback.format_exc())
	
	def get_layer(self, layer_name):
		try:
			return self.layer_list[layer_name]
		except:
			log.err(repr(self), layer_name, traceback.format_exc())
	
	def get_layer_visible(self, layer_name):
		try:
			return self.layer_list[layer_name].get_visible()
		except:
			log.err(repr(self), layer_name, traceback.format_exc())
	
	def layer_clear(self, layer_name):
		try:
			widget_list = self.layer_list[layer_name].get_children()
			while widget_list:
				self.widget_del(widget_list.pop())
		except:
			log.err(repr(self), layer_name, traceback.format_exc())
	
	def layer_enable_event(self, layer_name):
		try:
			self.layer_list[layer_name].enable_event()
		except:
			log.err(repr(self), layer_name, traceback.format_exc())
	
	def layer_disable_event(self, layer_name):
		try:
			self.layer_list[layer_name].disable_event()
		except:
			log.err(repr(self), layer_name, traceback.format_exc())
	
	def layer_get_event_enable(self, layer_name):
		try:
			return self.layer_list[layer_name].get_event_enable()
		except:
			log.err(repr(self), layer_name, traceback.format_exc())
	
	def layer_mouse_leave(self, layer_name):
		try:
			for w in self.layer_list[layer_name].get_children():
				if isinstance(w, button.Button):
					w.mouse_leave()
		except:
			log.err(repr(self), layer_name, traceback.format_exc())
	
	def widget_put(self, layer_name, w, x, y):
		try:
			w.window_obj = self
			if isinstance(w, effect.Effect):
				l = self.layer_list[layer_name]
				w.layer = l
				w.layer_name = layer_name
				w.set_coord(x, y)
				for img in w.image_list:
					img.layer and self.widget_del(img)
					img.layer = l
					img.layer_name = layer_name
					img.set_coord(x, y)
					img.layer.put(img, img.real_x, img.real_y)
			else:
				w.layer and self.widget_del(w)
				w.layer = self.layer_list[layer_name]
				w.layer_name = layer_name
				w.set_coord(x, y)
				w.layer.put(w, w.real_x, w.real_y)
		except:
			log.err(repr(self), layer_name, w, x, y, traceback.format_exc())
	
	def widget_del(self, w):
		try:
			w.window_obj = None
			if isinstance(w, effect.Effect):
				for i in w.image_list:
					i.layer.remove(i)
					i.layer = None
					i.layer_name = ""
			else:
				w.layer.remove(w)
				w.layer = None
				w.layer_name = ""
		except:
			log.err(repr(self), w, traceback.format_exc())
	
	def widget_active(self, w):
		try:
			if isinstance(w, effect.Effect):
				for i in w.image_list:
					i.layer.remove(i)
					i.layer.put(i, i.real_x, i.real_y)
			else:
				w.layer.remove(w)
				w.layer.put(w, w.real_x, w.real_y)
		except:
			log.err(repr(self), w, traceback.format_exc())
	
	def _widget_move(self, w, x, y):
		#print "_widget_move", x, y
		try:
			if isinstance(w, effect.Effect):
				for i in w.image_list:
					i.set_coord(x, y)
					i.layer.move(i, i.real_x, i.real_y)
			else:
				w.set_coord(x, y)
				w.layer.move(w, w.real_x, w.real_y)
		except:
			log.err(repr(self), w, x, y, traceback.format_exc())
	
	def widget_move(self, w, x, y, time_use=0, delay=50, run=None, args=()):
		timer.timeout_list_clear(w.move_id_list)
		if not time_use:
			self._widget_move(w, x, y)
			return
		widget_x, widget_y = w.get_coord()
		if (x, y) == (widget_x, widget_y):
			self._widget_move(w, x, y)
			return
		w.push_running()
		step_count = float(time_use)/delay
		if step_count < 1:
			step_count = 1.0
		x_dev, y_dev = (x-widget_x)/step_count, (y-widget_y)/step_count
		for i in xrange(int(step_count)-1):
			timer.timeout_list_append(
				w.move_id_list,
				delay*(i+1),
				self._widget_move,
				w,
				widget_x+x_dev*i,
				widget_y+y_dev*i,
			)
		if run:
			timer.timeout_list_append(
				w.move_id_list,
				time_use,
				run,
				*args
			)
		timer.timeout_list_append(
			w.move_id_list,
			time_use+1,
			self._widget_move,
			w,
			x,
			y,
		)
		timer.timeout_list_append(
			w.move_id_list,
			time_use+1,
			w.pop_running,
		)
	
	def get_widgets_from_layer(self, layer_name):
		try:
			return self.layer_list[layer_name].get_children()
		except:
			log.err(repr(self), layer_name, traceback.format_exc())
	
	def get_screenshot(self):
		return image.get_screenshot(self.window)
