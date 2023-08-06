#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import setuptools

setuptools.setup(
      name="ochelper",
      version="0.0.1",
      author="weishqdevr",
      author_email="weishqdev@gmail.com",
      description="ochelper for objective",
      long_description= "long_description",
      long_description_content_type="text/markdown",
      url="https://github.com/pypa/sampleproject",
      packages=setuptools.find_packages(),
      classifiers=[
            'Operating System :: POSIX',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python :: 2.7',
            "License :: OSI Approved :: MIT License",
      ],
      entry_points = {
            'console_scripts': [
                  'ochelper = ochelper.ochelper:main'
            ]
      }
)
