#!/usr/bin/env python
# -*- coding:utf-8 -*-  

__author__ = 'r0ker'
import urllib
import urllib2
import json
import time
import os
import smtplib
import email.mime.text
from collections import OrderedDict
from config import mail_host, mail_port, mail_password, mail_username


def sendmail(to_addrs, title, text):
	from_addr = mail_username
	smtp = smtplib.SMTP()
	smtp.set_debuglevel(1)
	smtp.starttls()
	smtp.login(mail_username, mail_password)
	msg = email.mime.text.MIMEText(text, 'html', 'utf-8')
	msg['From'] = from_addr
	msg['To'] = to_addrs
	msg['Subject'] = title
	smtp.sendmail(from_addr, to_addrs, msg.as_string())
	smtp.quit()


def urljson(data):
	return json.loads(urlde(data))


def timede(t):
	return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))


def urlde(str):
	str = str.encode('utf-8')
	return urllib.unquote(str)


def urlen(str):
	str = str.encode('utf-8')
	return urllib.quote(str).replace("%", "%%")


def md5(str):
	import hashlib
	m = hashlib.md5()
	m.update(str)
	return m.hexdigest()


def getaddr(ip):
	url = 'http://ip.taobao.com/service/getIpInfo.php?ip='+ip
	req = urllib2.Request(url)
	res_data = json.loads(urllib2.urlopen(req).read())
	return '-'.join((res_data['data']['country'],res_data['data']['region'],res_data['data']['city'],res_data['data']['county'],res_data['data']['isp']))

def systeminfo():
	x = {}
	''' Return the information in /proc/meminfo
	as a dictionary '''
	meminfo = OrderedDict()

	with open('/proc/meminfo') as f:
		for line in f:
			meminfo[line.split(':')[0]] = line.split(':')[1].strip()
	total=float(meminfo['MemTotal'][:-3])
	use=total-float(meminfo['MemFree'][:-3])
	disk = os.statvfs("/")
	dtotal = float(disk.f_bsize * disk.f_blocks)
	duse= float(disk.f_bsize * disk.f_blocks-disk.f_bsize * disk.f_bfree)
	x['u'] = float('%.1f' % (use/total*100))
	x['use'] = int(use/1024.0)
	x['total'] = int(total/1024.0)
	x['du'] = float('%.1f' % (duse/dtotal*100))
	x['duse'] = float('%.1f' % (duse/1024.0/1024.0/1024.0))
	x['dtotal'] = float('%.1f' % (dtotal/1024.0/1024.0/1024.0))
	return x

