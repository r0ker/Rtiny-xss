#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'r0ker'
import tornado.web
import db
import time
from config import URL
from base import BaseHandler
from function import urlde, timede, urlen, systeminfo


class ModuleHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self, id, do):
		if id:
			row = db.ct("module", "*", "id="+id)
			if row:
				if do == 'del':
					db.d("module", "id="+id)
					self.redirect("http://"+URL+"/module")
				else:
					self.render(
						'module_edit.html',
						username=self.get_secure_cookie("username"),
						datainfo=db.datainfo(),
						systeminfo=systeminfo(),
						heads=[ 
							{'name':'Module', 'title':'Module list', 'url':'module/'},
							{'name':urlde(row['name']), 'title': '', 'url': ''},
						],
						row=row,
						url=URL,
						urlde=urlde,
						)
			else:
				self.render('404.html')
		else:
			if do == 'add':
				self.render(
					'module_add.html',
					username=self.get_secure_cookie("username"),
					datainfo=db.datainfo(),
					systeminfo=systeminfo(),
					heads=[{'name':'Module', 'title':'Module list', 'url':'module/'},{'name':'Add', 'title':'', 'url':''}],
					url=URL,
					urlde=urlde,
					)
			else:
				mrows = db.cts("module", "*", "1=1 order by id")
				modulen = len(mrows)
				self.render(
					"module.html",
					username=self.get_secure_cookie("username"),
					datainfo=db.datainfo(),
					systeminfo=systeminfo(),
					heads=[{'name':'Module', 'title': '', 'url': ''}],
					url=URL,
					urlde=urlde,
					timede=timede,
					mrows=mrows,
					modulen=modulen,
					)

	@tornado.web.authenticated
	def post(self, id, do):
		if id:
			row=db.ct("module", "*", "id="+id)
			if row:
				description = urlen(self.get_argument('description', 'None'))
				name = urlen(self.get_argument('name', 'None'))
				code = urlen(self.get_argument('code', 'None'))
				addtime = int(time.time())
				db.u(
					"module",
					"description='"+description+"',name='"+name+"',code='"+code+"',addtime="+str(addtime), "id="+id)
				self.redirect("http://"+URL+"/module")
			else:
				self.render('404.html')
		else:
			if do == 'add':
				description = urlen(self.get_argument('description', 'None'))
				name = urlen(self.get_argument('name', 'None'))
				code = urlen(self.get_argument('code', 'None'))
				addtime = int(time.time())
				db.i(
					"module",
					"description,name,code,addtime",
					"'"+description+"','"+name+"','"+code+"','"+str(addtime)+"'")
				self.redirect("http://"+URL+"/module")
			elif do == 'del':
				db.d("module", "id in ("+self.get_argument('id')+")")
			else:
				self.render('404.html')