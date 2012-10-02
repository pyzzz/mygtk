#!/usr/bin/env python
# -*- coding:utf-8 -*-
import mygtk
import thread

def load_text_effect_thread(*args):
	texteffect.run()
	main.widget_move(texteffect, 50, 50, 1000)
	texteffect.wait()
	mygtk.log.msg("over")

def load_text_effect(*args):
	if texteffect.get_running():
		texteffect.show_all()
	else:
		thread.start_new_thread(load_text_effect_thread, ())

if __name__ == "__main__":
	mygtk.init(400, 300)
	mygtk.share.set_global_font_path("./mplus/mplus-1m-regular.ttf")
	#mygtk.share.SetFullScreenMode(True)
	main = mygtk.window.Window("show text effect when click")
	main.set_bg("#111")
	main.layer_add("test")
	texteffect = mygtk.texteffect.TextEffect(50, 1, 150, 200)
	texteffect.load_text("show text effect when click", color="#FFF")
	main.widget_put("test", texteffect, 100, 100)
	main.bind_event("mouse_click", load_text_effect)
	mygtk.run()
