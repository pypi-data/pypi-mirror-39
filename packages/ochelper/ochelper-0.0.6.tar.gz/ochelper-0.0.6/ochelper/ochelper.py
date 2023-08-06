#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import os;
import sys;
import argparse;

from .ochandler import ochandler;


project_dir = "/Users/wade/Documents/codingapp/LiteGZ" # 字符串

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help="需要处理的代码路径")
    parser.add_argument('-o', '--out', help="输出的路径")
    args = parser.parse_args()

    project_dir = os.getcwd()
    if args.path != None:
        project_dir = args.path
    print project_dir

    output_dir = os.path.join(os.getcwd(), 'output')
    if args.out != None:
        output_dir = args.out
    print output_dir

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    ochandler(project_dir, output_dir)


if __name__ == "__main__":
    main()
