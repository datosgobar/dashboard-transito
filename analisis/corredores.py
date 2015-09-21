#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import random
import config
import json
import datetime
import dateutil.parser

from sqlalchemy import create_engine
from dashboard_logging import dashboard_logging

db_url = config.db_url
engine = create_engine(db_url)
logger = dashboard_logging(config="logging.json", name=__name__)


def readSnapshot():
    """
            readSegmentos()
    """
    result = []

    try:
        cur = engine.connect()
    except Exception, ex:
        logger.error("read snapshot", traceback=True)
        result = []
    else:
        segment_snapshot = cur.execute("SELECT * FROM segment_snapshot")
        for row in segment_snapshot.fetchall():
            result.append(row)
        logger.info("read snapshot total: {}".format(len(result)))
    finally:
        cur.close()
        return result


def buildSegmentos(segment):
    return {
        "id": int(segment.id),
        "timestamp_medicion": str(segment.timestamp_medicion),
        "tiempo": int(segment.tiempo),
        "velocidad": int(segment.velocidad),
        "causa": str(segment.comentario_causa),
        "causa_id": int(segment.causa_id),
        "duracion_anomalia": int(segment.duracion_anomalia),
        "indicador_anomalia": float(segment.indicador_anomalia),
        "anomalia": int(segment.anomalia),
        "anomalia_id": int(segment.anomalia_id),
        "tipo_corte": int(segment.tipo_corte)
    }


def parserEmitData(self, template):
    """
            buildCorredores(
                corredores=corredores, template=template, update=result)
            evaluar si el segmentos corresponde a un corredor y si ese mismo es para prov o capi
    """
    corredores = {
        '9_de_julio': [13, 17, 15, 19],
        'cerrito': [16, 20],
        'pellegrini': [14, 18],
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

    update = readSnapshot()

    if len(update):
        for i in range(len(update)):
            for corredor, segmentosids in corredores.iteritems():
                if update[i][0] in segmentosids:
                    if update[i][0] in referencia['centro']:
                        # logger.info("{0} {1} {2}".format(update[i][0], c,
                        # 'centro'))
                        template['corredores'][corredor][
                            'segmentos_capital'].append(buildSegmentos(update[i]))
                    else:
                        # logger.info("{0} {1} {2}".format(update[i][0], c,
                        # 'prov'))
                        template['corredores'][corredor][
                            'segmentos_provincia'].append(buildSegmentos(update[i]))
                else:
                    continue

        for channell in corredores.keys():
            # logger.info("channel {0} template {1}".format(channell,
            # template['corredores'][channell]))
            self.emit(channell, template['corredores'][channell])
            logger.info("updateo channel {0}".format(channell))
            # time.sleep(0.5)
            ultima_actualizacion = str(
                (datetime.datetime.now() - dateutil.parser.parse(str(update[0][1])))).split(".")[0]
        self.emit("ultima_actualizacion", ultima_actualizacion)
    else:
        logger.info("sin datos en tabla")
        self.emit('info', "sin datos")
