#!/usr/bin/env python
# -*- coding:utf-8 -*-  

__author__ = 'r0ker'
from base import BaseHandler
import os


class SwfHandler(BaseHandler):
	def set_default_headers(self):
		self.set_header ('Content-Type', 'application/x-shockwave-flash')
	def get(self):
		file =  os.path.join(os.path.dirname(__file__), "../swf.swf")
		with open(file, 'r') as f:
			while True:
				data = f.read()
				if not data:
					break
				self.write(data)
		self.finish()