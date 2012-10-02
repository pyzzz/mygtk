#!/usr/bin/env python
# -*- coding:utf-8 -*-
import gtk
import widget

class EventBox(widget.Widget, gtk.EventBox):
	def __init__(self):
		gtk.EventBox.__init__(self)
		widget.Widget.__init__(self)
		self.widget = None
		self.set_visible_window(False)
		self.show()
	
	def add(self, w):
		gtk.EventBox.add(self, w)
		self.widget = w
		self.set_size(*w.get_size())
	
	def get_widget(self):
		return self.widget
