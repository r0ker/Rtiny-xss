#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'r0ker'
import tornado.web
import db
import json
from config import URL
from base import BaseHandler
from function import urlde, timede, urljson, systeminfo


class HostHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self, projectid, ip, page, do):
		def getname(id):
			return urlde(db.ct("project","name","id="+id)['name'])
		if ip and projectid:
			num = db.c('host', "hostip='"+ip+"' and projectid='"+projectid+"'")
			if num:
				page = str(page and (int(page)-1>0 and (int(page)-1<num and int(page)-1 or 0) or 0) or 0)
				host = db.ct(
					"host",
					"*",
					"hostip = '"+ip+"' and projectid='"+projectid+"' order by id desc limit "+page+",1")
				if do == 'del':
					db.d("host", "id="+str(host['id']))
					if num == 1:
						hostlist = json.loads(db.ct("project", "hosts", "id="+projectid)['hosts'])
						hostlist.remove(ip)
						db.u("project", "hosts='"+json.dumps(hostlist)+"'", "id="+projectid)
						self.redirect("http://"+URL+"/project/"+projectid)
					self.redirect("http://"+URL+"/host/"+projectid+"/"+ip)
				else:
					self.render(
						"host.html",
						heads=[
							{'name':getname(projectid), 'title': 'Go to ' + getname(projectid),
								'url': 'project/'+projectid},
						{'name': ip, 'title': '', 'url': ''},
						],
						username=self.get_secure_cookie("username"),
						datainfo=db.datainfo(),
						systeminfo=systeminfo(),
						urlde=urlde,
						timede=timede,
						url=URL,
						urljson=urljson,
						host=host,
						num=range(num),
						page=int(page)+1,
						)
			else:
				self.render('404.html')
		else:
			self.render('404.html')
