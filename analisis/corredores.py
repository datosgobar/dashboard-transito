#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import os
import time
import random
import config

def createSegmentos():

	db = MySQLdb.connect(host=config.mysql["host"], passwd=config.mysql["password"], user=config.mysql["user"])
	cur = db.cursor()
	cur.execute('DROP DATABASE dashboardoperativo;')
	cur.execute('CREATE DATABASE IF NOT EXISTS dashboardoperativo;')
	cur.close()
	db.select_db("dashboardoperativo")
	
	causas = ["Choque", "Manifestacion", "Animales sueltos"]

	try:
		cur = db.cursor()
		cur.execute("""CREATE TABLE infosegmentos (id INT NOT NULL, PRIMARY KEY(id), timestamp_medicion TIMESTAMP, tiempo INT, \
		velocidad FLOAT,causa TEXT,causa_id INT,duracion_anomalia INT,indicador_anomalia FLOAT,anomalia INT);""")
		cur.close()
	except Exception, ex:
		return ex
	else:
		cur = db.cursor()
		for ID in range(10, 58):
			cur.execute("""INSERT INTO infosegmentos VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",  \
				(ID, time.strftime('%Y-%m-%d %H:%M:%S'), random.randrange(5, 21), \
					random.randrange(0, 101), causas[random.randrange(0, 3)], random.randrange(0, 21), random.randrange(1, 120), \
					random.random(), random.randrange(0, 4)))
			print "Auto Increment ID: %s" % ID
	finally:
  		cur.close()
		db.close()

def readSegmentos():
	"""
		readSegmentos()
	"""
	result = []

	try:
		db = MySQLdb.connect(host=config.mysql["host"], passwd=config.mysql["password"], user=config.mysql["user"])
		db.select_db("dashboardoperativo")
		cur = db.cursor()
	except:
		result = []
	else:
		cur.execute("SELECT * FROM infosegmentos")
		for row in cur.fetchall():
			result.append(row)
	finally:
			cur.close()
			db.close()
			return result

	
def buildSegmentos(data):
	return {
		"id": int(data[0]),
		"timestamp_medicion": str(data[1]),
		"tiempo": int(data[2]),
		"velocidad": int(data[3]),
		"causa" : str(data[4]),
		"causa_id" : int(data[5]),
		"duracion_anomalia": int(data[6]),
		"indicador_anomalia": float(data[7]),
		"anomalia" : int(data[8])
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
		"centro" : [10, 12, 57, 53, 51, 49, 40, 43, 37, 36, 21, 31, 33, 35, 13, 14, 18, 17, 23, \
		24, 25, 26, 28, 30, 32, 45, 47, 38, 44],
		"provincia" : [11, 56, 54, 55, 41, 22, 16, 15, 19, 20, 10, 27, 29, 34, 39, 42, 46, 50 ,52, 48]
	}

	update = readSegmentos()

	if len(update):
		for i in range(len(update)):
			for corredor, segmentosids in corredores.iteritems():
				if update[i][0] in segmentosids:
					if update[i][0] in referencia['centro']:
						#print update[i][0], c, 'centro'
						template['corredores'][corredor]['segmentos_capital'].append(buildSegmentos(update[i]))
					else:
						#print update[i][0], c, 'prov'
						template['corredores'][corredor]['segmentos_provincia'].append(buildSegmentos(update[i]))
				else:
					continue

		for channell in corredores.keys():
		  self.emit(channell, template['corredores'][channell])
		  time.sleep(0.5)
	else:
		self.emit('info', "sin datos")


if __name__ == '__main__':

	createSegmentos()