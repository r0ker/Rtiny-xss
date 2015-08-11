#!/usr/bin/env python
# -*- coding:utf-8 -*-  

__author__ = 'r0ker'
from base import BaseHandler
import db
from config import URL
from function import urlde, systeminfo


class ConsoleHandler(BaseHandler):
	def get(self, id):
		row = db.ct("host", "*", "id="+id)
		if row:
			if row['online'] == 1:
				self.render(
					'console.html',
					username=self.get_secure_cookie("username"),
					heads=[
						{'name': 'console', 'title': '', 'url': ''},
						{'name': row['hostip'], 'title':'', 'url':''},
					],
					datainfo=db.datainfo(),
					systeminfo=systeminfo(),
					url=URL,
					urlde=urlde,
					hostip=row['hostip']
					)
			else:
				self.set_header('Content-type', 'text/html;charset=utf-8')
				self.write('(⊙ˍ⊙)')
		else:
			self.write(id)
