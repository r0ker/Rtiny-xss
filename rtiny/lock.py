#!/usr/bin/env python
# -*- coding:utf-8 -*-  

__author__ = 'r0ker'
import tornado.web
from function import md5
import db
from config import URL


class LockHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_secure_cookie("lock",'1')
		self.render("lock.html")

	def post(self):
		username = self.get_secure_cookie("username") or ''
		passwd = md5(self.get_argument('password', ''))
		row = db.ct("manager", "*", "username='" + username + "' and password='" + passwd + "'")
		if row:
			self.set_secure_cookie("lock", "0")
			self.redirect("http://" + URL)
		else:
			self.redirect("http://" + URL + "/lock")