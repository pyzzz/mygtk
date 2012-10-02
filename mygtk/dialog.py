#!/usr/bin/env python
# -*- coding:utf-8 -*-
import gtk

def dialog(message, title="", ok="OK", cancel=None, default_ok=True):
	d = gtk.Dialog(title)
	d.add_button(ok, gtk.RESPONSE_OK)
	if cancel:
		d.add_button(cancel, gtk.RESPONSE_CANCEL)
	d.set_default_response(gtk.RESPONSE_OK if default_ok else gtk.RESPONSE_CANCEL)
	d.vbox.pack_start(gtk.Label(""))
	d.vbox.pack_start(gtk.Label(message))
	d.vbox.pack_start(gtk.Label(""))
	d.show_all()
	response = (d.run() == gtk.RESPONSE_OK)
	d.destroy()
	return response

