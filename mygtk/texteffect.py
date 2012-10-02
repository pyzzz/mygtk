#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
import image
import effect
import timer
import share
import convert
import log
import traceback
import Image
import ImageDraw, ImageFont, ImageColor

def get_ink_with_alpha(self, fill=None, alpha=None):
	ink = self.ink if (fill == None) else fill
	if ink == None:
		return ink
	if Image.isStringType(ink):
		ink = ImageColor.getcolor(ink, self.mode)
	if self.palette and not Image.isNumberType(ink):
		ink = self.palette.getcolor(ink)
	if alpha != None: #and self.mode == "RGBA"
		ink = ink[:3]+(alpha,)
	#print ink
	return self.draw.draw_ink(ink, self.mode)

def set_text_with_alpha(self, xy, text, fill=None, font=None, alpha=None):
	ink = get_ink_with_alpha(self, fill, alpha)
	if ink == None:
		return
	if font == None:
		font = self.getfont()
	try:
		mask, offset = font.getmask2(text, self.fontmode)
		xy = xy[0] + offset[0], xy[1] + offset[1]
	except AttributeError:
		try:
			mask = font.getmask(text, self.fontmode)
		except TypeError:
			mask = font.getmask(text)
	self.draw.draw_bitmap(xy, mask, ink)

def image_list_from_text(string, length_once, width, height,
		font_path, font_size, color=None):
	font_path = font_path or share.GLOBAL_FONT_PATH
	font_size = font_size or share.GLOBAL_FONT_SIZE
	color = color or "#000"
	string = convert.get_unicode(string).replace("\r\n", "\n")
	font = ImageFont.truetype(font_path, font_size)
	space = 1
	x, y = space, 0
	length_buffer = 0
	img_list = []
	draw_next = None
	img = Image.new("RGBA", (int(width), int(height)))
	draw = ImageDraw.Draw(img)
	for word in string:
		if word == "\n":
			x = space
			y += font_size+space
			continue
		if draw_next:
			set_text_with_alpha(
				draw_next, (x, y), word, font=font, fill=color, alpha=50
			)
			draw_next = None
		if length_buffer >= length_once:
			set_text_with_alpha(draw, (x, y), word, font=font, fill=color, alpha=100)
			length_buffer = 0
			draw_next = draw
			img_list.append(img)
			img = Image.new("RGBA", (int(width), int(height)))
			draw = ImageDraw.Draw(img)
		set_text_with_alpha(draw, (x, y), word, font=font, fill=color)
		if ord(word) < 255:
			x += font_size*0.5
			length_buffer += 0.5
		else:
			x += font_size*1
			length_buffer += 1
		if (x+font_size+space) > width:
			x = space
			y += font_size+space
	if length_buffer:
		img_list.append(img)
	return img_list

class TextEffect(effect.Effect):
	def __init__(self, delay_ms, length_once, width, height,
			string="", *args, **kwargs):
		assert length_once > 0
		effect.Effect.__init__(self, delay_ms)
		self.length_once = length_once
		self.width = width
		self.height = height
		self.text = ""
		if string:
			self.load_text(string, *args, **kwargs)
	
	def show(self, i_show=0):
		if not self.image_list:
			return
		self.image_list[i_show].show()
	
	def run(self, run_end=None, args=(), reverse=False, hide=False):
		self.hide()
		effect.Effect.run(self, run_end, args, reverse, hide)
	
	def load_text(self, string, font_size=None, font_path=None, color=None):
		if not font_path:
			assert os.path.isfile(share.GLOBAL_FONT_PATH)
		if not string:
			return
		try:
			self.clear()
			self.text = string
			for pimg in image_list_from_text(
				string,
				self.length_once,
				self.width,
				self.height,
				font_path,
				font_size,
				color
			):
				img = image.Image(show=False)
				img.set_image(image.image_from_auto_resize(pimg))
				self.image_list.append(img)
			self.start_index = 0
			self.end_index = len(self.image_list)-1
			self.index_range = len(self.image_list)
			self.setup()
		except:
			log.err(repr(self),
				string,
				font_size,
				font_path,
				color,
				traceback.format_exc(),
			)
	
	def get_text(self):
		return self.text
	
	def get_text_length(self):
		return len(self.text)
