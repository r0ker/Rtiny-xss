#!/usr/bin/env python
# -*- coding:utf-8 -*-  

__author__ = 'r0ker'
from base import BaseHandler
import tornado.web
import db
import time
from config import URL
from function import urlde, systeminfo


class MainHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		def getname(id):
			return urlde(db.ct("project","name","id="+id)['name'])
			
		month = time.strftime("%m", time.localtime(time.time()))
		tables = db.cts("host", "projectid,date_format(from_unixtime(addtime),'%%e') as day", "date_format(from_unixtime(addtime),'%%m')='"+month+"'")
		datatable = {}
		for table in tables:
			id = str(table['projectid'])
			if id not in datatable:
				datatable[id] = {}
				i = 1
				while i <= 31:
					datatable[id][i] = 0
					i += 1
			else:
				datatable[id][int(table['day'])] += 1
		x=''
		for data in datatable:
			for day in datatable[data]:
				x = x + '['+str(day)+', '+str(datatable[data][day])+'],'
			x = x[:-1]
			datatable[data] = x
		self.render(
			'home.html',
			username=self.get_secure_cookie("username"),
			datainfo=db.datainfo(),
			systeminfo=systeminfo(),
			heads=[],
			url=URL,
			urlde=urlde,
			datatable=datatable,
			getname = getname,
			)
