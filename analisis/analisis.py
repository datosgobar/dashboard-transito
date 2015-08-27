#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

import pdb
from getDataFake import api_sensores_fake
import config
import json
import requests
import datetime
import dateutil.parser
import multiprocessing
import os
import argparse

import anomalyDetection

detection_params_fn = os.path.dirname(
    os.path.realpath(__file__)) + "/detection_params.json"

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


def getData(url):
    # url
    for i in xrange(3):
        try:
            response = requests.get(url)
            if (response.status_code == 200):
                return response.json()
            else:
                print ("hubo timeout de teracode en {0}".format(url))
                pass
        except requests.exceptions.Timeout:
            print ("hubo timeout del request en {0}".format(url))
            pass
        except:
            return None

    return None


"""
Funcion que arme para bajar datos de la api de teracode
Ej:
sensor_ids = [...] # Sacar de waypoints.py
download_startdate = "2015-07-01T00:00:00-00:00"
download_enddate = "2015-07-12T00:00:01-00:00"
step = datetime.timedelta(days=2)
newdata = downloadData (
    sensor_ids, step, download_startdate, download_enddate, outfn="raw_api_01_11.json")
"""


def downloadData(sensor_ids, step, download_startdate, download_enddate, outfn=None, token="superadmin.", pool_len=48):

    # vsensids = virtsens["id_sensor"].unique()
    urltpl = "https://apisensores.buenosaires.gob.ar/api/data/%s?token=%s&fecha_desde=%s&fecha_hasta=%s"

    # end = dateutil.parser.parse(download_enddate)
    start = download_startdate
    end = download_enddate
    urls = []
    if step > (download_enddate - download_startdate):
        step = download_enddate - download_startdate
    while start < end:
        startdate, enddate = start, start + step
        for sensor_id in sensor_ids:
            # startdate, enddate, sensor_id
            url = urltpl % (sensor_id, token, startdate.strftime(
                "%Y-%m-%dT%H:%M:%S-03:00"), enddate.strftime("%Y-%m-%dT%H:%M:%S-03:00"))
            if not url in urls:
                urls.append(url)
        start += step

    """cambiar funcion map por api_sensores_fake"""
    alldata = map(api_sensores_fake, urls)
    # pool = multiprocessing.Pool(pool_len)
    # alldata = pool.map(getData, urls)
    # pool.close()
    # pool.terminate()
    # pool.join()
    # if outfn != None:
    #     outf = open(outfn, "wb")
    #     json.dump(alldata, outf)
    #     outf.close()

    return alldata


def createDBEngine():
    # engine = sqlalchemy.create_engine("postgres://postgres@/postgres")
    # engine = sqlalchemy.create_engine("sqlite:///analysis.db")

    return create_engine(config.db_url)


def getDBConnection():
    conn = createDBEngine().connect()
    return conn


def setupDB():
    """
    Guarda el enum de causas de una anomalia
    """
    with open('../static/data/causas.json') as causas_data:
        causas = json.load(causas_data)
    for causa in causas['causas']:
        if not session.query(Causa).filter(Causa.id == causa['id']).count():
            session.add(
                Causa(descripcion=causa['descripcion'].encode('utf-8'), id=causa['id']))
            session.commit()


"""
Guarda datos recibidos por parámetro en la tabla "historical"
"""


def updateDB(newdata):
    # "Updating database"
    conn = getDBConnection()
    Session = sessionmaker(bind=conn)
    session = Session()
    newrecords = False
    if len(newdata) > 0:
        try:
            session.bulk_save_objects(newdata)
            session.commit()
            newrecords = True
        except exc.SQLAlchemyError:
            # "Encountered SQLAlchemyError"
            pass

            # for historical in newdata:
            # pushear instancia de Historial a la base
            #    session.add(historical)
            #    session.commit()
            #    newrecords = True

    conn.close()
    return newrecords


"""
Elimina registros con mas de un mes de antiguedad de la tabla "historical"
"""


def removeOldRecords():
    conn = getDBConnection()
    Session = sessionmaker(bind=conn)
    session = Session()

    pass


"""
Filtro los registros para no duplicar datos en la base de datos
"""


