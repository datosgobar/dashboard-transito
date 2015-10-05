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

import pandas as pd
import numpy as np
#import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
import json
import sys
import anomalyDetection
import misc_helpers

conn_sql = instanceSQL(cfg=config)
conn_sql.createDBEngine()

Causa = conn_sql.instanceTable(unique_table='causa')
Anomaly = conn_sql.instanceTable(unique_table='anomaly')
Historical = conn_sql.instanceTable(unique_table='historical')
SegmentSnapshot = conn_sql.instanceTable(unique_table='segment_snapshot')



# Datos de los de corredores
corrdata = []
for (idseg, data) in misc_helpers.corrdata.items():
    d = data.copy()
    d["iddevice"] = idseg
    corrdata += [d]

corrdata = pd.DataFrame(corrdata)
valids = pd.read_csv("/home/lmokto/Desktop/dump_anomaly.csv", sep=";")

valids["timestamp_start"] = pd.to_datetime(valids["timestamp_start"])
valids["timestamp_end"] = pd.to_datetime(valids["timestamp_end"])
valids["iddevice"] = valids[["id_segment"]]
valids = valids[
    (valids["timestamp_end"] - valids["timestamp_start"]).dt.seconds >= 20 * 60]
valids = valids[["iddevice", "timestamp_start", "timestamp_end"]].copy()


reportdata = pd.merge(
    valids, corrdata[["iddevice", "corr", "name"]], on=["iddevice"])
reportdata = reportdata.rename(columns={"name": "corr_name"})
reportdata["duration"] = (
    reportdata.timestamp_end - reportdata.timestamp_start).dt.seconds / 60.

reportdata["daytype"] = anomalyDetection.dfdaytype.loc[
    reportdata.timestamp_start.dt.weekday].values[:, 0]

reportdata["corr"] = corrdata.set_index(
    "iddevice").loc[reportdata["iddevice"]].reset_index()["corr"]

reportdata.loc[
    reportdata["corr"].str.endswith("_acentro"), "sentido"] = "centro"
reportdata.loc[
    reportdata["corr"].str.endswith("_aprovincia"), "sentido"] = "provincia"


#############
# 1er grafico
aux = reportdata.copy()
aux = aux.groupby([aux["timestamp_start"].dt.week, aux["sentido"]]).size()
aux = aux.reset_index().rename(columns={"level_0":"semana", 0:"count"})

aux = aux.pivot(index='semana', columns='sentido', values='count').reset_index()
aux.columns.name = None

aux["promedio"] = (aux["centro"] + aux["provincia"]) / 2
aux["semana"] =  aux["semana"].astype(str)

ax = aux[["semana", "promedio"]].plot(x='semana', color="r")
ax = aux[["semana", "centro", "provincia"]].plot(x='semana', kind='bar', ax=ax)

plt.title('Cantidad de anomalias en las ultimas 4 semanas')
plt.show()
#############

"""

    1) Cantidad anomalias por semana x sentido (prov, centro) y (desde hoy a los ultimos 7 dias pasados) y tiempo promedio (de esa semana)  
            (comparalo 4 semanas) ??

    2) Media duracion anomalia por corredor por sentido
        (agrupar todas las anomalias por corredor y generar el promedio de duracion)


    3) Duracion de cada anomalia
        agrupar todas las anomalias por niveles y cual es la duracion ?? es algo mas complejo, solicitar a pablo


    4) 

"""
