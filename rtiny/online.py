#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'r0ker'

import tornado.web
from base import BaseHandler
import db
import json
from config import URL
import time
from function import urlde, timede, urljson, getaddr, systeminfo


class OnlineHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		def gethostn(hostip):
			return db.c("host", "hostip='"+hostip+"'")

		def getname(id):
			return urlde(db.ct("project", "name", "id="+str(id))['name'])
		rows = db.cts("host", "hostip", "online=1")
		row = []
		for x in rows:
			row.append(db.ct("host", "*", "hostip='"+x['hostip']+"' order by id desc limit 1"))
		self.render(
			"online.html",
			heads=[
				{'name':'Online', 'title':'', 'url':''},
			],
			username=self.get_secure_cookie("username"),
			datainfo=db.datainfo(),
			systeminfo=systeminfo(),
			urlde=urlde,
			url=URL,
			timede=timede,
			urljson=urljson,
			getaddr=getaddr,
			row=row,
			getname=getname,
			gethostn=gethostn,
		)
			