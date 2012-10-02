#!/usr/bin/env python
# -*- coding:utf-8 -*-
import gtk
import widget
import log
import convert
import share
import lock
import archive
import traceback
import Image as PIL
try:
	from cStringIO import StringIO
except:
	from StringIO import StringIO

def pixbuf_from_string(string, w, h):
	return gtk.gdk.pixbuf_new_from_data(
		string,
		gtk.gdk.COLORSPACE_RGB,
		True,
		8,
		w,
		h,
		w*4,
	)

def pixbuf_from_image(img):
	return pixbuf_from_string(img.tostring(), *img.size)

def image_from_pixbuf(pixbuf):
	if not pixbuf.get_has_alpha():
		pixbuf.add_alpha(False, 0, 0, 0)
	img = PIL.new("RGBA", (pixbuf.get_width(), pixbuf.get_height()))
	img.fromstring(pixbuf.get_pixels())
	return img

def pixmap_from_string(string, w, h):
	pixmap = gtk.gdk.Pixmap(None, w, h, 32)
	colormap = gtk.gdk.Screen().get_rgba_colormap()
	colormap and pixmap.set_colormap(colormap)
	pixmap_gc = gtk.gdk.GC(pixmap)
	pixmap.draw_rgb_32_image(
		pixmap_gc,
		0,
		0,
		w,
		h,
		gtk.gdk.RGB_DITHER_NORMAL,
		string,
	)
	return pixmap

def pixmap_from_image(image):
	return pixmap_from_string(
		image.tostring(),
		image.size[0],
		image.size[1],
	)

def pixmap_from_pixbuf(pixbuf):
	return pixmap_from_string(
		pixbuf.get_pixels(),
		pixbuf.get_width(),
		pixbuf.get_height(),
	)

def pixbuf_from_area(pixbuf, x, y, w, h):
	pixbuf_new = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, w, h)
	pixbuf.copy_area(x, y, w, h, pixbuf_new, 0, 0)
	return pixbuf_new

def pixbuf_from_area_resize(pixbuf, x, y, w, h):
	x = int(x*share.WIDTH_ZOOM_SCALE)
	y = int(y*share.HEIGHT_ZOOM_SCALE)
	w = int(w*share.WIDTH_ZOOM_SCALE)
	h = int(h*share.HEIGHT_ZOOM_SCALE)
	pixbuf_new = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, w, h)
	pixbuf.copy_area(x, y, w, h, pixbuf_new, 0, 0)
	return pixbuf_new

def pixbuf_from_composite_color(pixbuf, color, alpha):
	try:
		w, h = pixbuf.get_width(), pixbuf.get_height()
		pixbuf_color = pixbuf_from_string(
			"".join(map(chr, convert.color_list(color)))*w*h,
			w,
			h,
		)
		pixbuf_color.composite(
			pixbuf, 0, 0, w, h, 0, 0, 1, 1, gtk.gdk.INTERP_BILINEAR, alpha,
		)
	except:
		log.err(pixbuf, color, alpha, traceback.format_exc())
	return pixbuf

def pixbuf_from_resize(pixbuf, w, h):
	return pixbuf.scale_simple(
		max(int(w), 1),
		max(int(h), 1),
		gtk.gdk.INTERP_BILINEAR,
	)

def image_from_auto_resize(img):
	if share.WIDTH_ZOOM_SCALE == 1 and share.HEIGHT_ZOOM_SCALE == 1:
		return img
	w, h = img.size
	w_new = max(int(w*share.WIDTH_ZOOM_SCALE), 1)
	h_new = max(int(h*share.HEIGHT_ZOOM_SCALE), 1)
	return img.resize((w_new, h_new), share.IMAGE_RESIZE_MODE)

def image_set_transparent(img, old_value, value):
	data = []
	for color in img.getdata():
		data.append(color[:3] + (int(round(color[3]/old_value*value, 0)), ))
	img.putdata(data)
	return img

class Image(gtk.Image, widget.Widget):
	def __init__(self, path="", show=True):
		gtk.Image.__init__(self)
		widget.Widget.__init__(self)
		self.transparent = 1
		if path:
			self.load_path(path)
		if show:
			self.show()
	
	def get_image(self):
		return image_from_pixbuf(self.get_pixbuf())
	
	def get_pixbuf(self):
		return gtk.Image.get_pixbuf(self)
	
	def set_image(self, image):
		self.set_pixbuf(pixbuf_from_image(image))
	
	def set_pixbuf(self, pixbuf):
		self.set_real_size(pixbuf.get_width(), pixbuf.get_height())
		gtk.Image.set_from_pixbuf(self, pixbuf)
	
	def load_path(self, path):
		try:
			data = archive.read(path, share.KEY)
			if not data:
				raise Exception("read failed")
			self.set_image(
				image_from_auto_resize(
					PIL.open(StringIO(data)).convert("RGBA")
				)
			)
		except:
			log.err(repr(self), path, traceback.format_exc())
	
	def set_image_size(self, w, h):
		self.set_image(
			self.get_image().resize(
				(max(w, 1), max(h, 1)),
				share.IMAGE_RESIZE_MODE,
			)
		)
	
	def set_pixbuf_size(self, w, h):
		self.set_pixbuf(
			pixbuf_from_resize(
				self.get_pixbuf(),
				w,
				h,
			)
		)
	
	def set_transparent(self, value):
		assert type(value) in (int, float)
		assert (value >= 0 and value <= 1)
		if value == self.transparent:
			return
		self.set_image(
			image_set_transparent(
				self.get_image(),
				self.transparent,
				value,
			)
		)
		self.transparent = value
	
	def get_transparent(self):
		return self.transparent
	
	def save(self, path, format="png", *args, **argv):
		self.get_pixbuf().save(path, format, *args, **argv)

def get_screenshot(window):
	w, h = window.get_size()
	pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, w, h)
	pixbuf.get_from_drawable(window, window.get_colormap(), 0, 0, 0, 0, w, h)
	pixbuf.save(share.SCREENSHOT_PATH, share.SCREENSHOT_FORMAT)
	img = Image(share.SCREENSHOT_PATH)
	lock.remove_file(share.SCREENSHOT_PATH)
	return img

def GetDesktop():
	return get_screenshot(gtk.gdk.get_default_root_window())
