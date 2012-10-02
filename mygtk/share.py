#!/usr/bin/env python
# -*- coding:utf-8 -*-
import gtk
import sys
import os
import log
import convert
import traceback
import threading
import random
import socket
import Image

SCRIPT_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
STD_WIDTH = 0
STD_HEIGHT = 0
REAL_WIDTH = 0
REAL_HEIGHT = 0
WIDTH_ZOOM_SCALE = 1.0
HEIGHT_ZOOM_SCALE = 1.0
GLOBAL_FONT_PATH = ""
GLOBAL_FONT_SIZE = 25
GLOBAL_GTK_FONT_NAME = "system"
GLOBAL_GTK_FONT_SIZE = 11
WINDOW_TITLE = ""
KEY = ""
SCREENSHOT_PATH = "__SCREENSHOT__"
SCREENSHOT_FORMAT = "png"
LOCK_PATH = "__LOCK__"
RESTORE_PATH = "__RESTORE__"

IMAGE_RESIZE_MODE = Image.ANTIALIAS
SCREEN_WIDTH, SCREEN_HEIGHT = gtk.gdk.get_default_root_window().get_size()
USE_FULLSCREEN = False

EVENT_RETURN_NONE = "__EVENT_RETUEN_NONE__" #pass event
EVENT_RETURN_FALSE = "__EVENT_RETURN_FALSE__" #pass event
EVENT_RETURN_TRUE = "__EVENT_RETURN_TRUE__" #break event
CTRL_MASK = gtk.gdk.CONTROL_MASK
ALT_MASK = gtk.gdk.MOD1_MASK
SHIFT_MASK = gtk.gdk.SHIFT_MASK
SUPER_MASK = gtk.gdk.SUPER_MASK #gtk.gdk.MOD4_MASK

USE_ZLIB = True
USE_DATA_BUFFER = True
IODATA_BUFFER = []
MAX_IODATA_BUFFER = 100
ENCODE_BYTES = 1024*1
PATCH_ARCHIVE = "update.bin"
ARCHIVE_READ_LOCK = threading.RLock()

MPLAYER_POSIX_PATH = "mplayer"
MPLAYER_NT_PATH = "./mplayer-bin/mplayer.exe"
HTTP_HANDLE_INTERVAL = 30
PLAYER_RUN_END_DELAY = 100

GLOBAL_WAIT_DELAY = 0.03
PLAYER_THREAD = None
GTK_LOCK = None

EVENT_LIST = {
	# event_name: gtk_event_name, pass_arg_count, run_after
	"onshow"		: ("focus-in-event", 2), #map-event only work on linux
	"exit"		: ("delete_event", 1),
	"destroy"		: ("destroy", 1),
	"realize"		: ("realize", 1),
	"draw"		: ("expose-event", 2),
	"mouse_enter"	: ("enter-notify-event", 2),
	"mouse_leave"	: ("leave-notify-event", 2),
	"mouse_down"	: ("button_press_event", 1),
	"mouse_up"	: ("button_release_event", 1),
	"mouse_click"	: ("button_release_event", 1),
	"mouse_move"	: ("motion_notify_event", 1),
	"key_down"	: ("key-press-event", 1),
	"key_up"		: ("key-release-event", 1),
}

EVENT_MASK = (
	gtk.gdk.EXPOSURE_MASK |
	gtk.gdk.ENTER_NOTIFY_MASK |
	gtk.gdk.LEAVE_NOTIFY_MASK |
	gtk.gdk.KEY_PRESS_MASK |
	gtk.gdk.KEY_RELEASE_MASK |
	gtk.gdk.POINTER_MOTION_MASK |
	gtk.gdk.POINTER_MOTION_HINT_MASK |
	gtk.gdk.BUTTON_PRESS_MASK |
	gtk.gdk.BUTTON_RELEASE_MASK |
	gtk.gdk.BUTTON_MOTION_MASK |
	gtk.gdk.BUTTON1_MOTION_MASK |
	gtk.gdk.BUTTON2_MOTION_MASK |
	gtk.gdk.BUTTON3_MOTION_MASK
)

MAIN_WINDOW = None

def _get_port():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	while True:
		port = random.randint(1024, 65535)
		try:
			s.connect(("127.0.0.1", port))
		except:
			break
		else:
			s.close()
	del s
	return port
PORT = _get_port()

get_key = gtk.gdk.keyval_from_name #get_key(key_name)
get_key_name = gtk.gdk.keyval_name #get_key_name(keyval)

def set_global_font_path(path):
	try:
		global GLOBAL_FONT_PATH
		assert os.path.isfile(path)
		GLOBAL_FONT_PATH = convert.get_str(path)
	except:
		log.err(traceback.format_exc())

def set_global_font_size(size):
	try:
		global GLOBAL_FONT_SIZE
		GLOBAL_FONT_SIZE = int(size)
	except:
		log.err(traceback.format_exc())

def set_image_resize_mode(mode):
	"""mode: NEAREST, BILINEAR, BICUBIC, ANTIALIAS"""
	assert mode in ("NEAREST", "BILINEAR", "BICUBIC", "ANTIALIAS")
	global IMAGE_RESIZE_MODE
	IMAGE_RESIZE_MODE = getattr(Image, mode)

def set_use_fullscreen(mode):
	global USE_FULLSCREEN
	USE_FULLSCREEN = bool(mode)

def set_gtk_theme_name(name): #Raleigh, ...
	settings = gtk.settings_get_default()
	settings.set_property("gtk-theme-name", name)
	settings.set_property("gtk-icon-theme-name", name)

def set_gtk_font(name, size):
	global GLOBAL_GTK_FONT_NAME, GLOBAL_GTK_FONT_SIZE
	GLOBAL_GTK_FONT_NAME = name
	GLOBAL_GTK_FONT_SIZE = size
	size = int(size*(WIDTH_ZOOM_SCALE+HEIGHT_ZOOM_SCALE)*0.5)
	gtk.settings_get_default().set_property("gtk-font-name", "%s %s"%(name, size))
