#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import traceback
try: sys.dont_write_bytecode = True
except: pass
import mygtk
import myio

#max line can get from Script.get_script()
MaxScriptLineOnce = 100

def set_max_script_line_once(i):
	global MaxScriptLineOnce
	MaxScriptLineOnce = i

def get_tab_count(code):
	tab_count = 0
	for s in code:
		if s == "\t": tab_count+=1
		else: break
	return tab_count

class Script:
	def __init__(self, script_paths):
		self.script_lines_dict = {}
		self.script_line_max_dict = {}
		self.script_label_dict = {}
		for name, path in script_paths.iteritems():
			script_lines = self.get_script_lines(mygtk.read(path))
			#mygtk.log(script_lines)
			self.script_lines_dict[name] = script_lines
			self.script_line_max_dict[name] = len(script_lines)-1
			self.script_label_dict[name] = {}
		for name, lines in self.script_lines_dict.iteritems():
			for i, line in enumerate(lines):
				if line.startswith("#label") and len(line) > 7:
					self.script_label_dict[name][line[7:].strip()] = i
		self.script_lines = []
		self.script_line_max = 0
		#self.script_line_last = 0
		self.script_line = 0
		self.script_name = ""
		self.script = ""
	
	def get_script_lines(self, code):
		return filter(None,
			code.replace("\r\n", "\n").replace("\\\n", "").split("\n"))
	
	def get_script_from_lines(self, script_lines, line=0):
		#mygtk.log("Script.get_script_from_lines", line)
		code_return = ""
		pass_tab_count = 100
		pass_tab_mask = True
		for l, i in enumerate(xrange(line, len(script_lines))):
			if l > MaxScriptLineOnce:
				break
			code = script_lines[i]
			if pass_tab_mask:
				if code[0] != "\t":
					pass_tab_mask = False
				else:
					j = get_tab_count(code)
					if j < pass_tab_count:
						pass_tab_count = j
					#mygtk.log("strip", pass_tab_count, code)
					code = code[pass_tab_count:]
			code_return += code+"\n"
		#mygtk.log(" code_return", "\n"+code_return, "--------------")
		return code_return
	
	def get_script_name(self):
		return self.script_name
	
	def get_script_line(self):
		return self.script_line #self.script_line_last
	
	def get_label_line(self, label, script_name=None):
		if not script_name:
			script_name = self.get_script_name()
		return self.script_label_dict[script_name][label]
	
	def set_script_line(self, i):
		try: i = int(i)
		except:
			mygtk.logerr("Script.set_script_line Error", traceback.format_exc())
			return
		if i < 0						: i = 0
		elif i > self.script_line_max	: i = self.script_line_max
		self.script_line = i
		self.script = self.get_script_from_lines(self.script_lines, self.script_line)
		self.script_end = False
	
	def set_script_line_from_exc(self):
		for exc in traceback.extract_tb(sys.exc_info()[2]):
			if exc[0] == "<string>" and exc[2] == "<module>" and exc[3] == None:
				new_line = self.script_line+exc[1]
				self.set_script_line(new_line)
				return new_line
	
	def get_script(self):
		#self.script_line_last = self.script_line
		return self.script
	
	def next(self):
		"""if false, script end"""
		return (self.set_script_line_from_exc() <= self.script_line_max)
	
	def next_line(self):
		"""if false, script end"""
		if self.script_line == self.script_line_max:
			return False
		self.set_script_line(self.script_line+1)
		return True
	
	def goto(self, name, line=0):
		#mygtk.log("goto", name, line)
		self.script_lines = self.script_lines_dict[name]
		self.script_line_max = self.script_line_max_dict[name]
		self.script_name = name
		self.script_line = line
		#self.script_line_last = line
		self.set_script_line(line)
	
	def goto_label(self, label, script_name=None):
		if not script_name:
			#mygtk.log("goto_label", label, self.get_label_line(label))
			self.set_script_line(self.get_label_line(label))
		else:
			self.goto(script_name, self.get_label_line(label, script_name))