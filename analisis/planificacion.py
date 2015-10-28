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
Historical = conn_sql.instanceTable(unique_table='historical')


class GraficosPlanificacion(object):

    def __init__(self):

        self.metadata = []
        self.savepath_file = os.path.abspath(".") + "/static/img/{0}"
        self.savepath_csv = None
        self.timestamp_end = datetime.datetime.now()
        self.timestamp_start = self.timestamp_end - datetime.timedelta(weeks=4)
        self.__flg = False
        self.corrdata = []
        self.valids = {}
        self.reportdata = None
        self.session = conn_sql.session()

        for (idseg, data) in misc_helpers.corrdata.items():
            d = data.copy()
            d["iddevice"] = idseg
            self.corrdata += [d]

        self.mensuales = {
            "anomalias_ultimo_mes": "Cantidad total de anomalias en las ultimas 4 semanas",
            "duracion_media_anomalias": "Duracion media de anomalias por corredor",
            "duracion_perceniles": "Duracion en Perceniles",
            "cant_anomalias_xcorredores": "Cantidad de anomalias por corredor",
            "indice_anomalias_xcuadras": "Indice de anomalias por cuadra"
        }

        self.semanales = {}

        self.__grp = {
            'mensuales': self.mensuales.keys(),
            'semanales': self.semanales.keys()
        }

        self.asignacion_frame()
        self.generacion_dataframe()

    def generacion_graficos(self, tipo="mensuales"):
        for grafico in self.__grp[tipo]:
            eval("self.{0}()".format(grafico))

    def generador_csv(self):
        pass

    def guardar_grafico(self, grafico={}):
        """
            los graficos generados se tienen que almacenar en una tabla con su 
            filename, identificador y periodo generado

            tabla, csv y carpeta
        """
        nuevo_grafico = Estadisticas(idg=grafico.get("idg"), name=grafico.get('name'),
                                     filename=grafico.get('filename'), timestamp_start=grafico.get('timestamp_start'),
                                     timestamp_end=grafico.get('timestamp_end')
                                     )
        self.session.add(nuevo_grafico)
        self.session.commit()
        plt.savefig(self.savepath_file.format(grafico.get("filename")))

    def __instanciar_save(self, **args):
        print args
        if args.get("ifshow") == True:
            print "show"
            plt.show()
        if args.get("ifcsv") == True:
            print "csv"
            self.generador_csv()
        if args.get("ifsave"):
            print "save"
            params = args.get('params')
            print params
            self.guardar_grafico(grafico=params)
        plt.close()

    def generar_metadata(self, name):
        start = self.timestamp_start.date()
        end = self.timestamp_end.date()
        filename = "{0}_{1}_{2}.png".format(
            name, str(start).replace("-", "_"), str(end).replace("-", "_"))
        idn = name.split("_")
        _id = "{0}{1}{2}{3}{4}".format(
            idn[0][0], idn[1][0], idn[2][0], start.day, end.day)
        metadata_grafico = {
            "idg": _id,
            "name": self.mensuales[name],
            "filename": filename,
            "timestamp_start": start,
            "timestamp_end": end
        }
        self.metadata.append(metadata_grafico)
        return metadata_grafico

    def anomalias_ultimo_mes(self, save=True, csv=True, show=False):
        """
            Cantidad total de anomalias en las ultimas 4 semanas
            grafico.anomalias_ultimo_mes(save=False, csv=False, show=True)
        """
        aux = self.reportdata.copy()
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
        metadata = self.generar_metadata(
            name=self.anomalias_ultimo_mes.__name__)
        self.__instanciar_save(
            ifsave=save, ifcsv=csv, ifshow=show, params=metadata)

    def duracion_media_anomalias(self, save=True, csv=True, show=False):
        """
            Duracion media de anomalias por corredor
        """
        aux = self.reportdata.copy()
        aux = self.reportdata.groupby(
            ["corr", "corr_name", "sentido"]).mean()["duration"].reset_index()
        sns.barplot(x="corr_name", y="duration", hue="sentido", data=aux)
        plt.xticks(rotation=90)

    def duracion_perceniles(self, save=True, csv=True, show=False):
        """
            Duracion en Perceniles
        """
        self.reportdata.duration.quantile(
            [.1 * i for i in range(1, 11)]).plot(kind='line')
        plt.title('Duracion de en percentiles')
        plt.xlabel("Percentil")
        plt.ylabel("Duracion en minutos")

    def cant_anomalias_xcorredores(self, save=True, csv=True, show=False):
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

    def indice_anomalias_xcuadras(self, save=True, csv=True, show=False):
        """
            Indice de anomalias por cuadra
        """
        aux = self.reportdata.groupby(["corr", "corr_name", "sentido"]).apply(
            lambda e: e.shape[0]).reset_index()
        aux = pd.merge(
            aux, misc_helpers.corrlenghts, on="corr").reset_index(drop=True)
        aux = aux.rename(columns={0: "anomalias", "len": "cuadras"})
        aux["indice"] = aux["anomalias"] / (aux["cuadras"] / 100.)
        aux = aux[["corr", "indice", "corr_name", "cuadras", "anomalias", "sentido"]].sort(
            "indice", ascending=False)
        aux["indice"] = aux["indice"].round(2)
        aux["cuadras"] = (aux["cuadras"] / 100).astype(int)
        display(
            aux[["corr_name", "sentido", "indice", "cuadras", "anomalias"]])
        sns.barplot(x="corr_name", y="indice", hue="sentido", data=aux)
        plt.xticks(rotation=90)

    def asignacion_frame(self):
        # def asignacion_frame(self, tabla=Estadisticas, **args):
        """
           valids = asignacion_frame('anomaly', col1="id", col2="timestamp_end", col3="timestamp_end")
           # parse_dates={"timestamp_asignacion": (lambda X: "" if X == None else X)}
        """
        # columns = []
        # if args:
        #     args.update({'col0': 'id'})
        #     for e, col in enumerate(args):
        #         columns.append(args.get('col{0}'.format(e)))

        self.valids = pd.read_sql(
            ('select * from "anomaly" where "timestamp_start" BETWEEN %(dstart)s AND %(dfinish)s'),
            conn_sql._instanceSQL__engine, params={
                "dstart": self.timestamp_start, "dfinish": self.timestamp_end
            }
        )

        # self.valids = pd.read_sql_table(tabla, conn_sql._instanceSQL__engine, columns=columns)
        return self.valids

    def generacion_dataframe(self):

        self.corrdata = pd.DataFrame(self.corrdata)
        self.valids["timestamp_start"] = pd.to_datetime(
            self.valids["timestamp_start"])
        self.valids["timestamp_end"] = pd.to_datetime(
            self.valids["timestamp_end"])
        self.valids["iddevice"] = self.valids[["id_segment"]]
        self.valids = self.valids[
            (self.valids["timestamp_end"] - self.valids["timestamp_start"]).dt.seconds >= 20 * 60]
        self.valids = self.valids[
            ["iddevice", "timestamp_start", "timestamp_end"]].copy()

        self.reportdata = pd.merge(
            self.valids, self.corrdata[["iddevice", "corr", "name"]], on=["iddevice"])
        self.reportdata = self.reportdata.rename(columns={"name": "corr_name"})
        self.reportdata["duration"] = (
            self.reportdata.timestamp_end - self.reportdata.timestamp_start).dt.seconds / 60.
        self.reportdata["daytype"] = anomalyDetection.dfdaytype.loc[
            self.reportdata.timestamp_start.dt.weekday].values[:, 0]
        self.reportdata["corr"] = self.corrdata.set_index(
            "iddevice").loc[self.reportdata["iddevice"]].reset_index()["corr"]
        self.reportdata.loc[
            self.reportdata["corr"].str.endswith("_acentro"), "sentido"] = "centro"
        self.reportdata.loc[
            self.reportdata["corr"].str.endswith("_aprovincia"), "sentido"] = "provincia"


def main():
    grafico = planificacion.GraficosPlanificacion()
    grafico.anomalias_ultimo_mes()

if __name__ == '__main__':
    main()
