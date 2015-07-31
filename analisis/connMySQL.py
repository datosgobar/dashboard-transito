#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import os
import time
import random
# OPENSHIFT_MYSQL_DB_LOG_DIR=/var/lib/openshift/55bbc87dca988e695100000e/app-root/logs
# http://stackoverflow.com/questions/372885/how-do-i-connect-to-a-mysql-database-in-python


if os.environ.get('OPENSHIFT_MYSQL_DIR'):
	host = os.environ.get('OPENSHIFT_MYSQL_DB_HOST')
	port = os.environ.get('OPENSHIFT_MYSQL_DB_PORT')
	user = os.environ.get('OPENSHIFT_MYSQL_DB_USERNAME')
	pwd = os.environ.get('OPENSHIFT_MYSQL_DB_PASSWORD')
	db = MySQLdb.connect(host=host, user=user, passwd=pwd, db="dashboardoperativo")
else:
    db = MySQLdb.connect(host="localhost", user="root", db="dashboardoperativo")


def createSegmentos():
	cur = db.cursor()
	try:
		cur.execute("""CREATE TABLE infosegmentos2 (id INT NOT NULL, PRIMARY KEY(id), timestamp_medicion TIMESTAMP, tiempo INT, \
		velocidad FLOAT,causa TEXT,causa_id INT,duracion_anomalia INT,indicador_anomalia FLOAT,anomalia INT);""")
	except Exception, ex:
		return ex
	else:
		cur = db.cursor()
		#"anomalia","timestamp_medicion","tiempo","velocidad","causa","duracion_anomalia","indicador_anomalia","id"
		for ID in range(1, 58):
			cur.execute("""INSERT INTO infosegmentos2 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",  \
				(ID, time.time(), random.randrange(2, 10), random.random(), "algo sucedio", random.randrange(2, 3), \
					random.randrange(1, 50), random.random(), random.randrange(2, 15)))
			print "Auto Increment ID: %s" % ID
	except:
		pass

def readSegmentos():
	"""
		readSegmentos()
	"""
	cur = db.cursor()
	result = []
	try:
		cur.execute("SELECT * FROM infosegmentos2")
		for row in cur.fetchall():
    		result.append(row)
	except:
		result = []

	db.disconnect()
	return result

