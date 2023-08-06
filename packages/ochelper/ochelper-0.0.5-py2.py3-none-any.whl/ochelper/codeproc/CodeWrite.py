#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
# sys.path.append(os.path.dirname(__file__) +os.sep+'../')
class CodeWrite:
	
	'处理OC 代码的类'
	
	def __init__(self, name):
		self.name = name

	def fileName(self):
		# print  self.name
		return self.name

	def getFirstClassName(self):
		# print "Total Employee %d"
		return self.name

	def displayEmployee(self):
	 	# print "Name : "
		return self.name