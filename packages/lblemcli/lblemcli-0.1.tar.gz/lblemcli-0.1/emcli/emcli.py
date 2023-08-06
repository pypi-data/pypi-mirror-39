#!/bin/python3
#_*_ coding: UTF-8 _*_
from __future__ import print_function
import os
import sys

try:
	import ConfigParser
except ImportError:
	import configparser as ConfigParser

import argparse
import yagmail

from emcli.storage import Storage
from emcli.logger import get_logger

logger = get_logger()

def get_argparse():
	parser = argparse.ArgumentParser(description='A email client in terminal')
	parser.add_argument('-s', action='store', dest='subject', required=True, help='specify a subject (must be in quotes if it has spaces)')
	parser.add_argument('-a', action='store', nargs='*', dest='attaches', required=False, help='attach file(s) to the message')
	parser.add_argument('-f', action='store', dest='conf', required=False, help='specify an alternate .emcli.cnf file')
	parser.add_argument('-r', action='store', nargs='*',dest='recipients', required=True, help='recipient who you are sending the email to')
	parser.add_argument('-v', action='version', version='%(prog)s 0.2')
	return parser.parse_args()

def get_config_file(config_file):
	if config_file is None:
		config_file = os.path.expanduser('~/.emcli.cnf')
	return config_file

def get_meta_from_config(config_file):
	#config = ConfigParser.SafeConfigParser()
	config = ConfigParser.ConfigParser()
	with open(config_file) as fp:
		config.read_file(fp)
		
	meta = Storage()
	print(type(meta))
	for key in ['smtp_server', 'smtp_port', 'username', 'password']:
		try:
			val = config.get('DEFAULT', key)
		except (ConfigParser.NoSectionError, ConfigParser.NoOptionError) as err:
			logger.error(err)
			raise SystemExit(err)
		else:
			meta[key] = val
	
	return meta

def get_email_content():
	#输入内容后,以ctrl+c结束输入
	print('请自动输入邮件内容,以 ctrl+d 结束,如果以 echo "This email come from terminal" | /usr/local/python/bin/emcli -s "This is subject" -r libinglin@126.com 或 /usr/local/python/bin/emcli -s "This is subject" -a *.py -r libinglin@126.com < /etc/passwd方式调用则不用手动输入:')
	return sys.stdin.read()

#可以不用运行main()而独立调用send_email(meta)函数发邮件,不过要传一个dict类型的meta,这个dict的形为 {'smtp_server': 'smtp.126.com', 'smtp_port': '994', 'username': 'libinglin@126.com', 'password': '834312lBl', 'subject': 'This is subject', 'recipients': ['libinglin@126.com'], 'attaches': ['important.jpg']}
#直接调用的办法
#import emcli
#meta = {'smtp_server': 'smtp.126.com', 'smtp_port': '994', 'username': 'libinglin@126.com', 'password': '834312lBl', 'subject': 'This is subject', 'recipients': ['libinglin@126.com'], 'attaches: ['important.jpg']} 
#emcli.send_email(meta)
def send_email(meta):
	content = get_email_content()
	#content = "this is body, my body"
	body = [content]
	if 'attaches' in meta.keys():
		body.extend(meta['attaches'])
	#with yagmail.SMTP(user=meta.username, password=meta.password, host=meta.smtp_server, port=int(meta.smtp_port)) as yag:
	#	logger.info('ready to send email "{0}" to {1}'.format(meta.subject, meta.recipients))
	#	ret = yag.send(meta.recipients, meta.subject, body)
	with yagmail.SMTP(user=meta['username'], password=meta['password'], host=meta['smtp_server'], port=int(meta['smtp_port'])) as yag:
		logger.info('ready to send email "{0}" to {1}'.format(meta['subject'], meta['recipients']))
		ret = yag.send(meta['recipients'], meta['subject'], body)
		
def main():
	#https://github.com/lalor/emcli/
	#获得命令行参数,如果不用-a指定附件的参数,则attaches=None
	print("into main")
	parser = get_argparse()
	config_file = get_config_file(parser.conf)
	if not os.path.exists(config_file):
		logger.error('{0} is not exists'.format(config_file))
		raise SystemExit()
	else:
		#获得配置文件中的参数
		meta = get_meta_from_config(config_file)
	
	meta.subject = parser.subject
	meta.recipients = parser.recipients
	if  parser.attaches:
		meta.attaches = parser.attaches
		for attach in meta.attaches:
			if not os.path.exists(attach):
				logger.error('{0} is not exists'.format(attach))
				raise SystemExit()
	
	print(meta)
	send_email(meta)

"""def main():
	meta = {'smtp_server': 'smtp.126.com', 'smtp_port': '994', 'username': 'libinglin@126.com', 'password': '834312lBl', 'subject': 'This is subject', 'recipients': ['libinglin@126.com'], 'attaches': ['important.jpg']}
	print("here")
	send_email(meta)"""


if __name__ == '__main__':
	main()
