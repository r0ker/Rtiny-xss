#!/usr/bin/env python
# -*- coding:utf-8 -*-  

__author__ = 'r0ker'
import tornado.web
import db
from config import URL, sql
from function import md5


class LoginHandler(tornado.web.RequestHandler):
	def get(self):
		if self.get_secure_cookie("username") and self.get_secure_cookie("password"):
			self.redirect("/")
		else:
			self.render("login.html", url=URL)

	def post(self):
		self.set_header("Content-Type", "text/plain")
		if True not in [f in self.get_argument("email") for f in sql]:
			row = db.ct(
				"manager",
				"*", "username='"+self.get_argument("email")+"' and password='" + md5(self.get_argument('pass'))+"'")
			if row:
				self.set_secure_cookie("username", row['username'])
				self.set_secure_cookie("password", row['password'])
				self.write("true")

			else:
				self.write("false")
		else:
			self.write("false")
