#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import json
import StringIO


franjas = [
    ("00:00:00", "07:00:00"),
    ("07:00:00", "10:00:00"),
    ("10:00:00", "17:00:00"),
    ("17:00:00", "20:00:00"),
    ("20:00:00", "23:59:00"),
]


def prepareDataFrame(df, timeadjust=None, doimputation=False):
    dfdaytype = pd.DataFrame([
        "workingday",
        "workingday",
        "workingday",
        "workingday",
        "workingday",
        "saturday",
        "sunday",
    ])
    df.date = pd.to_datetime(df.date)

    # Ajuste del timezone
    if timeadjust:
        df.date += timeadjust

    df["weekday"] = df.date.dt.weekday
    df["daytype"] = dfdaytype.loc[df.weekday].values[:, 0]

    # Imputacion de datos faltantes
    if doimputation:
        # Datos para completar los faltantes
        filler_data = df.groupby(
            [df.date.dt.hour, df.daytype, df.iddevice]).mean()["data"]
        newrecords = []
        for iddevice in df.iddevice.unique():
            work = df[df.iddevice == iddevice].sort("date")
            diff = work.date.shift(periods=-1) - work.date
            diff = diff[diff > pd.Timedelta(hours=1, minutes=10)]
            for idx in diff.index:
                # if d.iloc[0] == pd.NaT or d.iloc[1] == pd.NaT:
                #    continue
                r = pd.date_range(
                    start=work.loc[idx].date, end=work.loc[idx].date + diff.loc[idx], freq="h")
                filler_values = filler_data.loc[
                    zip(r.hour, dfdaytype.loc[r.weekday].values[:, 0], [iddevice] * len(r))].reset_index(drop=True).values
                newrecord_data = {
                    "iddevice": [iddevice] * len(r),
                    "data": filler_values,
                    "date": r
                }
                newrecord = pd.DataFrame(
                    newrecord_data, columns=['iddevice', u'data', u'date'])
                newrecords += [newrecord]

    df = pd.concat([df] + newrecords)

    # Normalizacion de intervalos a 5min
    df.index = df.date
    df = df.groupby("iddevice").resample(
        "5Min", how='mean').interpolate(method='linear').reset_index()
    df.index = df.date

    # Agregado de dia tipo de dia
    #df["weekday"] = df.date.apply(lambda e: e.weekday())
    df["weekday"] = df.date.dt.weekday
    df["time"] = df.date.dt.time
    df["daytype"] = dfdaytype.loc[df.weekday].values[:, 0]
    #df.loc[df.weekday.isin([0, 1, 2, 3, 4]), "daytype"] = "workingday"
    #df.loc[df.weekday == 5, "daytype"] = "saturday"
    #df.loc[df.weekday == 6, "daytype"] = "sunday"

    # Agregado de franjas horarias
    for (i, (begin, end)) in enumerate(franjas):
        df.ix[df.index.indexer_between_time(
            start_time=begin, end_time=end), "franja"] = int(i)
    #df["franja"] = df["franja"].astype(int)
    return df.reset_index(drop=True)

"""
Esta funcion implementa el detector de anomalias.
Recibe como entrada :
- Una string a modo de blob que con los parametros de configuracion del detector
- Un listado de tuplas de la forma (id_segment, data, timestamp) con los datos de los ultimos 20 minutos

Retorna una lista con las anomalias encontradas de la forma:
[{'timestamp': datetime.datetime(2015, 7, 12, 6, 0), 'indicador_anomalia': 2.29, 'id_segment': 10}]
"""


def detectAnomalies(detectparams, lastrecords, dontfilter=False):
    if len(lastrecords) == 0:
        return []
    detectparams = pd.read_json(detectparams, orient="records")
    lastrecords = pd.DataFrame(
        lastrecords, columns=["iddevice", "data", "date"])
    lastrecords = lastrecords.groupby('iddevice').apply(
        lambda df: df[df.date == df.date.max()].iloc[0])
    lastrecords = prepareDataFrame(lastrecords)

    resultsdf = _detectAnomalies(detectparams, lastrecords)

    if dontfilter:
        anomalies = resultsdf
    else:
        anomalies = resultsdf[resultsdf["isanomaly"]]

    def formatOutput(anomaly):
        anomaly = anomaly[1]
        return {
            "id_segment": anomaly["iddevice"],
            "timestamp": anomaly["date"].to_pydatetime(),
            "indicador_anomalia": round((anomaly["data"] - anomaly["mean"]) / anomaly["std"], 2),
            "threshold": anomaly["threshold"],
            "evalfield": anomaly["data"],
            "isanomaly": anomaly["isanomaly"],
        }
    output = map(formatOutput, anomalies.iterrows())
    return output


def _detectAnomalies(detectparams, lastrecords):
    evalfield = "data"
    basefield = "mean"
    marginfield = "std"
    # resultsdf = pd.merge(
    # lastrecords, detectparams, on=["iddevice", "franja",
    # "daytype"]).sort("date")
    resultsdf = pd.merge(
        lastrecords, detectparams, on=["iddevice", "franja", "daytype", "time"]).sort("date")

    #anomalies = resultsdf[resultsdf[evalfield]>(resultsdf[basefield]+resultsdf[marginfield])]
    #resultsdf["threshold"] = resultsdf[basefield]
    resultsdf["threshold"] = resultsdf[basefield] + resultsdf[marginfield] * 2
    resultsdf["isanomaly"] = resultsdf[evalfield] > resultsdf["threshold"]
    return resultsdf


"""
Recibe un listado de tuplas de la forma (id_segment, data, timestamp)
"""


