#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import convert

def log(pipe, type, *messages):
	pipe.write("%s %s\n"%(
		str(type),
		" ".join(map(lambda s: convert.get_str(s), messages)),
	))

def msg(*messages):
	log(sys.stdout, "[ msg ]", *messages)
def err(*messages):
	log(sys.stderr, "[ err ]", *messages)