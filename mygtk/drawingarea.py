#!/usr/bin/env python
# -*- coding:utf-8 -*-
import gtk
import widget
import threading
from share import WIDTH_ZOOM_SCALE, HEIGHT_ZOOM_SCALE

class DrawingArea(widget.Widget, gtk.DrawingArea):
	def __init__(self, width, height, color):
		gtk.DrawingArea.__init__(self)
		widget.Widget.__init__(self)
		self.set_size(width, height)
		self.set_bg(color)
		self.bind_event("draw", self._draw)
		self.command_list = []
		self.command_list_lock = threading.RLock()
		self.show()
	
	def update(self):
		self.queue_draw()
	
	def queue(self, *args):
		with self.command_list_lock:
			self.command_list.append(args)
		self.update()
	
	def _draw(self):
		cr = self.window.cairo_create()
		with self.command_list_lock:
			for command in self.command_list:
				command[0](*(command[1:]+(cr,)))
			del self.command_list
			self.command_list = []
	
	def _draw_line(self, color, x, y, move_x, move_y, transparent, cr):
		cr.set_source_rgba(*color_to_float(color, transparent))
		cr.move_to(x, y)
		cr.rel_line_to(move_x, move_y)
		cr.stroke()
	
	def _draw_square(self, color, x, y, width, height, fill, transparent, cr):
		cr.set_source_rgba(*color_to_float(color, transparent))
		cr.rectangle(x, y, width, height)
		cr.fill() if fill else cr.stroke()
	
	def _draw_circle(self, color, x, y, radius, fill, transparent, cr):
		self._draw_arc(color, x, y, radius, 0, 1, fill, transparent, cr)
	
	def _draw_arc(self, color, x, y, radius, start, end, fill, transparent, cr):
		cr.set_source_rgba(*color_to_float(color, transparent))
		cr.arc(x, y, radius, math.pi*2*start, math.pi*2*end)
		cr.fill() if fill else cr.stroke()
	
	def draw_line(self, color, x, y, move_x, move_y, transparent=1.0):
		self.queue(self._draw_line,
			color,
			int(x*WIDTH_ZOOM_SCALE),
			int(y*HEIGHT_ZOOM_SCALE),
			int(move_x*WIDTH_ZOOM_SCALE),
			int(move_y*HEIGHT_ZOOM_SCALE),
			transparent,
		)
	
	def draw_square(self, color, x, y, width, height, fill=False, transparent=1.0):
		self.queue(
			self._draw_square,
			color,
			int(x*WIDTH_ZOOM_SCALE),
			int(y*HEIGHT_ZOOM_SCALE),
			int(width*WIDTH_ZOOM_SCALE),
			int(height*HEIGHT_ZOOM_SCALE),
			fill,
			transparent,
		)
	
	def draw_circle(self, color, x, y, radius, fill=False, transparent=1.0):
		self.queue(
			self._draw_circle,
			color,
			int(x*WIDTH_ZOOM_SCALE),
			int(y*HEIGHT_ZOOM_SCALE),
			int(radius*(WIDTH_ZOOM_SCALE+HEIGHT_ZOOM_SCALE)/2),
			fill,
			transparent,
		)
	
	def draw_arc(self, color, x, y, radius, start, end, fill=False, transparent=1.0):
		self.queue(self._draw_arc,
			color,
			int(x*WIDTH_ZOOM_SCALE),
			int(y*HEIGHT_ZOOM_SCALE),
			int(radius*(WIDTH_ZOOM_SCALE+HEIGHT_ZOOM_SCALE)/2),
			start,
			end,
			fill,
			transparent,
		)
