#!/usr/bin/env python
# -*- coding:utf-8 -*-
import gtk
import sys
import os
import time
import traceback
import gobject
import log
import share
import widget
import window
import layer
import lock
import timer
import event
import convert
import image
import text
import texteffect
import gtktext
import effect
import dialog
import scrolledwindow
import textview
import eventbox
import button
import drawingarea
import player
import Image
import warnings
from share import get_key, get_key_name
from share import EVENT_RETURN_NONE, EVENT_RETURN_FALSE, EVENT_RETURN_TRUE
from share import CTRL_MASK, ALT_MASK, SHIFT_MASK, SUPER_MASK
from event import with_mask
from button import Button
from dialog import dialog
from drawingarea import DrawingArea
from effect import Effect
from eventbox import EventBox
from gtktext import GtkText
from image import Image
from layer import Layer
from window import Window
from log import msg, err
from player import Player, MoviePlayer
from scrolledwindow import ScrolledWindow
from text import Text
from texteffect import TextEffect
from textview import TextView
from widget import Widget
warnings.filterwarnings("ignore", category=DeprecationWarning)

def init(std_width=400, std_height=300, password="", workdir="", use_player=True):
	share.STD_WIDTH = std_width
	share.STD_HEIGHT = std_height
	share.REAL_WIDTH = std_width
	share.REAL_HEIGHT = std_height
	if password:
		share.KEY = archive.Key(password)
	os.chdir(workdir or share.SCRIPT_DIR)
	if os.name == "posix":
		gtk.gdk.threads_init()
	else:
		gobject.threads_init()
	if use_player:
		player.start_http_server()

def run():
	if os.path.exists(share.LOCK_PATH):
		lock.remove_file(share.LOCK_PATH)
		log.msg("check lock...")
		for i in xrange(5):
			time.sleep(0.5)
			if os.path.exists(share.LOCK_PATH):
				log.err("lock exist, exit")
				lock.create_file(share.RESTORE_PATH)
				os._exit(1)
	timer.timeout_add(500, lock.check_lock)
	share.MAIN_WINDOW.show()
	gtk.main()

def exit(*args):
	event.exit(*args)
