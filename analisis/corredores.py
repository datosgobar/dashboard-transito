#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import os
import time
import random


if os.environ.get('OPENSHIFT_MYSQL_DIR'):
	host = os.environ.get('OPENSHIFT_MYSQL_DB_HOST')
	port = os.environ.get('OPENSHIFT_MYSQL_DB_PORT')
	user = os.environ.get('OPENSHIFT_MYSQL_DB_USERNAME')
	pwd = os.environ.get('OPENSHIFT_MYSQL_DB_PASSWORD')
	db = MySQLdb.connect(host=host, user=user, passwd=pwd, db="dashboardoperativo")
else:
	db = MySQLdb.connect(host="127.0.0.1", user="root")
	cur = db.cursor()
	cur.execute('CREATE DATABASE IF NOT EXISTS dashboardoperativo;')
	cur.close()
	db.select_db("dashboardoperativo")

def createSegmentos():
	try:
		cur = db.cursor()
		cur.execute("""CREATE TABLE infosegmentos2 (id INT NOT NULL, PRIMARY KEY(id), timestamp_medicion TIMESTAMP, tiempo INT, \
		velocidad FLOAT,causa TEXT,causa_id INT,duracion_anomalia INT,indicador_anomalia FLOAT,anomalia INT);""")
		cur.close()
	except Exception, ex:
		return ex
	else:
		cur = db.cursor()
		for ID in range(10, 58):
			cur.execute("""INSERT INTO infosegmentos2 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",  \
				(ID, time.time(), random.randrange(2, 10), random.random(), "algo sucedio", random.randrange(2, 3), \
					random.randrange(1, 50), random.random(), random.randrange(2, 15)))
			print "Auto Increment ID: %s" % ID
	finally:
		db.close()
		#db.commit()
  		cur.close()

def readSegmentos():
	"""
		readSegmentos()
	"""
	result = []

	try:
		cur = db.cursor()
	except:
		result = []
	else:
		cur.execute("SELECT * FROM infosegmentos2")
		for row in cur.fetchall():
			result.append(row)
	finally:
       	#cur.close()
        #db.close()
		return result

	
def buildSegmentos(data):
	return {
		"id": data[0],
		"anomalia" : data[1],
		"timestamp_medicion": data[2],
		"tiempo": data[3],
		"velocidad": data[4],
		"causa" : data[5],
		"duracion_anomalia": data[6],
		"indicador_anomalia": data[7]
	}

def parserEmitData(self, template):
	"""
		buildCorredores(corredores=corredores, template=template, update=result)
		evaluar si el segmentos corresponde a un corredor y si ese mismo es para prov o capi
	"""

	corredores = {
	 '9_de_julio': [13, 14, 15, 16, 17, 18, 19, 20],
	 'Illia': [11],
	 'alcorta': [54, 55],
	 'alem': [21, 22],
	 'av_de_mayo': [25],
	 'cabildo': [41, 42, 44, 45],
	 'cordoba': [36, 37, 38],
	 'corrientes': [23],
	 'independencia': [10],
	 'juan_b_justo': [30, 31, 32, 33, 34, 35],
	 'libertador': [48, 49, 50, 51, 52, 53],
	 'paseo_colon': [39],
	 'pueyrredon': [46, 47],
	 'rivadavia': [24],
	 'san_martin': [26, 27, 28, 29]
	}

	referencia  = {
		"centro" : [10,12,57, 53,51,49, 40, 43, 37,36, 21, 31,33,35, 13,14, 18,17,23, \
		24,25, 26,28, 30,32 ,45, 47, 38, 44, 48,48],
		"provincia" : [11,56, 54,55, 41, 22, 16,15, 19, 20, 10, 27,29, 34, 39, 42, 46, 50 ,52]
	}

	update = readSegmentos()

	if len(update):
		for i in range(len(update)):
			for corredor, segmentosids in corredores.iteritems():
				if update[i][0] in segmentosids:
					if update[i][0] in referencia['centro']:
						#print update[i][0], c, 'centro'
						template['corredores'][corredor]['segmentos'].append({"id": \
							update[i][0], "capital": buildSegmentos(update[i])})
					else:
						#print update[i][0], c, 'prov'
						template['corredores'][corredor]['segmentos'].append({"id": \
							update[i][0], "provincia": buildSegmentos(update[i])})
				else:
					continue

		for channell in corredores.keys():
		  self.emit(channell, template['corredores'][channell])
		  time.sleep(0.5)
	else:
		self.emit('info', "sin datos")


if __name__ == '__main__':

	createSegmentos()
