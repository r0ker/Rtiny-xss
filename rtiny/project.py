#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'r0ker'
import tornado.web
from base import BaseHandler
import db
import json
import re
from config import URL
import time
from function import urlde, timede, urlen, urljson, getaddr, systeminfo


class ProjectHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self, id, do):
		def gethostn(hostip):
			return db.c("host", "hostip='"+hostip+"'")

		def getmcustom(code):
			code = urlde(code)
			s = re.findall("({set\..*})", code)
			return s
		if id:
			row = db.ct("project", "*", "id="+id)
			if row:
				if do == 'del':
					db.d("project", "id="+id)
					self.redirect("http://"+URL+"/project")
				elif do == 'edit':
					modules = db.cts("module", "*", "1=1")
					pmodules = json.loads(urlde(db.ct("project", "module", "id="+id)['module']))
					self.render(
						"project_edit.html",
						heads=[
							{'name':'Project', 'title':'Project list', 'url':'project'},
							{'name':urlde(row['name']), 'title':urlde(row['name']) + 'view', 'url':'project/'+id},
						],
						username=self.get_secure_cookie("username"),
						datainfo=db.datainfo(),
						systeminfo=systeminfo(),
						urlde=urlde,
						getmcustom=getmcustom,
						row=row,
						url=URL,
						modules=modules,
						pmodules=pmodules,
						)
				else:
					x = []
					hosts = []
					hostlist = json.loads(db.ct("project", "hosts", "id="+id)['hosts'])
					hostn = 0
					if hostlist:
						for i in hostlist:
							x.append(db.ct(
								"host", "id", "hostip='"+i+"' and projectid="+id+" order by id desc limit 1")['id'])
						x.sort(reverse=True)
						hostn = len(x)
						for i in x:
							hosts.append(db.ct(
								"host", "hostip,information,online,addtime,projectid,id", "id="+str(i)))
					self.render(
						"project_select.html",
						heads=[
							{'name':'Project', 'title':'Project list', 'url':'project'},
							{'name':urlde(row['name']), 'title':'', 'url':''},
						],
						username=self.get_secure_cookie("username"),
						datainfo=db.datainfo(),
						systeminfo=systeminfo(),
						urlde=urlde,
						hostn=hostn,
						hosts=hosts,
						gethostn=gethostn,
						url=URL,
						timede=timede,
						urljson=urljson,
						getaddr=getaddr,
						)
			else:
				self.render('404.html')
		else:
			if do == 'add':
				modules = db.cts("module", "*", "1=1")
				self.render(
					"project_add.html",
					heads=[
						{'name': 'Project', 'title': 'Project list', 'url': 'project'},
						{'name': 'Add', 'title': '', 'url': ''},
					],
					username=self.get_secure_cookie("username"),
					datainfo=db.datainfo(),
					systeminfo=systeminfo(),
					url=URL,
					urlde=urlde,
					modules=modules,
					getmcustom=getmcustom,
					)
			else:
				prows = db.cts("project", "*", "1=1 order by id")                #所有的project
				hrown = {}                                                  #host数目
				hrowno = {}                 #host online 数目
				if prows:
					for i in prows:
						hrown[i['id']] = db.c("host", "projectid="+str(i['id']))
						hrowno[i['id']] = db.c("host", "projectid="+str(i['id'])+" and online=1")
				self.render(
					"project.html",
					heads=[{'name': 'Project', 'title': '', 'url':''}],
					prows=prows,
					prown=len(prows),
					hrown=hrown,
					hrowno=hrowno,
					username=self.get_secure_cookie("username"),
					datainfo=db.datainfo(),
					systeminfo=systeminfo(),
					url=URL,
					urlde=urlde,
					timede=timede,
					)

	@tornado.web.authenticated
	def post(self, id, do):
		if id:
			if do == 'del':
				hostip = self.get_argument('hostip').split(',')
				hostlist = json.loads(db.ct("project","hosts","id="+id)['hosts'])
				for x in hostip:
					hostlist.remove(x)
					hostips = "'"+x+"',"
				db.u("project", "hosts='"+json.dumps(hostlist)+"'", "id="+id)
				db.d("host", "hostip in ("+hostips[:-1]+") and projectid="+id)
			else:
				row = db.ct("project", "*", "id="+id)
				if row:
					post_data = {}
					for key in self.request.arguments:
						post_data[key] = self.get_arguments(key)
					i = 0
					module = {}
					if 'moduleid' in post_data:
						for key in post_data['moduleid']:
							module[key] = urlen(post_data['modulecustom'][i])
							i += 1
						module = json.dumps(module)
					else:
						module = '[]'
					addtime = int(time.time())
					db.u(
						"project",
						"name='"+urlen(post_data['name'][0])+"',description='"+urlen(post_data['description'][0])+"',email='"+post_data['email'][0]+
						"',custom='"+urlen(post_data['custom'][0])+"',fip='"+post_data['fip'][0]+"',furl='"+post_data['furl'][0]+"',status='"+post_data['status'][0]+
						"',module='"+module+"',addtime="+str(addtime), "id="+id)
					self.redirect("http://"+URL+"/project")
				else:
					self.render('404.html')
		else:
			if do == 'add':
				post_data = {}
				for key in self.request.arguments:
					post_data[key] = self.get_arguments(key)
				i = 0
				module = {}
				if 'moduleid' in post_data:
					for key in post_data['moduleid']:
						module[key]=urlen(post_data['modulecustom'][i])
						i += 1
					module = json.dumps(module)
				else:
					module = '[]'
				addtime = int(time.time())
				db.i(
					"project","name,description,email,custom,fip,furl,status,hosts,module,addtime","'"+urlen(post_data['name'][0])+"','"+
					urlen(post_data['description'][0])+"','"+post_data['email'][0]+"','"+urlen(post_data['custom'][0])+"','"+post_data['fip'][0]+"','"+
					post_data['furl'][0]+"','"+post_data['status'][0]+"','[]','"+module+"','"+str(addtime)+"'")
				self.redirect("http://"+URL+"/project")
			elif do == 'del':
				db.d("project", "id in ("+self.get_argument('id')+")")
