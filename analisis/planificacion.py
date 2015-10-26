#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conn_sql import sqlalchemyDEBUG, instanceSQL
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, exc, event
from corredores import referencia_sentidos, referencia_corredores
from IPython.display import display, HTML

import config
import datetime
import dateutil.parser
import pdb
import config
import json

import pandas as pd
import numpy as np

import os
import seaborn as sns
import matplotlib.pyplot as plt
import json
import sys
import anomalyDetection
import misc_helpers

conn_sql = instanceSQL(cfg=config)
conn_sql.createDBEngine()
Estadisticas = conn_sql.instanceTable(unique_table='estadisticas')


class GraficosPlanificacion(object):

    def __init__(self):

        self.corrdata = []
        self.valids = None
        self.reportdata = None

        for (idseg, data) in misc_helpers.corrdata.items():
            d = data.copy()
            d["iddevice"] = idseg
            self.corrdata += [d]

        self.__grp = {
            'mensaules': [
                "anomalias_ultimomes", "duracion_media_anomalias",
                "duracion_perceniles", "cant_anomalias_pc",  "indice_anomalias_cuadras"
            ],
            'semanales': []
        }

    def anomalias_ultimomes(self):
        """
            Cantidad total de anomalias en las ultimas 4 semanas
        """
        aux = self.eportdata.copy()
        aux = aux.groupby(
            [aux["timestamp_start"].dt.week, aux["sentido"]]).size()
        aux = aux.reset_index().rename(
            columns={"level_0": "semana", 0: "count"})
        aux = aux.pivot(
            index='semana', columns='sentido', values='count').reset_index()
        aux.columns.name = None
        aux["promedio"] = (aux["centro"] + aux["provincia"]) / 2
        aux["semana"] = aux["semana"].astype(str)
        ax = aux[["semana", "promedio"]].plot(x='semana', color="r")
        ax = aux[["semana", "centro", "provincia"]].plot(
            x='semana', kind='bar', ax=ax)
        plt.title('Cantidad de anomalias en las ultimas 4 semanas')
        plt.close()

    def duracion_media_anomalias(slef):
        """
            Duracion media de anomalias por corredor
        """
        aux = self.reportdata.copy()
        aux = self.reportdata.groupby(
            ["corr", "corr_name", "sentido"]).mean()["duration"].reset_index()
        sns.barplot(x="corr_name", y="duration", hue="sentido", data=aux)
        plt.xticks(rotation=90)
        # plt.show()
        plt.close()

    def duracion_perceniles(self):
        """
            Duracion en Perceniles
        """
        self.reportdata.duration.quantile(
            [.1 * i for i in range(1, 11)]).plot(kind='line')
        plt.title('Duracion de en percentiles')
        plt.xlabel("Percentil")
        plt.ylabel("Duracion en minutos")
        # plt.show()
        plt.close()

    def cant_anomalias_pc(self):
        """
            Cantidad de anomalias por corredor
        """
        aux = self.reportdata.copy()
        aux = aux.groupby(["corr", "sentido"]).size().reset_index().rename(
            columns={0: "size"})
        f, axarr = plt.subplots(1, 2, sharey=True)
        aux[aux["sentido"] == "centro"].plot(x="corr", kind="bar", ax=axarr[0])
        aux[aux["sentido"] == "provincia"].plot(
            x="corr", kind="bar", ax=axarr[1])
        # plt.show()
        plt.close()

    def indice_anomalias_cuadras(self):
        """
            Indice # anomalias por cuadra
        """
        aux = self.reportdata.groupby(["corr", "corr_name", "sentido"]).apply(lambda e: e.shape[0]).reset_index()
        aux = pd.merge(aux, misc_helpers.corrlenghts, on="corr").reset_index(drop=True)
        aux = aux.rename(columns={0:"anomalias","len":"cuadras"})
        aux["indice"] = aux["anomalias"] / (aux["cuadras"]/100.)
        aux = aux[["corr", "indice", "corr_name", "cuadras", "anomalias", "sentido"]].sort("indice", ascending=False)
        aux["indice"] = aux["indice"].round(2)
        aux["cuadras"] = (aux["cuadras"]/100).astype(int)
        display(aux[["corr_name","sentido","indice","cuadras","anomalias"]])
        sns.barplot(x="corr_name", y="indice", hue="sentido" , data=aux)
        plt.xticks(rotation=90)
        #plt.show()
        plt.close()

    def asignacion_frame(self, **args):
        """
           valids = asignacion_frame('anomaly', col1="id", col2="timestamp_end", col3="timestamp_end")
           # parse_dates={"timestamp_asignacion": (lambda X: "" if X == None else X)}
        """
        columns = []
        if args:
            args.update({'col0': 'id'})
            for e, col in enumerate(args):
                columns.append(args.get('col{0}'.format(e)))
        self.valids = pd.read_sql_table(
            tabla, conn_sql._instanceSQL__engine, columns=columns)
        return self.valids

    def generacion_dataframe(self):

        self.valids["timestamp_start"] = pd.to_datetime(
            valids["timestamp_start"])
        self.valids["timestamp_end"] = pd.to_datetime(valids["timestamp_end"])
        self.valids["iddevice"] = self.valids[["id_segment"]]
        self.valids = self.valids[
            (self.valids["timestamp_end"] - self.valids["timestamp_start"]).dt.seconds >= 20 * 60]
        self.valids = self.valids[
            ["iddevice", "timestamp_start", "timestamp_end"]].copy()

        self.reportdata = pd.merge(
            valids, corrdata[["iddevice", "corr", "name"]], on=["iddevice"])
        self.reportdata = self.reportdata.rename(columns={"name": "corr_name"})
        self.reportdata["duration"] = (
            self.reportdata.timestamp_end - self.reportdata.timestamp_start).dt.seconds / 60.
        self.reportdata["daytype"] = anomalyDetection.dfdaytype.loc[
            self.reportdata.timestamp_start.dt.weekday].values[:, 0]
        self.reportdata["corr"] = corrdata.set_index(
            "iddevice").loc[self.reportdata["iddevice"]].reset_index()["corr"]
        self.reportdata.loc[
            self.reportdata["corr"].str.endswith("_acentro"), "sentido"] = "centro"
        self.reportdata.loc[
            self.reportdata["corr"].str.endswith("_aprovincia"), "sentido"] = "provincia"

    def generacion_grafico(self):
        pass

    def generador_csv(self):
        pass

    def guardar_grafico(self, **grafico):
        """
            los graficos generados se tienen que almacenar en una tabla con su 
            filename, identificador y periodo generado

            tabla, csv y carpeta
        """
        session = conn_sql.session()
        __filename__ = "{0}_bar.png".format(grafico.get('filename'))
        nuevo_grafico = Estadisticas(
            id="bar2", name=grafico.get('name'), filename=__filename__, timestamp_start="2015-09-22", timestamp_end="2015-10-22")
        session.add(nuevo_grafico)
        session.commit()
        plt.savefig(
            os.path.abspath(".") + "/static/img/{0}".format(__filename__))


def main():
    pass

if __name__ == '__main__':
    main()
