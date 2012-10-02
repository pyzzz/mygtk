#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
import image
import share
import convert
import log
import traceback
import Image
import ImageDraw, ImageFont

def image_from_text(string, font_path, font_size, color=None, image_bg=None):
	font_path = font_path or share.GLOBAL_FONT_PATH
	font_size = font_size or share.GLOBAL_FONT_SIZE
	color = color or "#000"
	if image_bg: # from Button.__init__
		font_size = int(font_size*(share.WIDTH_ZOOM_SCALE+share.HEIGHT_ZOOM_SCALE)/2)
	string = convert.get_unicode(string)
	font = ImageFont.truetype(font_path, font_size)
	space = 1
	#guess size
	i = w = h = space*3
	for line in string.replace("\r\n", "\n").split("\n"):
		for word in line:
			i += font_size*(0.5 if ord(word)<255 else 1)
		w = max(i, w)
		i = space*3
		h += font_size*1.3+space
	#set bg
	if not image_bg:
		img = Image.new("RGBA", (int(w), int(h)))#, "#FFF")
		x, y = space, 0
	else:
		img = image_bg
		x, y = int((img.size[0]-w)/2), int((img.size[1]-h)/2)
	#draw text
	draw = ImageDraw.Draw(img)
	for line in string.replace("\r\n", "\n").split("\n"):
		for word in line:
			draw.text((x, y), word, font=font, fill=color)
			x += font_size*(0.5 if ord(word)<255 else 1)
		x = space
		y += font_size+space
	return img

def image_from_draw_outline(img, color, outline_width=1, draw_shadow=False):
	outline_color_out = color_to_list(color, 0x50)
	outline_color_mid = color_to_list(color, 0x90)
	outline_color_in = color_to_list(color, 255)
	outline_range_out = round(outline_width*2*(3/3.0), 0)
	outline_range_mid = round(outline_width*2*(2/3.0), 0)
	outline_range_in = round(outline_width*2*(1/3.0), 0)
	def set_color(data, index, data_length, color):
		if index < 0:
			return
		if index >= data_length:
			return
		if color[3] > data[index][3]:
			data[index] = color
	if draw_shadow:
		width_range = range(0, outline_width+1)
	else:
		width_range = range(0-outline_width, outline_width+1)
	img_w, img_h = img.size
	new = Image.new("RGBA", img.size)
	data = list(new.getdata())
	data_length = len(data)
	for i, color in enumerate(img.getdata()):
		if not color[3]:
			continue
		if i%img_w < outline_width:
			continue
		for j in width_range:
			for k in width_range:
				outline_range = abs(j)+abs(k)
				index = i+j*(img_w)+k
				if outline_range <= outline_range_in:
					set_color(data, index, data_length, outline_color_in)
				elif outline_range <= outline_range_mid:
					set_color(data, index, data_length, outline_color_mid)
				elif outline_range <= outline_range_out:
					set_color(data, index, data_length, outline_color_out)
	new.putdata(data)
	new.paste(img, (0, 0), img)
	return new

class Text(image.Image):
	def __init__(self, string="", *args, **kwargs):
		image.Image.__init__(self)
		self.text = ""
		self.load_text(string, *args, **kwargs)
	
	def load_text(self, string, font_size=None, font_path=None, color=None):
		if not font_path:
			assert os.path.isfile(share.GLOBAL_FONT_PATH)
		try:
			self.text = string
			self.set_image(
				image.image_from_auto_resize(
					image_from_text(
						string,
						font_path,
						font_size,
						color,
					)
				)
			)
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
	
	def draw_out_line(self, color="#FFF", width=1):
		try:
			self.set_image(
				image_from_draw_outline(
					self.get_image(),
					color,
					width,
				)
			)
		except:
			log.err(repr(self), color, width, traceback.format_exc())
	
	def draw_shadow(self, color="#FFF", width=2):
		try:
			self.set_image(
				image_from_draw_outline(
					self.get_image(),
					color,
					width,
					True,
				)
			)
		except:
			log.err(repr(self), color, width, traceback.format_exc())
