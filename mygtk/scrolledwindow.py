#!/usr/bin/env python
# -*- coding:utf-8 -*-
import gtk
import widget

class ScrolledWindow(widget.Widget, gtk.ScrolledWindow):
	def __init__(self, w=None):
		gtk.ScrolledWindow.__init__(self)
		widget.Widget.__init__(self)
		self.widget = None
		self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		if w:
			self.add(w)
		self.show()
	
	def add(self, w):
		gtk.ScrolledWindow.add(self, w)
		self.widget = w
