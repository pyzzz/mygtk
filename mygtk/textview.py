#!/usr/bin/env python
# -*- coding:utf-8 -*-
import gtk
import widget
import log
import convert

class TextView(widget.Widget, gtk.TextView):
	def __init__(self, text_buffer=None, pixmap=None):
		gtk.TextView.__init__(self)
		widget.Widget.__init__(self)
		self.pixmap = pixmap
		self.buf = text_buffer or gtk.TextBuffer()
		self.set_wrap_mode(True)
		self.set_buffer(self.buf)
		if pixmap:
			self.set_real_size(*pixmap.get_size())
			self.bind_event("realize", self.realize, True)
		self.show()
	
	def realize(self, *args):
		if not self.pixmap:
			return
		window = self.get_window(gtk.TEXT_WINDOW_TEXT)
		if window:
			window.set_back_pixmap(self.pixmap, False)
	
	def get_text(self):
		return self.buf.get_text(
			self.buf.get_start_iter(),
			self.buf.get_end_iter(),
		)
	
	def set_text(self, text):
		self.buf.set_text(convert.get_str(text))
	
	def set_editable(self, *args):
		gtk.TextView.set_editable(self, *args)
		self.realize()
	
	def set_cursor_visible(self, *args):
		gtk.TextView.set_cursor_visible(self, *args)
		self.realize()
	
	def modify_text(self, *args):
		gtk.TextView.modify_text(self, *args)
		self.realize()
