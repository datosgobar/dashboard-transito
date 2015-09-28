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
        '9_de_julio': [13, 17, 15, 19], # ok
        'cerrito': [16, 20], # ok
        'pellegrini': [14, 18], # ok
        'Illia': [12, 57, 11, 56], # ok
        'alcorta': [54, 55], # ok dudoso, esto no es libertador?
        'alem': [21, 22], # ok mal
        'av_de_mayo': [25], # ok
        'cabildo': [40, 42, 45, 41, 43, 44], # ok mal
        'cordoba': [36, 37], # ok
        'corrientes': [23], # ok
        'independencia': [10], # ok
        'juan_b_justo': [31, 32, 35, 30, 33, 34], # ok
        'libertador': [49, 51, 53, 48, 50, 52], # ok
        'paseo_colon': [39, 38], # ok
        'pueyrredon': [47, 46], # ok
        'rivadavia': [24], # ok
        'san_martin': [26, 28, 27, 29] # ok
    }

    referencia = {
        "centro": [10, 12, 57, 53, 51, 49, 22, 15, 19, 40, 37, 36, 31, 35, 14, 18, 23, 24, 25, 26, 28, 32, 47, 38, 43, 44],
        "provincia": [11, 56, 54, 55, 41, 16, 42, 21, 20, 10, 13, 27, 17, 29, 34, 39, 46, 50, 52, 48, 30, 33, 45]
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
            # time.sleep(0.5)update[0][1]
            ultima_actualizacion = (datetime.datetime.now() - dateutil.parser.parse(str(update[0][1]))).seconds/60
        self.emit("ultima_actualizacion", ultima_actualizacion)
    else:
        logger.info("sin datos en tabla")
        self.emit('info', "sin datos")
