#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import json
import StringIO


def prepareDataFrame (df) :
    franjas = [
        ("00:00:00", "07:00:00"),
        ("07:00:00", "10:00:00"),
        ("10:00:00", "17:00:00"),
        ("17:00:00", "20:00:00"),
        ("20:00:00", "23:59:00"),
    ]
    df.date = pd.to_datetime(df.date)
    df.index = df.date
    df = df.groupby("iddevice").resample("5Min", how='mean').interpolate(method='linear').reset_index()
    df.index = df.date
    df["weekday"] = df.date.apply(lambda e: e.weekday())
    df.loc[df.weekday.isin([0,1,2,3,4]), "daytype"] = "workingday"
    df.loc[df.weekday==5, "daytype"] = "saturday"
    df.loc[df.weekday==6, "daytype"] = "sunday"
    for (i,(begin,end)) in enumerate(franjas) :
        df.ix[df.index.indexer_between_time(start_time=begin, end_time=end),"franja"] = i
    df["franja"] = df["franja"].astype(int)
    return df.reset_index(drop=True)

"""
Esta funcion implementa el detector de anomalias.
Recibe como entrada 
"""
def detectAnomalies(detectparams, lastrecords) :
    detectparams = pd.read_json(detectparams, orient="records")
    lastrecords = pd.DataFrame(lastrecords, columns=["iddevice", "data", "date"])
    lastrecords = lastrecords.groupby('iddevice').apply(lambda df: df[df.date == df.date.max()].iloc[0])
    lastrecords = prepareDataFrame(lastrecords)
    
    evalfield="data"
    basefield="mean"
    marginfield="std"
    resultsdf = pd.merge(lastrecords, detectparams, on=["iddevice","franja","daytype"]).sort("date")
    anomalies = resultsdf[resultsdf[evalfield]>(resultsdf[basefield]+resultsdf[marginfield])]
    
    def formatOutput (anomaly) :
        anomaly = anomaly[1]
        return {
            "id_segment" : anomaly["iddevice"],
            "timestamp" : anomaly["date"].to_pydatetime(),
            "indicador_anomalia" : round((anomaly["data"]-anomaly["mean"]) / anomaly["std"], 2)
        }
    output = map(formatOutput, anomalies.iterrows())
    return output


"""
Recibe un listado de tuplas de la forma (id_segment, data, timestamp)
"""
def computeDetectionParams(lastmonthrecords) :
    apidata = pd.DataFrame(lastmonthrecords, columns=["iddevice", "data", "date"])
    apidata = prepareDataFrame(apidata)
    output = apidata.groupby(["iddevice","franja","daytype"])["data"].agg({"mean":"mean", "std":"std"}).reset_index()  
    return output.to_json(orient="records")

"""

"""
lastmonthrecords = [(10, 222, '2015-07-12T00:00:01-03:00'), (10, 217, '2015-07-12T01:00:00-03:00'), (10, 183, '2015-07-12T02:00:00-03:00'), (10, 248, '2015-07-12T03:00:00-03:00')]
detectparams = computeDetectionParams(lastmonthrecords)
lastrecords = lastmonthrecords
anomalies = detectAnomalies(detectparams, lastrecords)
