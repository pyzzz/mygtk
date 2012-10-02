#!/usr/bin/env python
# -*- coding:utf-8 -*-
import gtk
import widget
import eventbox
import traceback
import text
import image
import log

class Button(eventbox.EventBox):
	def __init__(self,
			button_normal,
			button_select,
			string="",
			font_size=None,
			font_path=None,
			color=None,
			run=None,
			run_args=()):
		eventbox.EventBox.__init__(self)
		if type(button_normal) in (str, unicode):
			self.image_normal = image.Image(button_normal)
		else:
			self.image_normal = button_normal
		if type(button_select) in (str, unicode):
			self.image_select = image.Image(button_select)
		else:
			self.image_select = button_select
		if string:
			self.image_normal.set_image(
				text.image_from_text(
					string,
					font_size,
					font_path,
					color,
					self.image_normal.get_image(),
				)
			)
			self.image_select.set_image(
				text.image_from_text(
					string,
					font_size,
					font_path,
					color,
					self.image_select.get_image(),
				)
			)
		self.mode = 0 #0:normal, 1:select
		self.add(self.image_normal)
		self.bind_event("mouse_enter", self.event_mouse_enter)
		self.bind_event("mouse_leave", self.event_mouse_leave)
		if run:
			self.bind_event("mouse_click", run, *run_args)
	
	def mouse_enter(self):
		for w in self.get_children():
			self.remove(w)
		self.add(self.image_select)
		self.mode = 1
	
	def mouse_leave(self):
		for w in self.get_children():
			self.remove(w)
		self.add(self.image_normal)
		self.mode = 0
	
	def event_mouse_enter(self):
		(self.mode == 0) and self.mouse_enter()
	
	def event_mouse_leave(self):
		(self.mode == 1) and self.mouse_leave()
