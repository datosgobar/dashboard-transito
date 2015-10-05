#!/usr/bin/env python
# -*- coding: utf-8 -*-

from waypoints import waypoints_config

import json
import pandas as pd
import numpy as np
import requests
import datetime
import dateutil.parser
import multiprocessing
import pandas as pd
import dateutil.parser
import datetime
import json

from corredores import referencia_corredores, referencia_sentidos
from pprint import pprint


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

corrdata = dict([(wp["id"], {"name": wp["name"], "description":wp[
                "description"]}) for wp in waypoints_config])
for k in corrdata.keys():
    corrdata[k][
        "label"] = "%s - %s" % (corrdata[k]["name"], corrdata[k]["description"])
    if k in acentro:
        corrdata[k]["corr"] = "%s_%s" % (corrdata[k]["name"], "acentro")
    if k in aprovincia:
        corrdata[k]["corr"] = "%s_%s" % (corrdata[k]["name"], "aprovincia")


import waypoints
data = []
coords = []
split_latlng = lambda s: map(float, s.split(", "))
for e in waypoints.waypoints_config:
    data += [{
        "name": e["name"],
        "description": e["description"],
        "id": e["id"],
        "corr": corrdata[e["id"]]["corr"],
        "num_waypoints": 2 + len(e["waypoints"])
    }]
    for (i, (lat, lng)) in enumerate(map(split_latlng, [e["from"]] + e["waypoints"] + [e["to"]])):
        coords += [{
            "id": e["id"],
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

aux = coordsdf.groupby("id").agg({"lng": {"lng0": "first", "lng1": "last"}, "lat": {
    "lat0": "first", "lat1": "last"}}).reset_index()
aux.columns = aux.columns.droplevel()
aux = aux.rename(columns={"": "id"})
aux["len"] = coords_to_meters(
    aux["lat0"], aux["lng0"], aux["lat1"], aux["lng1"])
corrdatadf = pd.merge(corrdatadf, aux, on="id")
corrlenghts = corrdatadf.groupby("corr").sum()["len"].reset_index()
