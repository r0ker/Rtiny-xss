#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'r0ker'

import tornado.ioloop
import tornado.web
import os
import rtiny
import sockjs.tornado
import logging

logging.getLogger().setLevel(logging.DEBUG)

settings = {
	"static_path": os.path.join(os.path.dirname(__file__), "themes/static"),
	"template_path": os.path.join(os.path.dirname(__file__), "themes"),
	"cookie_secret": "M0ehO260Qm2dD/MQFYfczYpUbJoyrkp6qYoI2hRw2jc=",
	"login_url": "/login",
	"debug": True,
}

SockRouter = sockjs.tornado.SockJSRouter(rtiny.sock.SockConnection, r'/sock')
	
application = tornado.web.Application([
	(r"/", rtiny.main.MainHandler),
	(r"/login", rtiny.login.LoginHandler),
	(r"/out", rtiny.out.OutHandler),
	(r"/lock", rtiny.lock.LockHandler),
	(r"/module[/]?(\d{1,4})?[/]?(edit|del|add)?[/]?", rtiny.module.ModuleHandler),
	(r"/project[/]?(\d{1,4})?[/]?(view|edit|del|add)?[/]?", rtiny.project.ProjectHandler),
	(r"/host[/]?(\d{1,3})?[/]?(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})?[/]?(\d{1,3})?[/]?(del)?[/]?", rtiny.host.HostHandler),
	(r"/online", rtiny.online.OnlineHandler),
	(r"/(\d{1,4})(m)?", rtiny.get.GetHandler),
	(r"/swf", rtiny.swf.SwfHandler),
	(r"/console[/](\d{1,5})", rtiny.console.ConsoleHandler),] + SockRouter.urls + [(r".*", rtiny.error.ErrorHandler)], **settings)
	
if __name__ == "__main__":
	application.listen('7753', '127.0.0.1')
	tornado.ioloop.IOLoop.instance().start()
