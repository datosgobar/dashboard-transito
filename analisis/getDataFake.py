#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
import os
import config
import random

from dateutil import parser
import datetime
import urlparse
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

# Schema reflection! Para que las clases esten
# Actualizadas con las migraciones de la DB
Base = automap_base()
# Base = declarative_base()

db_url = config.db_url
engine = create_engine(db_url)

# reflect the tables
Base.prepare(engine, reflect=True)

Historical = Base.classes.historical
Anomaly = Base.classes.anomaly
SegmentSnapshot = Base.classes.segment_snapshot
Causa = Base.classes.causa

session = Session(engine)


def readSegmentos():
    """
            readSegmentos()
    """
    result = []
    try:
        cur = engine.connect()
    except Exception, ex:
        print ex
        result = []
    else:
        segment_snapshot = cur.execute("SELECT * FROM segment_snapshot")
        for row in segment_snapshot.fetchall():
            result.append(row)
    finally:
        cur.commit()
        cur.close()
        return result


def createSegmentos():

    causas = ["Choque", "Manifestacion", "Animales sueltos"]
    cur = engine.connect()
    try:
        for ID in range(10, 58):
            cur.execute("""INSERT INTO segment_snapshot VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (ID, time.strftime('%Y-%m-%d %H:%M:%S'), random.randrange(5, 21),
                            random.randrange(0, 101), causas[random.randrange(0, 3)], random.randrange(
                            0, 21), random.randrange(1, 120),
                            random.random(), random.randrange(0, 4)))
            print "Auto Increment ID: %s" % ID
    except Exception, ex:
        print(ex)
    finally:
        cur.commit()
        cur.close()


def api_sensores_fake(url):

    sensor = urlparse.urlsplit(url).path.split("/")[3]

    dato = {
        "_id": {"$id": "55dca5f7312e783b74c62b9d"},
        "date": datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%dT%H:%M:%S-03:00'),
        "iddevice": sensor,
        "data": random.randrange(100, 1500),
        "id_data_type": 13,
        "migrated": "false"
    }

    res = {
        "codigo": "200",
        "error": [],
        "datos": {
            "id": sensor,
            "date_beg": "nulL",
            "date_end": "null",
            "duration": "null",
            "datatype": "null",
            "count": "null",
            "data": []
        },
        "mensaje": "Operación exitosa"
    }

    res['datos']['data'].append(dato)
    return res


def getData():

    filecorredorfake = os.path.abspath("analisis/corredores_fake.json")
    with open(filecorredorfake) as f:
        output = json.loads(f.read())

    return output


def parserEmitDataFake(self, result):
    """
      funcion que trae los datos de mongo, crea un json y emite al front segun corredor
    """
    corredores = ["independencia", "Illia", "nueve_de_julio", "alem", "corrientes",
                  "rivadavia", "av_de_mayo", "san_martin", "juan_b_justo", "cordoba", "paseo_colon", "cabildo", "pueyrredon", "alcorta", "libertador"]

    if len(result):
        for i in range(len(corredores)):
            self.emit(corredores[i], result['corredores'][
                      i][result['corredores'][i].keys()[0]])
            time.sleep(0.5)
    else:
        self.emit('info', "sin datos")


def updateSegmentos():

    conn = engine.connect()
    trans = conn.begin()
    causas = ["Choque", "Manifestacion", "Animales sueltos"]
    query = """UPDATE segment_snapshot SET timestamp_medicion = %s, tiempo = %s, velocidad = %s, comentario_causa = %s, causa_id = %s, duracion_anomalia = %s, \
  indicador_anomalia =%s, anomalia = %s WHERE id = %s"""

    for ID in range(1, 57):
        # timestamp_medicion, tiempo, velocidad, causa, causa_id,
        # duracion_anomalia, indicador_anomalia, anomalia, id
        update = (time.strftime('%Y-%m-%d %H:%M:%S'), random.randrange(5, 21), random.randrange(0, 101), causas[random.randrange(0, 3)],
                  random.randrange(0, 21), random.randrange(1, 120),
                  random.random(), random.randrange(0, 4), ID)
        print update
        conn.execute(query, update)
    trans.commit()
    conn.close()


if __name__ == '__main__':

    while(True):
        updateSegmentos()
        print("Generando nuevos datos")
        time.sleep(60)