def filterDuplicateRecords(data, desde=None, hasta=None):
    # "Removing duplicates"
    conn = getDBConnection()
    # parsear json
    Session = sessionmaker(bind=conn)
    session = Session()
    # loopear por cada corredor
    query = session.query(Historical)
    if desde != None:
        query = query.filter(Historical.timestamp >= desde)
    if hasta != None:
        query = query.filter(Historical.timestamp <= hasta)
    results = query.all()

    prevrecords_unique = []
    for result in results:
        prevrecords_unique.append((result.segment, datetime.datetime.strftime(
            result.timestamp, '%Y-%m-%dT%H:%M:%S-03:00')))

    prevrecords_unique = set(prevrecords_unique)
    filtered_data = []
    for corredor in data:
        if not bool(corredor):
            continue
        if len(corredor["datos"]) == 0:
            continue
        for segmento in corredor["datos"].get("data", []):
            # crear nueva instancia de Historical
            segment = segmento["iddevice"]
            data = segmento["data"]
            timestamp = segmento["date"]

            # timestamp

            if (segment, timestamp) in prevrecords_unique:
                continue

            filtered_data.append(Historical(**{
                "segment": segment,
                "data": data,
                "timestamp": datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S-03:00')
            }))

    return filtered_data


def loadApiDump(fn):
    raw_data = json.load(open(fn))
    filtered_data = filterDuplicateRecords(raw_data)
    has_new_records = updateDB(filtered_data)

"""
Este loop se va a ejecutar con la frecuencia indicada para cada momento del dia.
"""


def executeLoop(desde, hasta, dontdownload=False):
    """
        datetime.datetime.strptime(
            "2015-07-15T18:00:00-00:00"[:-6], '%Y-%m-%dT%H:%M:%S')
        traer los sensores lista de archivo configuracion
        desde = "2015-07-01T00:00:00-00:00"
        hasta = "2015-07-12T00:00:01-00:00"
    """

    sensores = [10, 12, 57, 53, 51, 49, 40, 43, 37, 36, 21, 31, 33, 35, 13, 14, 18, 17, 23,
                24, 25, 26, 28, 30, 32, 45, 47, 38, 44, 48, 48, 11, 56, 54, 55, 41, 22, 16, 15, 19, 20, 10, 27, 29, 34, 39, 42, 46, 50, 52]

    if dontdownload:
        has_new_records = True
    else:
        raw_data = downloadData(
            sensores, datetime.timedelta(days=2), desde, hasta)
        filtered_data = filterDuplicateRecords(raw_data, desde, hasta)
        has_new_records = updateDB(filtered_data)
    if has_new_records:
        performAnomalyAnalysis(hasta)

"""
Esta tabla retorna una lista de tuplas de la forma (id_segment, data, timestamp) con los ultimos registros agregados a la tabla "historical"
"""


def getLastRecords(desde, hasta):
    conn = getDBConnection()
    # sesion
    Session = sessionmaker(bind=conn)
    session = Session()
    # realizando una consulta

    # desde = datetime.datetime.strptime(desde, '%Y-%m-%dT%H:%M:%S-03:00')
    # hasta = datetime.datetime.strptime(hasta, '%Y-%m-%dT%H:%M:%S-03:00')
    # ahora = datetime.datetime.now()
    # desde_cuando = ahora - datetime.timedelta(minutes=20)

    # results = session.query(Historical).filter(Historical.timestamp >
    # desde_cuando  ).all()
    results = session.query(Historical).filter(
        Historical.timestamp > desde).filter(Historical.timestamp < hasta).all()
    last_records = []
    for result in results:
        record = [result.segment, result.data, result.timestamp]
#        record = { "id_segment" : result.segment,
#                    "data" : result.data,
#                    "timestamp" : result.timestamp }
        last_records.append(record)
    conn.close()
    return last_records


"""
Esta tabla retorna una lista de tuplas de la forma (id_segment, data, timestamp) con todos los registros \ agregados a la tabla "historical" en el ultimo mes
"""


def getLastMonthRecords():
    pass

"""
Esta funcion determina los parametros de deteccion de anomalias para cada segmento y los guarda en el archivo detection_params.json
"""


def updateDetectionParams(desde=None, hasta=None):
    if hasta == None:
        hasta = datetime.datetime.now()
    if desde == None:
        desde = hasta - datetime.timedelta(weeks=4)
    # lastmonthrecords =
    # getLastRecords("2015-07-06T15:10:00-03:00","2015-08-06T16:00:00-03:00")
    lastmonthrecords = getLastRecords(desde, hasta)
    newparams = anomalyDetection.computeDetectionParams(lastmonthrecords)
    outf = open(detection_params_fn, "wb")
    outf.write(newparams)
    outf.close()