def computeDetectionParams(lastmonthrecords):
    apidata = pd.DataFrame(
        lastmonthrecords, columns=["iddevice", "data", "date"])
    apidata = prepareDataFrame(apidata, doimputation=True)
    output = _computeDetectionParams(apidata)
    return output.to_json(orient="records")


def _computeDetectionParams(lastmonthrecords):
    detectparams = lastmonthrecords.groupby(["iddevice", "franja", "daytype"])["data"].agg(
        {"mean": "mean", "std": "std"}).reset_index()

    timetable = pd.DataFrame(
        index=pd.date_range("00:00", "23:59", freq="5min"))
    for (i, (begin, end)) in enumerate(franjas):
        timetable.ix[timetable.index.indexer_between_time(
            start_time=begin, end_time=end), "franja"] = int(i)

    timetable = timetable.reset_index()
    timetable.columns = ["time", "franja"]
    timetable["time"] = timetable.time.dt.time
    resampled_detectparams = pd.merge(detectparams, timetable)

    # Funcion de ventana para ensanchar margenes

    def widdenSeries(s):
        ret = pd.rolling_max(s, window=20, center=True)
        ret = ret.fillna(method="ffill").fillna(method="bfill")
        ret = pd.rolling_mean(ret, window=10, center=True)
        ret = ret.fillna(method="ffill").fillna(method="bfill")
        return ret

    # resampled_detectparams = resampled_detectparams.set_index(
    #    ["iddevice", "daytype"])
    # newdetectparams_gp = resampled_detectparams.groupby(
    #    level=["iddevice", "daytype"])
    #newdetectparams = newdetectparams_gp["mean", "std"].transform(widdenSeries)
    #newdetectparams["franja"] = resampled_detectparams["franja"]
    #newdetectparams["time"] = resampled_detectparams["time"]
    #newdetectparams = newdetectparams.reset_index()

    resampled_detectparams.set_index(["iddevice", "daytype"], inplace=True)
    for iddevice in detectparams.iddevice.unique():
        # workdf = resampled_detectparams[
        #    resampled_detectparams["iddevice"] == iddevice]
        # workdf.loc[["workingday", "saturday", "sunday"], ["mean", "std"]] = widdenSeries(workdf.ix[
        #    ["workingday", "workingday", "saturday", "sunday", "workingday"], ["mean", "std"]]).iloc[
        #    len(workdf.ix["workingday"]): -len(workdf.ix["workingday"])]
        # resampled_detectparams.iloc[["workingday", "saturday", "sunday"], ["mean", "std"]].loc[:, ] = widdenSeries(workdf.ix[
        #    ["workingday", "workingday", "saturday", "sunday", "workingday"], ["mean", "std"]]).iloc[
        #    len(workdf.ix["workingday"]): -len(workdf.ix["workingday"])]
        # resampled_detectparams.loc[
        #    resampled_detectparams["iddevice"] == iddevice].ix[["workingday", "saturday", "sunday"], ["mean", "std"]] = widdenSeries(workdf.ix[
        #        ["workingday", "workingday", "saturday", "sunday", "workingday"], ["mean", "std"]]).iloc[
        #    len(workdf.ix["workingday"]): -len(workdf.ix["workingday"])]
        workdf = resampled_detectparams.loc[iddevice, :]
        a = widdenSeries(workdf.ix[
            ["workingday", "workingday", "saturday", "sunday", "workingday"], ["mean", "std"]]).iloc[
            len(workdf.ix["workingday"]): -len(workdf.ix["workingday"])]
        a["iddevice"] = iddevice
        a = a.reset_index()
        a.set_index(["iddevice", "daytype"], inplace=True)

        resampled_detectparams.loc[(iddevice, "workingday"), "mean"] = a.loc[
            (iddevice, "workingday"), "mean"]
        resampled_detectparams.loc[(iddevice, "saturday"), "mean"] = a.loc[
            (iddevice, "saturday"), "mean"]
        resampled_detectparams.loc[(iddevice, "sunday"), "mean"] = a.loc[
            (iddevice, "sunday"), "mean"]

    return resampled_detectparams.reset_index()


"""
# El codigo de ejemplo que sigue funciona tanto con timestamps en forma de string como con objetos datetime
from anomalyDetection import *
from analisis import * 

# Con el timestamp a modo de string
import pandas as pd
import json 
import dateutil.parser
lastmonthrecords = [(10, 222, '2015-07-12T00:00:01-03:00'), (10, 217, '2015-07-12T01:00:00-03:00'), (10, 183, '2015-07-12T02:00:00-03:00'), (10, 248, '2015-07-12T03:00:00-03:00')]
def f(r) :
    return [
        r[0],
        r[1],
        dateutil.parser.parse(r[2])
    ]

lastmonthrecords = map(f, lastmonthrecords)

# Con el timestamp como objeto datetime
import datetime
from dateutil.tz import tzoffset
lastmonthrecords = [[10, 222, datetime.datetime(2015, 7, 12, 0, 0, 1, tzinfo=tzoffset(None, -10800))], [10, 217, datetime.datetime(2015, 7, 12, 1, 0, tzinfo=tzoffset(None, -10800))], [10, 183, datetime.datetime(2015, 7, 12, 2, 0, tzinfo=tzoffset(None, -10800))], [10, 248, datetime.datetime(2015, 7, 12, 3, 0, tzinfo=tzoffset(None, -10800))]]

# Las lineas que siguen emulan el proceso de:
# 1) Calcular los parametros del modelo
# 2) Evaluar los los mismos datos con el modelo generado
# 3) Combinar la informacion de las ultimas mediciones con la de las anomalias detectadas

detectparams = computeDetectionParams(lastmonthrecords)
lastrecords = lastmonthrecords
anomalies = detectAnomalies(detectparams, lastrecords)
getCurrentSegmentState (anomalies, lastrecords)
"""
