#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import random
import config
import json
from getDataFake import readSegmentos
from sqlalchemy import create_engine

db_url = config.db_url
engine = create_engine(db_url)


def readSnapshot():
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
        cur.execute("SELECT * FROM segment_snapshot")
        for row in cur.fetchall():
            result.append(row)
    finally:
        cur.close()
        return result


def buildSegmentos(data):
    return {
        "id": int(data[0]),
        "timestamp_medicion": str(data[1]),
        "tiempo": int(data[2]),
        "velocidad": int(data[3]),
        "causa": str(data[4]),
        "causa_id": int(data[5]),
        "duracion_anomalia": int(data[6]),
        "indicador_anomalia": float(data[7]),
        "anomalia": int(data[8])
    }


def parserEmitData(self, template):
    """
            buildCorredores(
                corredores=corredores, template=template, update=result)
            evaluar si el segmentos corresponde a un corredor y si ese mismo es para prov o capi
    """
    corredores = {
        '9_de_julio': [13, 17, 15, 19],
        '9_de_julio_externo': [14, 18, 16, 20],
        'Illia': [12, 57, 11, 56],
        'alcorta': [54, 55],
        'alem': [21, 22],
        'av_de_mayo': [25],
        'cabildo': [40, 42, 45, 41, 43, 44],
        'cordoba': [36, 37],
        'corrientes': [23],
        'independencia': [10],
        'juan_b_justo': [31, 32, 35, 30, 33, 34],
        'libertador': [49, 51, 53, 48, 50, 52],
        'paseo_colon': [39],
        'pueyrredon': [47, 46],
        'rivadavia': [24],
        'san_martin': [26, 28, 27, 29]
    }

    referencia = {
        "centro": [10, 12, 57, 53, 51, 49, 40, 37, 36, 21, 31, 35, 13, 14, 18, 17, 23,
                   24, 25, 26, 28, 32, 45, 47, 38, 42],
        "provincia": [11, 56, 54, 55, 41, 22, 16, 15, 19, 20, 10, 27, 29, 34, 39, 46, 50, 52, 48, 30, 33, 43, 44]
    }

    #update = readSnapshot()
    update = readSegmentos()

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
