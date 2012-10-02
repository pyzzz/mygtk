#!/usr/bin/env python
# -*- coding:utf-8 -*-
import mygtk

if __name__ == "__main__":
	mygtk.init(400, 300, "password")
	main = mygtk.Window("sample image")
	main.set_bg("#111")
	main.layer_add("test")
	main.widget_put("test", mygtk.Image("./sample.bin>normal.png"), 100, 100)
	mygtk.run()