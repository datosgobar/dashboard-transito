#!/usr/bin/env python
# -*- coding: utf-8 -*-

from analisis import *
from nose.tools import with_setup

"""
	Metodos en analisis

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


def setup_func():
    a = 2


def teardown_func():
    print "b"


@with_setup(setup_func, teardown_func)
def test():


def main():
    test()


if __name__ == '__main__':
    main()
