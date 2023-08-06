#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
# sys.path.append(os.path.dirname(__file__) +os.sep+'../')
class CodeWrite:
	
	'处理OC 代码的类'
	
	def __init__(self, name):
		print name
		self.name = name

	def fileName(self):
		print  self.name

	def getFirstClassName(self):
		print "Total Employee %d"

	def displayEmployee(self):
	 	print "Name : "