#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import re
from .fileproc.FileProc import *;
from .codeproc.CodeMatch import *;
from .codeproc.CodeWrite import *;
from .codeproc.ObjectiveClass import *;



def ochandler(code_dir, output_dir):
	all_class_names = []
	all_property_names = []
	all_method_names = []

	mfile_list = search_file_recur_indir_with_ext(code_dir, [".m"])
	for filename in mfile_list:
		item = CodeMatch(filename)
		item.getMatchCodeFile()
		if item.hasClass():
			all_class_names = all_class_names + item.getClassName()

		if item.hasMethod():
			all_method_names = all_method_names + item.getMethod()

		if item.hasProperty():
			all_property_names = all_property_names + item.getProperty()

	# print all_class_names
	# print all_property_names

	hfile_list = search_file_recur_indir_with_ext(code_dir, [".h"])
	for filename in hfile_list:
		item = CodeMatch(filename)
		item.getMatchCodeFile()
		if item.hasProperty():
			all_property_names = all_property_names + item.getProperty()




	fCls = open(os.path.join(output_dir, "class_name.txt"), "w+")
	for ele in all_class_names:
		fCls.write(ele + '\n')
	fCls.close()


	fProperty = open(os.path.join(output_dir, "property_name.txt"), "w+")
	for ele in all_property_names:
		property_name_match = re.match( r'^[a-z]*[A-Z]{1}[a-zA-Z]*', ele)
		if property_name_match:
			fProperty.write(ele+ '\n')
	fProperty.close()

