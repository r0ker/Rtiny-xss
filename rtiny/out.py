#!/usr/bin/env python
# -*- coding:utf-8 -*-  

__author__ = 'r0ker'
from base import BaseHandler


class OutHandler(BaseHandler):
	def get(self):
		self.clear_cookie("username")
		self.clear_cookie("password")
		self.redirect("/login")
