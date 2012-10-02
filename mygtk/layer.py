#!/usr/bin/env python
# -*- coding:utf-8 -*-
import gtk
import widget

class Layer(widget.Widget, gtk.Fixed):
	def __init__(self, layer_name=""):
		gtk.Fixed.__init__(self)
		widget.Widget.__init__(self)
		self.layer_name = layer_name
		self.master = None
		self.master_name = ""
