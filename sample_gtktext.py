#!/usr/bin/env python
# -*- coding:utf-8 -*-
import mygtk

if __name__ == "__main__":
	mygtk.init(400, 300)
	main = mygtk.Window("gtktext", 400, 300)
	main.set_bg("#111")
	main.layer_add("test")
	main.widget_put(
		"test",
		mygtk.GtkText("hello world", "Monospace", 20, "#FFF"),
		100,
		100,
	)
	mygtk.run()
