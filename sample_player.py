#!/usr/bin/env python
# -*- coding:utf-8 -*-
import mygtk
import thread

def play_noise(*args):
	player.play("./sample.bin>noise.wav")
	player.wait()
	mygtk.msg("play end")

def play_movie(*args):
	if movieplayer.alive():
		movieplayer.stop()
		return
	movieplayer.play("./test.mpg")
	movieplayer.wait()
	mygtk.msg("play end")

def start_thread(event, target, args=()):
	thread.start_new_thread(target, args)

def exit(*args):
	player.stop()
	movieplayer.stop()
	mygtk.exit()

if __name__ == "__main__":
	mygtk.init(1024, 768, "password")
	mygtk.share.set_global_font_path("./mplus/mplus-1m-regular.ttf")
	mygtk.share.set_global_font_size(20)
	
	player = mygtk.Player()
	#player.set_volume(0.5)
	
	movieplayer = mygtk.MoviePlayer(800, 600, "#111")
	#movieplayer.set_volume(0.5)
	
	main = mygtk.Window("sample image")
	#main.SetBG("#111")
	main.layer_add("button")
	main.layer_add("player")
	
	main.widget_put("player", movieplayer, 10, 10)
	main.widget_put(
		"button",
		mygtk.Button(
			"./sample.bin>normal.png",
			"./sample.bin>select.png",
			"play noise",
			run=start_thread,
			run_args=(play_noise,)
		),
		100,
		650,
	)
	main.widget_put(
		"button",
		mygtk.Button(
			"./sample.bin>normal.png",
			"./sample.bin>select.png",
			"play movie",
			run=start_thread,
			run_args=(play_movie,)
		),
		400,
		650,
	)
	
	main.bind_event("exit", exit)
	mygtk.run()