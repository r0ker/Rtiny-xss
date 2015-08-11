#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'r0ker'
import tornado.web
import db
from config import sql, URL

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		if not self.get_secure_cookie("lock") == '1':
			if self.get_secure_cookie("username") and self.get_secure_cookie("password"):
				if True not in [f in self.get_secure_cookie("username") for f in sql]:
					row = db.ct("manager", "password", "username='"+self.get_secure_cookie("username")+"'")
					if row:
						if row['password'] == self.get_secure_cookie("password"):
							return 1
						else:
							self.clear_cookie("username")
							self.clear_cookie("password")
				else:
						self.clear_cookie("username")
						self.clear_cookie("password")
		else:
			self.redirect("http://" + URL + "/lock")

