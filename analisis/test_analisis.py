#!/usr/bin/env python
# -*- coding: utf-8 -*-
from nose import with_setup
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


def setup_module(module):
    print ("")  # this is to get a newline after the dots
    print ("setup_module before anything in this file")


def teardown_module(module):
    print ("teardown_module after everything in this file")


def my_setup_function():
    print ("my_setup_function")


def my_teardown_function():
    print ("my_teardown_function")


@with_setup(my_setup_function, my_teardown_function)
def test_getData():
    pass  # api_sensores_fake
