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
import os.path

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
        self.savepath_folder = os.path.abspath(".") + "/static/graficos/"

        self.timestamp_end = datetime.datetime.now()
        self.timestamp_start = self.timestamp_end - datetime.timedelta(weeks=4)

        if not os.path.exists(self.savepath_folder):
            os.mkdir(self.savepath_folder)

        self.savepath_folder = self.savepath_folder + "{0}_{1}".format(str(self.timestamp_start.date()).replace(
            "-", ""), str(self.timestamp_end.date()).replace("-", ""))

        if not os.path.exists(self.savepath_folder):
            os.mkdir(self.savepath_folder)

        self.savepath_file = self.savepath_folder + "/{0}"
        self.savepath_csv = None

        self.__flg = False
        self.corrdata = []
        self.valids = {}
        self.reportdata = None
        self.session = conn_sql.session()
        self.aux = None

        for (idseg, data) in misc_helpers.corrdata.items():
            d = data.copy()
            d["iddevice"] = idseg
            self.corrdata += [d]

        self.mensuales = {
            "anomalias_ultimo_mes": "Cantidad total de anomalias en las ultimas 4 semanas",
            "duracion_media_anomalias": "Duracion media de anomalias por corredor",
            "duracion_en_perceniles": "Duracion en Perceniles",
            "cant_anomalias_xcorredores": "Cantidad de anomalias por corredor",
            "indice_anomalias_xcuadras": "Indice de anomalias por cuadra"
        }

        self.semanales = {}

        self.__grp = {
            'mensuales': self.mensuales.keys(),
            'semanales': self.semanales.keys()
        }

        # metodos privados
        self.__asignacion_frame()
        self.__generacion_dataframe()

    def generacion_graficos(self, tipo="mensuales"):
        """
           grafico.generacion_graficos(tipo="mensuales") 
           grafico.generacion_graficos(tipo="semanales")
        """
        for grafico in self.__grp[tipo]:
            eval("self.{0}()".format(grafico))

    def generador_csv(self):
        pass

    def guardar_grafico(self, grafico={}):
        """
            grafico.guardar_grafico(grafico={'idg': 'aum3028', 'timestamp_start': datetime.date(2015, 9, 30), 
                'timestamp_end': datetime.date(2015, 10, 28), 'name': 'Cantidad total de anomalias en las ultimas 4 semanas', 
                'filename': 'anomalias_ultimo_mes_2015_09_30_2015_10_28.png'})
        """
        filesave = self.savepath_file.format(grafico.get("filename"))
        query = self.session.query(Estadisticas)
        if_count_id = query.filter(
            Estadisticas.idg == grafico.get("idg")).count()
        if not if_count_id:
            nuevo_grafico = Estadisticas(
                idg=grafico.get("idg"), name=grafico.get('name'), filename=filesave.replace(os.path.abspath(".") + "/static/", "/_static/"),
                timestamp_start=grafico.get('timestamp_start'), timestamp_end=grafico.get('timestamp_end')
            )
            self.session.add(nuevo_grafico)
            self.session.commit()
        if not os.path.exists(filesave):
            plt.savefig(filesave)

    def __instanciar_save(self, **args):
        if args.get("ifcsv") == True:
            self.generador_csv()
        if args.get("ifsave"):
            params = args.get('params')
            self.guardar_grafico(grafico=params)
        if args.get("ifshow") == True:
            plt.show()
        plt.close()

    def __wrpsave(self, name_func, **args):
        metadata = self.generar_metadata(name=name_func)
        self.__instanciar_save(ifsave=args.get("save"), ifcsv=args.get(
            "csv"), ifshow=args.get("show"), params=metadata)

    def generar_metadata(self, name):
        """
            grafico.generar_metadata(name=grafico.anomalias_ultimo_mes.__name__)
            Params
                name: Nombre del metodo que genera el grafico, segun el tipo, se guarda en self.mensuales o self.semanales| dic
        """
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
        self.aux = self.reportdata.copy()
        self.aux = self.aux.groupby(
            [self.aux["timestamp_start"].dt.week, self.aux["sentido"]]).size()
        self.aux = self.aux.reset_index().rename(
            columns={"level_0": "semana", 0: "count"})
        self.aux = self.aux.pivot(
            index='semana', columns='sentido', values='count').reset_index()
        self.aux.columns.name = "Referencia"
        self.aux["promedio"] = (self.aux["centro"] + self.aux["provincia"]) / 2
        self.aux["semana"] = self.aux["semana"].astype(str)
        self.ax = self.aux[["semana", "promedio"]].plot(x='semana', color="r")
        self.ax = self.aux[["semana", "centro", "provincia"]].plot(
            x='semana', kind='bar', ax=self.ax)
        self.__wrpsave(
            self.anomalias_ultimo_mes.__name__, save=save, csv=csv, show=show)

    def duracion_media_anomalias(self, save=True, csv=True, show=False):
        """
            Duracion media de anomalias por corredor
            grafico.anomalias_ultimo_mes(save=True, csv=True, show=True)
                Params
                    save: Guarda su metadata en una tabla en la base de datos.
                    csv: Guarda la tabla que genera el grafico en un csv
                    show: Muestra el grafico en pantalla
        """
        self.aux = self.reportdata.copy()
        self.aux = self.reportdata.groupby(
            ["corr", "corr_name", "sentido"]).mean()["duration"].reset_index()
        sns.barplot(x="corr_name", y="duration", hue="sentido", data=self.aux)
        plt.xticks(rotation=90)
        self.__wrpsave(
            self.duracion_media_anomalias.__name__, save=save, csv=csv, show=show)

    def duracion_en_perceniles(self, save=True, csv=True, show=False):
        """
            Duracion en Perceniles
        """
        self.reportdata.duration.quantile(
            [.1 * i for i in range(1, 11)]).plot(kind='line')
        plt.title('Duracion de en percentiles')
        plt.xlabel("Percentil")
        plt.ylabel("Duracion en minutos")
        self.__wrpsave(
            self.duracion_en_perceniles.__name__, save=save, csv=csv, show=show)

    def cant_anomalias_xcorredores(self, save=True, csv=True, show=False):
        """
            Cantidad de anomalias por corredor
        """
        self.aux = self.reportdata.copy()
        self.aux = self.aux.groupby(["corr", "sentido"]).size().reset_index().rename(
            columns={0: "size"})
        f, axarr = plt.subplots(1, 2, sharey=True)
        self.aux[self.aux["sentido"] == "centro"].plot(
            x="corr", kind="bar", ax=axarr[0])
        self.aux[self.aux["sentido"] == "provincia"].plot(
            x="corr", kind="bar", ax=axarr[1])
        self.__wrpsave(
            self.cant_anomalias_xcorredores.__name__, save=save, csv=csv, show=show)

    def indice_anomalias_xcuadras(self, save=True, csv=True, show=False):
        """
            Indice de anomalias por cuadra
        """
        self.aux = self.reportdata.groupby(["corr", "corr_name", "sentido"]).apply(
            lambda e: e.shape[0]).reset_index()
        self.aux = pd.merge(
            self.aux, misc_helpers.corrlenghts, on="corr").reset_index(drop=True)
        self.aux = self.aux.rename(columns={0: "anomalias", "len": "cuadras"})
        self.aux["indice"] = self.aux[
            "anomalias"] / (self.aux["cuadras"] / 100.)
        self.aux = self.aux[["corr", "indice", "corr_name", "cuadras", "anomalias", "sentido"]].sort(
            "indice", ascending=False)
        self.aux["indice"] = self.aux["indice"].round(2)
        self.aux["cuadras"] = (self.aux["cuadras"] / 100).astype(int)
        display(
            self.aux[["corr_name", "sentido", "indice", "cuadras", "anomalias"]])
        sns.barplot(x="corr_name", y="indice", hue="sentido", data=self.aux)
        plt.xticks(rotation=90)
        self.__wrpsave(
            self.indice_anomalias_xcuadras.__name__, save=save, csv=csv, show=show)

    def __asignacion_frame(self):
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

    def __generacion_dataframe(self):

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

    grafico = GraficosPlanificacion()
    grafico.generacion_graficos()

if __name__ == '__main__':
    main()
