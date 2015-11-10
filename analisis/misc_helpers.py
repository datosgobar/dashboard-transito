#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import numpy as np
import pandas as pd
import datetime
import dateutil.parser
import config


from conn_sql import sqlalchemyDEBUG, instanceSQL
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, exc, event

conn_sql = instanceSQL(cfg=config)
conn_sql.createDBEngine()
session = conn_sql.session()

Corredores = conn_sql.instanceTable(unique_table='corredores')
tabla_corredores = session.query(Corredores).all()
from corredores import referencia_corredores, referencia_sentidos


def loadData(infn):
    alldata_raw = json.load(open(infn))
    alldata_raw = [e for e in alldata_raw if e != None]
    measurements = []
    for rawres in alldata_raw:
        if rawres == None:
            continue
        if len(rawres["datos"]) == 0:
            continue
        for rawel in rawres["datos"]["data"]:
            measurements += [{
                "data": rawel["data"],
                "iddevice": rawel["iddevice"],
                "id_data_type": rawel["id_data_type"],
                "date": rawel["date"],
            }]
    df = pd.DataFrame(measurements)
    df["date"] = pd.to_datetime(df["date"]) - datetime.timedelta(hours=3)
    return df


acentro = referencia_sentidos['centro']
aprovincia = referencia_sentidos['provincia']

corrdata = dict([(wp.id, {"name": wp.corredor, "description": wp.segmento}) for wp in tabla_corredores])

for k in corrdata.keys():
    corrdata[k][
        "label"] = "%s - %s" % (corrdata[k]["name"], corrdata[k]["description"])
    if k in acentro:
        corrdata[k]["corr"] = "%s_%s" % (corrdata[k]["name"], "acentro")
    if k in aprovincia:
        corrdata[k]["corr"] = "%s_%s" % (corrdata[k]["name"], "aprovincia")


data = []
coords = []
split_latlng = lambda s: map(float, s.split(", "))
for e in tabla_corredores:
    data += [{
        "name": e.corredor,
        "description": e.segmento,
        "id": e.id,
        "corr": corrdata[e.id]["corr"],
        "num_waypoints": 2 + len(set(eval(e.waypoints_collection[0].linestring)))
    }]
    for (i, (lat, lng)) in enumerate(map(split_latlng, [e.waypoints_collection[0].desde] +
                                         list(eval(e.waypoints_collection[0].linestring)) + [e.waypoints_collection[0].hasta])):
        coords += [{
            "id": e.id,
            "wp_index": i,
            "lat": lat,
            "lng": lng,
        }]


corrdatadf = pd.DataFrame(data)
coordsdf = pd.DataFrame(coords)


def coords_to_meters(lat0, lng0, lat1, lng1):
    degrees_to_radians = np.pi / 180.0
    phi1 = (90.0 - lat0) * degrees_to_radians
    phi2 = (90.0 - lat1) * degrees_to_radians
    theta1 = lng0 * degrees_to_radians
    theta2 = lng1 * degrees_to_radians
    cos = (np.sin(phi1) * np.sin(phi2) *
           np.cos(theta1 - theta2) + np.cos(phi1) * np.cos(phi2))
    arc = np.arccos(cos)
    return arc * 6371. * 1000

aux = coordsdf.groupby("id").agg({"lng": {"lng0": "first", "lng1": "last"}, "lat": {"lat0": "first", "lat1": "last"}}).reset_index()
aux.columns = aux.columns.droplevel()
aux = aux.rename(columns={"": "id"})
aux["len"] = coords_to_meters(aux["lat0"], aux["lng0"], aux["lat1"], aux["lng1"])
corrdatadf = pd.merge(corrdatadf, aux, on="id")
corrlenghts = corrdatadf.groupby("corr").sum()["len"].reset_index()
