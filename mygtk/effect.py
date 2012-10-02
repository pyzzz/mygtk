#!/usr/bin/env python
# -*- coding:utf-8 -*-
import image
import share
import widget
import timer
import time

class Effect(widget.Widget):
	def __init__(self, delay_ms, path=None,
			i_start=None, i_end=None, show=True, fullscreen=False):
		widget.Widget.__init__(self)
		self.delay = delay_ms
		self.image_list = []
		self.path = None
		self.start_index = 0
		self.end_index = 0
		self.index_range = 0
		self.window_obj = None
		if path != None and i_start != None and i_end != None:
			self.load_path(path, i_start, i_end)
		show and self.show()
	
	def clear(self):
		self.stop()
		if self.window_obj:
			while self.image_list:
				self.window_obj.widget_del(self.image_list.pop())
		else:
			while self.image_list:
				self.image_list.pop()
	
	def setup(self):
		if self.window_obj:
			self.window_obj.widget_put(self.layer_name, self, self.x, self.y)
	
	def load_path(self, path, i_start, i_end):
		self.clear()
		self.path = path
		self.start_index = i_start
		self.end_index = i_end
		self.index_range = i_end-i_start+1
		for i in xrange(start_index, end_index+1):
			img = image.Image(path%i, False)
			if fullscreen:
				img.set_image_size(share.REAL_WIDTH, share.REAL_HEIGHT)
			self.image_list.append(img)
		self.setup()
	
	def show(self, i_show=0):
		for i, img in enumerate(self.image_list):
			if i == i_show:
				img.show()
			else:
				img.hide()
	
	def show_all(self):
		self.stop()
		for img in self.image_list:
			img.show()
	
	def hide(self):
		for img in self.image_list:
			img.hide()
	
	def set_transparent(self, value):
		for img in self.image_list:
			img.set_transparent(value)
	
	def get_transparent(self):
		for img in self.image_list:
			return img.get_transparent()
	
	def get_coord(self):
		for img in self.image_list:
			return img.get_coord()
	
	def run(self, run_end=None, args=(), reverse=False, hide=True):
		timer.timeout_list_clear(self.run_id_list)
		self.push_running()
		if reverse:
			r = enumerate(reversed(xrange(self.index_range)))
		else:
			r = enumerate(xrange(self.index_range))
		for i, j in r:
			timer.timeout_list_append(
				self.run_id_list,
				self.delay*(i+1),
				self.show,
				j,
			)
		if run_end:
			timer.timeout_list_append(
				self.run_id_list,
				self.delay*(self.index_range+1),
				run_end,
				*args
			)
		if hide:
			timer.timeout_list_append(
				self.run_id_list,
				self.delay*(self.index_range+1),
				self.hide,
			)
		timer.timeout_list_append(
			self.run_id_list,
			self.delay*(self.index_range+1),
			self.pop_running,
		)
		#log.msg(repr(self), self.run_id_list)
	
	def run_reverse(self,
			run_end=None, args=(), reverse=True, hide=False):
		self.run(run_end, args, reverse, hide)
	
	def run_turn(self, run_half=None, args_half=(), run_end=None, args_end=()):
		#TODO: self.wait return when run_reverse finish if delay not equal, fix it
		self.run_reverse(run_half, args_half)
		timer.timeout_list_append(
			self.run_id_list,
			self.delay*(self.index_range+1),
			self.run,
			run_end,
			args_end,
		)
	
	def set_events(self, *args):
		pass
