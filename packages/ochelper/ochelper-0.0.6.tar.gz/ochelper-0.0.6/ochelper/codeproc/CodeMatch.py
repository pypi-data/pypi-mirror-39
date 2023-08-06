#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import re

class CodeMatch:

	'匹配OC 代码的类'
	
	def __init__(self, name):
		self.name = name

		self.category_name = []
		self.class_name = []
		self.method_name = []
		self.property_name = []

	def getMatchCodeFile(self):
		# 打开文件
		fo = open(self.name, "r")
		for line in fo.readlines():
			class_name_match = re.match( r'^@implementation', line)
			if class_name_match:
				class_name_pattern = re.compile(r'^@implementation[ 	]*([A-Za-z0-9_]*)[ 	]*\(?.*')
				self.class_name = self.class_name  + class_name_pattern.findall(line) or []

				# category
				category_name_match = re.match(r'^@implementation[ 	]*.*\(.*\)', line)
				if category_name_match:
					category_name_pattern = re.compile(r'^@implementation[ 	]*[A-Za-z0-9_]*[ 	]*\([ 	]*([A-Za-z0-9_]*)[ 	]*\)')
					self.category_name = category_name_pattern.findall(line) or []

			method_name_match = re.match( r'^-[ 	]*\(', line)
			if method_name_match:
				method_name_pattern = re.compile(r'^-[	 ]*(.*)[ ]([A-Za-z0-9_]*)')
				self.method_name = self.method_name + [line]


			property_name_match = re.match(r'^@property', line)
			if property_name_match:
				property_name_pattern = re.compile(r'@property[ 	]*\(.*\)[ 	]*[A-Za-z0-9_]*[ 	\*]*([A-Za-z0-9_]*).*')
				self.property_name = self.property_name + property_name_pattern.findall(line) or []

		fo.close()

	def hasClass(self):
		return len(self.class_name) > 0
		
	def getClassName(self):
		return self.class_name

	def hasCategory(self):
		return len(self.category_name) > 0

	def getCategoryName(self):
		return self.category_name

	def hasMethod(self):
		return len(self.method_name) > 0

	def getMethod(self):
		return self.method_name

	def hasProperty(self):
		return len(self.property_name) > 0

	def getProperty(self):
		return self.property_name
