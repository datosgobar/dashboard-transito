#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import os
import time
import random
from analisis import getDBConnection
import config


def createSegmentos():

    db = MySQLdb.connect(host=config.mysql["host"], passwd=config.mysql[
                         "password"], user=config.mysql["user"])
    cur = db.cursor()
    cur.execute('DROP DATABASE dashboardoperativo;')
    cur.execute('CREATE DATABASE IF NOT EXISTS dashboardoperativo;')
    cur.close()
    db.select_db("dashboardoperativo")

    causas = ["Choque", "Manifestacion", "Animales sueltos"]

    try:
        cur = db.cursor()
        cur.execute("""CREATE TABLE segment_snapshot (id INT NOT NULL, PRIMARY KEY(id), timestamp_medicion TIMESTAMP, tiempo INT, \
		velocidad FLOAT,causa TEXT,causa_id INT,duracion_anomalia INT,indicador_anomalia FLOAT,anomalia INT);""")
        cur.close()
    except Exception, ex:
        return ex
    else:
        cur = db.cursor()
        for ID in range(10, 58):
            cur.execute("""INSERT INTO segment_snapshot VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (ID, time.strftime('%Y-%m-%d %H:%M:%S'), random.randrange(5, 21),
                         random.randrange(0, 101), causas[random.randrange(0, 3)], random.randrange(
                             0, 21), random.randrange(1, 120),
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
        db = MySQLdb.connect(host=config.mysql["host"], passwd=config.mysql[
                             "password"], user=config.mysql["user"])
        db.select_db("dashboardoperativo")
        cur = db.cursor()
    except Exception, ex:
        print ex
        result = []
    else:
        cur.execute("SELECT * FROM segment_snapshot")
        for row in cur.fetchall():
            result.append(row)
    finally:
        cur.close()
        db.close()
        return result


def readSnapshot():
    """
            readSnapshot()
    """
    result = []
    select_table = {}
    try:
        conn = getDBConnection()
    except Exception, ex:
        print ex
        result = []
    else:
        select_table = conn.execute("SELECT * FROM segment_snapshot")
        result = select_table.fetchall()
    finally:
        if hasattr(select_table, "close"):
            select_table.close()
        return result


def buildSegmentos(data):
    return {
        "id": int(data['id']),
        "timestamp_medicion": str(data['timestamp_medicion']),
        "tiempo": int(data['tiempo']),
        "velocidad": int(data['velocidad']),
        "causa": str(data['causa']),
        "causa_id": int(data['causa_id']),
        "duracion_anomalia": int(data['duracion_anomalia']),
        "indicador_anomalia": float(data['indicador_anomalia']),
        "anomalia": int(data['anomalia'])
    }


def parserEmitData(self, template):
    """
            buildCorredores(corredores=corredores, template=template, update=result)
            evaluar si el segmentos corresponde a un corredor y si ese mismo es para prov o capi
    """
    corredores = {
        '9_de_julio': [13,  15, 17, 19],
        '9_de_julio_externo': [14, 16, 18, 20],
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

    referencia = {
        "centro": [10, 12, 57, 53, 51, 49, 40, 43, 37, 36, 21, 31, 33, 35, 13, 14, 18, 17, 23,
                   24, 25, 26, 28, 30, 32, 45, 47, 38, 44],
        "provincia": [11, 56, 54, 55, 41, 22, 16, 15, 19, 20, 10, 27, 29, 34, 39, 42, 46, 50, 52, 48]
    }

    update = readSnapshot()

    if len(update):
        for i in range(len(update)):
            for corredor, segmentosids in corredores.iteritems():
                if update[i][0] in segmentosids:
                    if update[i][0] in referencia['centro']:
                        # print update[i][0], c, 'centro'
                        template['corredores'][corredor][
                            'segmentos_capital'].append(buildSegmentos(update[i]))
                    else:
                        # print update[i][0], c, 'prov'
                        template['corredores'][corredor][
                            'segmentos_provincia'].append(buildSegmentos(update[i]))
                else:
                    continue

        for channell in corredores.keys():
            print channell, template['corredores'][channell]
            self.emit(channell, template['corredores'][channell])
            time.sleep(0.5)
    else:
        print "sin datos"
        self.emit('info', "sin datos")


if __name__ == '__main__':

    with open(os.path.abspath("template.json")) as templatecorredores:
        template_buffer = buffer(templatecorredores.read())
        template = json.loads(template_buffer.__str__())
    parserEmitData(template)
    # createSegmentos()