"""
Esta funcion retorna la data que se va a cargar en la tabla segment_snapshot como una lista de diccionarios.
Recibe:
- Lista de dicts con las anomalias que estan vivas en este momento. Cada elemento sigue la forma de los registros de la tabla anomaly:
{
    "id_segment" : int,
    "timestamp_start" : datetime,
    "timestamp_end" : datetime,
    "comentario_causa" : str,
    "causa_id" : int
}

- Un listado de tuplas de la forma (id_segment, data, timestamp) con los datos de los ultimos 20 minutos

Retorna:
- Una lista con un dict tipo json por cada segmento con su estado updateado para la tabla segment_snapshot.
  Deberia tener la siguiente estructura:
{
    "id" : (id del segmento),
    "timestamp_medicion" : (timestamp de la medicion),
    "tiempo" : (tiempo que toma atravesar el segmento segun la ultima medicion),
    "velocidad" : (distancia del corredor / tiempo),
    "comentario_causa" : (por ahora null, lo modifica la UI),
    "causa_id" : (por ahora null, lo modifica la UI),
    "timestamp_start" : (ts de inicio),
    "timestamp_end" : (ts de fin),
    "indicador_anomalia" : (porcentaje),
    "anomalia" : True/False
}
"""
# TODO: Completar campo "velocidad"


def getCurrentSegmentState(anomalies, lastrecords):
    """
        anomalies index 0 {'comentario_causa': '', 'id_segment': '10', 'timestamp_start': \
            '2015-08-27 13:40:00', 'indicador_anomalia': '9.77', 'timestamp_end': '2015-08-27 13:55:00', \
            'id': '56', 'causa_id': '0'}

        lastrecords index 0 [57, 611, datetime.datetime(2015, 8, 27, 13, 40, 9)]
    """
    pdb.set_trace()
    segments = {}
    for r in lastrecords:
        if not segments.has_key(r[0]) or r[2] > segments[r[0]][2]:
            segments[r[0]] = r

    ad = {a["id_segment"]: a for a in anomalies}

    output = []
    # segments keys dispone de todos los sensores range(0, 57)
    for s in segments.values():
        # s [10, 248, datetime.datetime(2015, 8, 27, 15, 1, 27)]
        duracion_anomalia = 0
        if ad.has_key(s[0]):
            duracion_anomalia = (ad[s[0]][
                "timestamp_end"] - ad[s[0]]["timestamp_start"]).seconds / 60
        if ad.has_key(s[0]):
            anomalia = 1
        else:
            anomalia = 0
        output.append({
            "id": s[0],
            "timestamp_medicion": s[2],
            "tiempo": s[1],
            "velocidad": -1,
            "comentario_causa": ad.get(str(s[0]), {}).get("comentario_causa", ""),
            "causa_id": ad.get(str(s[0]), {}).get("causa_id", 0),
            "duracion_anomalia": duracion_anomalia,
            "indicador_anomalia": ad.get(str(s[0]), {}).get("indicador_anomalia", 0),
            "anomalia": anomalia,
            "anomalia_id": ad.get(str(s[0]), {}).get("id", 0)
        })
    return output

"""
Lee los parametros de deteccion de la tabla detection_params.csv
"""


def getDetectionParams():
    return open(detection_params_fn).read()

"""
Updetea una anomalia prexistente
La entrada de esta funcion es un unico diccionario que identifica a la anomalia y tiene la siguiente forma:
{
    "id_segment" : int,
    "timestamp" : datetime,
    "indicador_anomalia" : float,
}

Salida: Lista de dicts con las anomalias que estan vivas en este momento. Cada elemento es de la forma:
{
    "id_segment" : int,
    "timestamp_start" : datetime,
    "timestamp_end" : datetime,
    "comentario_causa" : str,
    "causa_id" : int
}

Los atributos id_segment y timestamp se usan para determinar si una anomalia ya esta presente en la tabla "anomaly".
Las anomalias candidatas a ser mergeadas son todas aquellas cuyo timestamp_end esta dentro de los ultimos 20 minutos.
Por cada anomalia en newanomalydata (como mucho hay una por segmento) me fijo si hay una anomalia candidata en ese segmento.
- Si la hay seteo el campo timestamp_end de la anomalia candidata con el campo timestamp de la anomalia nueva
- Si no la hay creo una nueva anomalia donde:
    id_segment = timestamp_end = anomalia.id_segment
    timestamp_start = timestamp_end = anomalia.timestamp
    indicador_anomalia = anomalia.indicador_anomalia

En este cuadro a es una anomalia ya cargada y b es un avistamiento de una anomalia

a.start    a.end
|          |           
v          v           
+----------+           
|          |           
+----------+           
        +..........+   
        ^          ^   
        |          |   
        b.ts-20m   b.ts

=>
+------------------+   
|                  |           
+------------------+
^                  ^   
|                  |   
a.start            a.end = b.ts
"""


