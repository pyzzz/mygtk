#!/usr/bin/env python
# -*- coding:utf-8 -*-
import gtk
import widget
import share
import log
import traceback

class GtkText(widget.Widget, gtk.Label):
	def __init__(self, text=None, name=None, size=None, color=None):
		gtk.Label.__init__(self)
		widget.Widget.__init__(self)
		if text != None:
			self.set_text(text)
		if name != None and size != None:
			self.set_font(name, size)
		if color != None:
			self.set_color(color)
		self.show()
	
	def show(self):
		gtk.Label.show(self)
	
	def hide(self):
		gtk.Label.hide(self)
	
	def get_text(self):
		return gtk.Label.get_text(self)
	
	def set_text(self, text):
		gtk.Label.set_text(self, text)
	
	def set_color(self, color):
		self.set_fg(color)
		self.set_font_color(color)
