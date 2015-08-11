#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'r0ker'
from config import mysql_db,mysql_host,mysql_password,mysql_user
import torndb
db = torndb.Connection(mysql_host, mysql_db, mysql_user, mysql_password)


def c(table, where):
	return db.get('select count(*) from '+table+" where "+where)['count(*)']


def ct(table, column, where):
	return db.get("select "+column+" from "+table+" where "+where)


def cts(table, column, where):
	return db.query("select "+column+" from "+table+" where "+where)


def u(table, content, where):
	return db.execute("update "+table+" set "+content+" where "+where)


def i(table, column, content):
	return db.execute("insert into "+table+" ("+column+") values ("+content+")")


def d(table, where):
	return db.execute("delete from "+table+" where "+where)


def datainfo():
	projectn = 0
	modulen = 0
	projects = []
	modules = []
	for project in cts("project", "*", "1=1"):
		projects.append(project)
		projectn += 1
	for module in cts("module", "*", "1=1"):
		modules.append(module)
		modulen += 1
	onlinen = c("host", "online=1")
	x = {
		'projectn': projectn, 'modulen': modulen,
		'projects': projects, 'modules': modules, 'onlinen': onlinen}
	return x
