#!/usr/bin/env python
# -*- coding:utf-8 -*-
import gtk
import share
import log
import lock
import timer

def with_mask(event, *args):
	mask_all = 0
	for mask in args:
		mask_all |= mask
	return (event.state & mask_all)

def exit(*args):
	#log.msg("exit")
	lock.remove_file(share.LOCK_PATH)
	gtk.main_quit()
