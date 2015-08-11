#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'r0ker'

from sockjs.tornado.transports import base
from sockjs.tornado import conn, session
import db
import json


class SockConnection(conn.SockJSConnection):
	participants = set()
		
	def on_open(self, info):
		username = base.BaseTransportMixin.sock_cookies
		row = db.ct("manager", "*", "username='"+username+"'")
		if row:
			self.name = 'manager'
		else:
			hostip = base.BaseTransportMixin.sock_headers['Remote-Ip']
			hostid = db.ct('host', 'id', "hostip='"+hostip+"' order by id desc limit 1")['id']
			db.u("host", "online=1", "id="+str(hostid))
			self.name = hostip
		self.participants.add(self)



	def on_message(self, message):
		if self.name == 'manager':
			message = json.loads(message)
			self.broadcast(filter(lambda x:x.name == message['hostip'], self.participants), message['msg'])
		else:
			self.broadcast(filter(lambda x:x.name == 'manager', self.participants), message)

	def on_close(self):
		self.participants.remove(self)
		if self.name != 'manager':
			hostip = base.BaseTransportMixin.sock_headers['Remote-Ip']
			hostid = db.ct('host', 'id', "hostip='"+ip+"' order by id desc limit 1")['id']
			db.u("host", "online=0", "id="+str(hostid))