def upsertAnomalies(newanomalydata):
    """
        newanomalydata index 0 {'timestamp': datetime.datetime(2015, 8, 27, 15, 5), 'isanomaly': True, \
            'id_segment': 37, 'indicador_anomalia': 3.39, 'threshold': 664.5, 'evalfield': 1010}
    """
    # pdb.set_trace()
    conn = getDBConnection()
    Session = sessionmaker(bind=conn)
    session = Session()
    liveanomalies = []
    for a in newanomalydata:
        window_older = a["timestamp"] - datetime.timedelta(minutes=20)
        candidate = session.query(Anomaly).filter(Anomaly.id_segment == a["id_segment"]).filter(
            Anomaly.timestamp_end >= window_older).filter(Anomaly.timestamp_end <= a["timestamp"]).first()
        if candidate:
            candidate.timestamp_end = max(
                a["timestamp"], candidate.timestamp_end)
            candidate.indicador_anomalia = a["indicador_anomalia"]
            curanomaly = {}
            for column in Anomaly.__table__.columns:
                curanomaly[column.name] = str(getattr(candidate, column.name))
            session.add(candidate)
            lastmodified_anomaly = candidate
        else:
            curanomaly = {
                "id_segment": a["id_segment"],
                "timestamp_start": a["timestamp"],
                "timestamp_end": a["timestamp"],
                "indicador_anomalia": a["indicador_anomalia"],
                "comentario_causa": "",
                "causa_id": 0
            }
            new_anomaly = Anomaly(**curanomaly)
            session.add(new_anomaly)
            lastmodified_anomaly = new_anomaly
        session.commit()
        print lastmodified_anomaly.id
        curanomaly['anomalia_id'] = lastmodified_anomaly.id
        liveanomalies.append(curanomaly)
    conn.close()
    return liveanomalies


def updateSnapshot(newstates):
    """
       newstates index 0 
       {'duracion_anomalia': 0, 'tiempo': 755, 'comentario_causa': '', 'indicador_anomalia': 0, 'velocidad': -1, \
        'anomalia': 0, 'timestamp_medicion': datetime.datetime(2015, 8, 27, 15, 32, 10), 'id': 10, 'causa_id': 0}    
    """
    # pdb.set_trace()
    conn = getDBConnection()
    Session = sessionmaker(bind=conn)
    sess = Session()
    for segstate in newstates:
        # print segstate["anomalia_id"]
        curstate = sess.query(SegmentSnapshot).get(segstate["id"])
        if curstate == None:
            curstate = SegmentSnapshot(**segstate)
        else:
            for (k, v) in segstate.items():
                setattr(curstate, k, v)
        sess.add(curstate)
        sess.flush()

    sess.commit()
    conn.close()


def performAnomalyAnalysis(ahora=None):
    if ahora == None:
        ahora = datetime.datetime.now()
    lastrecords = getLastRecords(ahora - datetime.timedelta(minutes=20), ahora)
    detectparams = getDetectionParams()
    anomalies = anomalyDetection.detectAnomalies(detectparams, lastrecords)
    curanomalies = upsertAnomalies(anomalies)
    curstate = getCurrentSegmentState(curanomalies, lastrecords)
    updateSnapshot(curstate)


def downloadAndLoadLastMonth():

    sensores = [10, 12, 57, 53, 51, 49, 40, 43, 37, 36, 21, 31, 33, 35, 13, 14, 18, 17, 23, 24, 25, 26, 28, 30,
                32, 45, 47, 38, 44, 48, 48, 11, 56, 54, 55, 41, 22, 16, 15, 19, 20, 10,
                27, 29, 34, 39, 42, 46, 50, 52]

    hasta = datetime.datetime.now()
    desde = hasta - datetime.timedelta(days=28)
    raw_data = downloadData(
        sensores, datetime.timedelta(days=2), desde, hasta, pool_len=len(sensores))
    # print raw_data
    filtered_data = filterDuplicateRecords(raw_data, desde, hasta)
    has_new_records = updateDB(filtered_data)


def dailyUpdate():
    removeOldRecords()
    updateDetectionParams()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Módulo de Análisis')
    parser.add_argument(
        '--setup_database', action='store_true', help='Setup de base de datos')
    parser.add_argument(
        '--download_lastmonth', action='store_true', help='Bajar y cargar la informacion del ultimo mes')
    parser.add_argument(
        '--load_apidump', metavar="dump.json", action='store', default=None, help='Cargar informacion historica desde un json con los resultados de las llamadas a Teracode')
    parser.add_argument(
        '--generate_detection_params', action='store_true', help='Generar modelo para análisis de anomalías')
    parser.add_argument(
        '--execute_loop_now', action='store_true', help='Ejecuta un unico ciclo de loop')

    args = parser.parse_args()
    if args.setup_database:
        setupDB()

    if args.download_lastmonth:
        downloadAndLoadLastMonth()

    if args.load_apidump:
        loadApiDump(args.load_apidump)

    if args.generate_detection_params:
        updateDetectionParams()

    if args.execute_loop_now:
        executeLoop(datetime.datetime.now() -
                    datetime.timedelta(minutes=20), datetime.datetime.now())
