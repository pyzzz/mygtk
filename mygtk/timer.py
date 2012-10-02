#!/usr/bin/env python
# -*- coding:utf-8 -*-
import gobject

def idle_add(*args):
	return gobject.idle_add(*args)

def timeout_add(*args):
	return gobject.timeout_add(*args)

def idle_del(*args):
	return gobject.source_remove(*args)

def timeout_del(*args):
	return gobject.source_remove(*args)

def timeout_list_append(timeout_list, *args):
	timeout_list.append(timeout_add(*args))

def timeout_list_clear(timeout_list):
	while timeout_list:
		timeout_del(timeout_list.pop())
