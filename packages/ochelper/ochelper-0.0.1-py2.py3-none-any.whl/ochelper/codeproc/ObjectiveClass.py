#!/usr/bin/python
# -*- coding: UTF-8 -*-

class ObjectiveClass:

	'OC 代码的类'
	
	def __init__(self, file_name, class_name):
		self.file_name = name
		self.class_name = class_name
		
		self.category  = None
		self.methods = []
		self.properties= []

	def isCategory(self):
		return self.category != None

	def hasProperties(self):
		return len(self.properties) > 0

	def hasMethods(self):
		return len(self.methods) > 0

	def setCategory(self, category):
		return self.category

	def addMethod(self, method):
		return self.methods.append(method)

	def addProperty(self, property):
		return self.properties.append(property)
