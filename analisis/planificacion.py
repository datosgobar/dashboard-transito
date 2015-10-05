#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conn_sql import sqlalchemyDEBUG, instanceSQL
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, exc, event
from corredores import referencia_sentidos, referencia_corredores

import config
import datetime
import dateutil.parser
import pdb
import config
import json


conn_sql = instanceSQL(cfg=config)
conn_sql.createDBEngine()

Causa = conn_sql.instanceTable(unique_table='causa')
Anomaly = conn_sql.instanceTable(unique_table='anomaly')
Historical = conn_sql.instanceTable(unique_table='historical')
SegmentSnapshot = conn_sql.instanceTable(unique_table='segment_snapshot')


"""

    1) Cantidad anomalias por semana x sentido (prov, centro) y (desde hoy a los ultimos 7 dias pasados) y tiempo promedio (de esa semana)  
            (comparalo 4 semanas) ??

    2) Media duracion anomalia por corredor por sentido
        (agrupar todas las anomalias por corredor y generar el promedio de duracion)


    3) Duracion de cada anomalia
        agrupar todas las anomalias por niveles y cual es la duracion ?? es algo mas complejo, solicitar a pablo


    4) 

"""
