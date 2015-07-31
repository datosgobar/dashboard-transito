#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import os
# http://stackoverflow.com/questions/372885/how-do-i-connect-to-a-mysql-database-in-python

#OPENSHIFT_MYSQL_DB_LOG_DIR=/var/lib/openshift/55bbc87dca988e695100000e/app-root/logs

if os.environ.get('OPENSHIFT_MYSQL_DIR'):
	host = os.environ.get('OPENSHIFT_MYSQL_DB_HOST')
	port = os.environ.get('OPENSHIFT_MYSQL_DB_PORT')
	user = os.environ.get('OPENSHIFT_MYSQL_DB_USERNAME')
	pwd = os.environ.get('OPENSHIFT_MYSQL_DB_PASSWORD')
	db = MySQLdb.connect(host=host, user=user, passwd=pwd, db="dashboardoperativo")
else:
    db = MySQLdb.connect(host="localhost", user="root", db="dashboardoperativo")


def readSegmentos(**args):
	"""
		readSegmentos(sub_seg_id="")
	"""
	cur = db.cursor()
	result = []
	try:
		cur.execute("SELECT * FROM infosegmentos")
		for row in cur.fetchall():
    		result.append(row[0])
	except:
		result = []

	return result


db.disconnect()