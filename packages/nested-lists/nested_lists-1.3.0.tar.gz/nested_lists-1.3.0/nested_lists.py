#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dez 18 10:37 2018

@author: Pedro Moura
"""
"""
This is "nester.py" module, which provides print_lists fuction, which
prints lists with or without nested lists
"""

"""
This function requires a positional argument called "some_list",
which is a Python list, even with nested lists.
As result each item inside the list, and its nested lists, is printed
recursively.
"""
def print_lists(some_list, indent=False, level=0):
	for each_item in some_list:
		if isinstance(each_item,list):
			print_lists(each_item, indent, level+1)
		else:
			if indent:
				for tab_stop in range(level):
					print("\t", end='')
			print(each_item)
