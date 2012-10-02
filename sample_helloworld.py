#!/usr/bin/env python
# -*- coding:utf-8 -*-
import mygtk

if __name__ == "__main__":
	mygtk.init(400, 300)
	mygtk.share.set_global_font_path("./mplus/mplus-1m-regular.ttf")
	main = mygtk.Window("sample hello world")
	main.set_bg("#111")
	main.layer_add("test")
	main.widget_put("test", mygtk.Text("hello world", color="#FFF"), 100, 100)
	mygtk.run()
