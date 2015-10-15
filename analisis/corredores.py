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

from conn_sql import sqlalchemyDEBUG, instanceSQL
conn_sql = instanceSQL(cfg=config)
conn_sql.createDBEngine()

TablaCorredores = conn_sql.instanceTable(unique_table='corredores')
TablaSegmentSnapshot = conn_sql.instanceTable(unique_table='segment_snapshot')
session = conn_sql.session()

logger = dashboard_logging(config="logging.json", name=__name__)

tabla_corredores = session.query(TablaCorredores).all()
tabla_segment_snapshot = session.query(TablaSegmentSnapshot).all()

corredores = dict(set(
    [(c.corredor.lower().replace(" ", "_"), c.ids) for c in tabla_corredores if c.ids]))


def asignacion(corredores, tabla_corredores):

    referencia_corredores = {corredor: [] for corredor in corredores if corredor}
    referencia_sentidos = {"centro": [], "provincia": []}

    for corredor in tabla_corredores:
        referencia_sentidos[corredor.sentido].append(corredor.id)

    if tabla_corredores:
        for nombre_corredor, segmentos_ids in referencia_corredores.iteritems():
            for corredor in tabla_corredores:
                if nombre_corredor.lower() == corredor.corredor.lower():
                    referencia_corredores[nombre_corredor].append(corredor.id)
                elif nombre_corredor.lower() == corredor.corredor.replace(" ", "_").lower():
                    referencia_corredores[nombre_corredor].append(corredor.id)

    return referencia_corredores, referencia_sentidos


referencia_corredores, referencia_sentidos = asignacion(
    corredores.keys(), tabla_corredores)


def buildSegmentos(segment):
    return {
        "id": int(segment.id),
        "nombreSegmento": [corredor.segmento for corredor in tabla_corredores if corredor.id == int(segment.id)][0],
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


def parserEmitData(self):

    template = {'corredores': {nombre: {'nombre': '', 'id': '', 'segmentos_capital': [], 'segmentos_provincia': []}
                               for nombre in corredores.keys() if nombre}}

    for corredor, ids in corredores.iteritems():
        template['corredores'][corredor]['id'] = ids
        template['corredores'][corredor][
            'nombre'] = corredor.replace("_", " ").title()

    if len(tabla_segment_snapshot):
        for segment in tabla_segment_snapshot:
            for corredor, segmentosids in referencia_corredores.iteritems():
                if segment.id in segmentosids:
                    if segment.id in referencia_sentidos['centro']:
                        template['corredores'][corredor][
                            'segmentos_capital'].append(buildSegmentos(segment))
                    else:
                        template['corredores'][corredor][
                            'segmentos_provincia'].append(buildSegmentos(segment))
                else:
                    continue

        for corredor in ("juan_b._justo", "libertador", "cerrito", "9_de_julio", "pellegrini", "alcorta"):
            template['corredores'][corredor]['segmentos_capital'].reverse()
            template['corredores'][corredor]['segmentos_provincia'].reverse()

        for channell in referencia_corredores.keys():
            # logger.info("channel {0} template {1}".format(channell, template['corredores'][channell]))
            logger.info("updateo channel {0}".format(channell))
            self.emit(channell, template['corredores'][channell])
            # time.sleep(0.5)update[0][1]
            ultima_actualizacion = (datetime.datetime.now(
            ) - dateutil.parser.parse(str(tabla_segment_snapshot[0].timestamp_medicion))).seconds / 60
        self.emit("ultima_actualizacion", ultima_actualizacion)
    else:
        logger.info("sin datos en tabla")
        self.emit('info', "sin datos")
