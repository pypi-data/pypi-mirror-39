#!/usr/bin/python
# -*- coding: UTF-8 -*-
 

import os



#非递归
def search_file_indir_with_ext(dirname, fileExts):

	result = 	[]#所有的文件
	
	items = os.listdir(dirname);

	for i in range(0,len(items)):
		path = os.path.join(dirname, items[i])
		if os.path.isfile(path):
			ext = os.path.splitext(path)[1]
			if ext in fileExts:
				result.append(path)
	return result

#递归
def search_file_recur_indir_with_ext(dirname, fileExts):

    result = []#所有的文件
    for maindir, subdir, file_name_list in os.walk(dirname):
		for filename in file_name_list:
			path = os.path.join(maindir, filename) #合并成一个完整路径
			ext = os.path.splitext(path)[1]  # 获取文件后缀 [0]获取的是除了文件名以外的内容
			if ext in fileExts:
				result.append(path)
    return result


#非递归
def search_dir_indir(dirname):

	result = []#所有的文件

	items = os.listdir(dirname);
	for i in range(0,len(items)):
		path = os.path.join(dirname,items[i])
		if os.path.isdir(path):
			result.append(path)

	return result

