#!/usr/bin/env python
# -*- coding:utf-8 -*-
import mygtk
import os

if __name__ == "__main__":
	mygtk.init()
	key = mygtk.archive.Key("password")
	mygtk.archive.pack("sample.bin", "test.zip", key)
	print mygtk.archive.read("test.zip>inc.txt", key)
	#mygtk.lock.remove_file("test.zip")