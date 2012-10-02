#!/usr/bin/env python
# -*- coding:utf-8 -*-

def get_str(s):
	return str(s) if type(s) != unicode else s.encode("utf-8")

def get_unicode(s):
	try:
		return str(s).decode("utf-8") if type(s) != unicode else s
	except UnicodeDecodeError:
		return unicode(s, "latin-1")

def color_list(color, alpha=255):
	if not color.startswith("#"):
		raise Exception("%s not color format"%color)
	if len(color) != 4 and len(color) != 7:
		raise Exception("%s not color format"%color)
	if len(color) <= 4:
		r = int(color[1:2], 16)*0x10
		g = int(color[2:3], 16)*0x10
		b = int(color[3:4], 16)*0x10
	else:
		r = int(color[1:3], 16)
		g = int(color[3:5], 16)
		b = int(color[5:7], 16)
	if alpha != None:
		return (r, g, b, alpha)
	else:
		return (r, g, b)

def gl_color_list(color, transparent=1.0):
	return tuple(map(lambda i: i/255.0, color_list(color, int(transparent*255))))
