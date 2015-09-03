#!/usr/bin/env python
# -*- coding: utf-8 -*-
from nose import with_setup
import datetime
from analisis import *
from unittest import TestCase
from nose import with_setup  # optional
from getDataFake import api_sensores_fake

"""
    link referencia http://pythontesting.net/framework/nose/nose-introduction/

    metodos en analisis
        getData
        downloadData
        createDBEngine
        getDBConnection
        setupDB
        updateDB

        removeOldRecords
        filterDuplicateRecords
        loadApiDump
        executeLoop
        getLastRecords
        
        getLastMonthRecords
        updateDetectionParams
        getCurrentSegmentState
        getDetectionParams
        
        upsertAnomalies
        updateSnapshot
        performAnomalyAnalysis
        downloadAndLoadLastMonth
        dailyUpdate


"""

sensor_ids = [10, 12, 57, 53, 51, 49, 40, 43, 37, 36, 21, 31, 33, 35, 13, 14, 18, 17, 23, 24, 25, 26, 28, 30,
              32, 45, 47, 38, 44, 48, 48, 11, 56, 54, 55, 41, 22, 16, 15, 19, 20, 10, 27, 29, 34, 39, 42, 46, 50, 52]


def setup_module(module):
    print ("")  # this is to get a newline after the dots
    print ("Unittest Analisis.py")
    print ("=" * 50)


def teardown_module(module):
    print ("")
    print ("fin")
    print ("=" * 50)


def my_setup_function():
    print ("my_setup_function")


def my_teardown_function():
    print ("my_teardown_function")


#@with_setup(my_setup_function, my_teardown_function)
def test_getData():
    endpoint_41 = "https://apisensores.buenosaires.gob.ar/api/data/41?token=superadmin.&fecha_desde=2015-09-01T10:39:31-03:00&fecha_hasta=2015-09-01T11:09:31-03:00"
    print "===> test getData {0}".format(endpoint_41)
    result = getData(endpoint_41)
    assert result['codigo'] == "200"


def test_downloadData():
    list_assert = []
    list_fall = []
    hasta = datetime.datetime.now()
    desde = hasta - datetime.timedelta(minutes=20)
    # downloadData(sensor_ids, step, download_startdate, download_enddate,
    # outfn=None, token="superadmin.", pool_len=5)
    print str(datetime.datetime.now())
    result = downloadData(
        sensor_ids, datetime.timedelta(days=2), desde, hasta, pool_len=5)
    print str(datetime.datetime.now())

    for res in result:
        if res['codigo'] == '200':
            list_assert.append(res)
        else:
            list_fall.append({
                "id": res['datos']['id'],
                "start": res['datos']['date_beg'],
                "end": res['datos']['date_end']
            })

    print "fallaron los siguientes sensores {}".format(list_fall)
    assert len(list_assert) == 48


def test_getDBConnection_createDBEngine():
    import config
    assert getDBConnection().engine.driver in config.db['engine']
    assert createDBEngine().connect()


def test_setupDB():
    # [u'migrate_version', u'historical', u'causa', u'segment_snapshot', u'anomaly']
    import json
    from sqlalchemy.orm import Session
    with open(os.path.abspath("../static/data/causas.json")) as f:
        causas = json.loads(f.read())
    engine = createDBEngine()
    session = Session(engine)
    Causa = Base.classes.causa
    session.query(Causa)
    for causa in causas['causas']:
        assert session.query(Causa).filter(Causa.id == causa['id']).count()


def test_updateDB():
    filtered_data = []
    updateDB(filtered_data)
    pass


def test_removeOldRecords():
    pass


def test_filterDuplicateRecords():
    hasta = datetime.datetime.now()
    desde = hasta - datetime.timedelta(minutes=20)
    print str(desde), str(hasta), "===", type(hasta), "diff 20min"
    data = downloadData(
        sensor_ids, datetime.timedelta(days=2), desde, hasta, pool_len=5)
    assert len(data) != 0
    filter_records = filterDuplicateRecords(data, desde, hasta)
    if filter_records:
        for obj in filter_records:
            assert hasattr(obj, 'id')
    else:
        print "filter_records sin resultado"
        assert len(filter_records) == 0


def test_loadApiDump():
    pass


def test_executeLoop():
    pass


def test_getLastRecords():
    hasta = datetime.datetime.now()
    desde = hasta - datetime.timedelta(minutes=20)
    last_records = getLastRecords(desde, hasta)
    assert len(last_records) == 3
    assert type(last_records[0]) == int
    assert type(last_records[1]) == int
    assert type(last_records[2]) == datetime.datetime
