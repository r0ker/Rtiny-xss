#!/usr/bin/env python
# -*- coding:utf-8 -*-  

__author__ = 'r0ker'
import tornado.web


class ErrorHandler(tornado.web.RequestHandler):
	"""404 page
	"""
	def get(self):
		self.write_error(404)

	def write_error(self, status_code, **kwargs):
		if status_code == 404:
			self.render('404.html')
