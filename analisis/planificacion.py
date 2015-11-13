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
import os.path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import csv
import os
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
        self.savepath_folder = os.path.abspath(".") + "/static/graficos/{0}/"
        self._mkdir(self.savepath_folder.replace("/{0}/", "/"))

        self.timestamp_end = datetime.datetime.now()
        self.timestamp_start = self.timestamp_end - datetime.timedelta(weeks=8)

        self.__mkdir(self.savepath_folder, ['csv', 'img'])

        self.savepath_folder = self.savepath_folder + "{0}_{1}".format(
            str(self.timestamp_start.date()).replace("-", ""),
            str(self.timestamp_end.date()).replace("-", "")
        )

        self.__mkdir(self.savepath_folder, ['csv', 'img'])

        self.savepath_file = self.savepath_folder.format('img') + "/{0}"
        self.savepath_csv = self.savepath_folder.format('csv') + "/{0}"

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
            "indice_anomalias_xcuadras": "Indice de anomalias por cuadra",
            "distribucion_horaria_sumarizada": "Distribucion horaria sumarizada",
            "anomalias_por_franjahoraria": "Duracion media de anomalias por franja horaria"
        }

        self.semanales = {}

        self.__grp = {
            'mensuales': self.mensuales.keys(),
            'semanales': self.semanales.keys()
        }

        self.__asignacion_frame()
        self.__generacion_dataframe()

    def _mkdir(self, folder):
        print folder
        if not os.path.exists(folder):
            os.mkdir(folder)

    def __mkdir(self, path, folders):

        for folder in folders:
            __folder = path.format(folder)
            self._mkdir(__folder)

    def generacion_graficos(self, tipo="mensuales"):
        """
           grafico.generacion_graficos(tipo="mensuales")
           grafico.generacion_graficos(tipo="semanales")
        """
        for grafico in self.__grp[tipo]:
            eval("self.{0}()".format(grafico))

    def generador_csv(self, filename, tabla):

        filesave = self.savepath_csv.format(filename.replace(".png", ".csv"))
        self.aux.to_csv(filesave)

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
        params = args.get('params')
        if args.get("ifcsv") == True:
            self.generador_csv(params.get("filename"), self.aux)
        if args.get("ifsave"):
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
            idn[0][0], idn[1][0], idn[2][0], str(start).replace("-", ""), end.day)
        metadata_grafico = {
            "idg": _id,
            "name": self.mensuales[name],
            "filename": filename,
            "timestamp_start": start,
            "timestamp_end": end
        }
        self.metadata.append(metadata_grafico)
        return metadata_grafico

    def anomalias_ultimo_mes(self, save=True, csv=False, show=False):
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

    def duracion_media_anomalias(self, save=True, csv=False, show=False):
        """
            Duracion media de anomalias por corredor
            grafico.anomalias_ultimo_mes(save=True, csv=False, show=True)
                Params
                    save: Guarda su metadata en una tabla en la base de datos.
                    csv: Guarda la tabla que genera el grafico en un csv
                    show: Muestra el grafico en pantalla
        """
        self.aux = self.reportdata.copy()
        self.aux = self.reportdata.groupby(["corr", "corr_name", "sentido"]).mean()["duration"].reset_index()
        graph = sns.factorplot(x="corr_name", y="duration", data=self.aux, saturation=.5, kind="bar", ci=None, size=4, aspect=2)
        graph.set_axis_labels("", "Duracion en Minutos").despine(left=True)
        #sns.factorplot(x="corr_name", y="duration", hue="sentido", kind="bar", data=self.aux, size=5, aspect=2)
        plt.xticks(rotation=17)
        #plt.ylabel('Duracion en minutos')
        #plt.xlabel('')
        self.__wrpsave(self.duracion_media_anomalias.__name__, save=save, csv=csv, show=show)

    def distribucion_horaria_sumarizada(self, save=True, csv=False, show=False):
        """
            Distribucion horaria sumarizada
        """
        self.aux = self.reportdata.copy()
        self.aux["Franja Horaria"] = self.aux["timestamp_start"].dt.hour
        self.aux = self.aux.rename(columns={'daytype': 'Tipos de Dias'})
        sns.factorplot("Franja Horaria", col="Tipos de Dias", hue="sentido", kind="count", data=self.aux, order=range(0, 24))
        plt.ylabel("Duracion en Minutos")
        self.__wrpsave(
            self.distribucion_horaria_sumarizada.__name__, save=save, csv=csv, show=show)

    def anomalias_por_franjahoraria(self, save=True, csv=False, show=False):
        self.aux = self.reportdata.copy()
        franjas = [
            (0, 7),
            (7, 10),
            (10, 17),
            (17, 20),
            (20, 24),
        ]
        for (i, (start, end)) in enumerate(franjas):
            self.aux.loc[
                (self.aux["timestamp_start"].dt.hour >= start) &
                (self.aux["timestamp_start"].dt.hour < end), "franja"] = i
        self.aux = self.aux.rename(columns={'daytype': 'Tipos de Dias', 'duration':'Duracion en Minutos'})
        self.aux.loc[self.aux["Tipos de Dias"].isin(["saturday", "sunday"]), "Tipos de Dias"] = "weekend"
        try:
            sns.boxplot(x="Tipos de Dias", y="Duracion en Minutos", hue="franja", hue_order=[0, 1, 2, 3, 4], data=self.aux)
        except:
            pass
        finally:
            self.__wrpsave(self.anomalias_por_franjahoraria.__name__, save=save, csv=csv, show=show)

    def duracion_en_perceniles(self, save=True, csv=False, show=False):
        """
            Duracion en Perceniles
        """
        self.reportdata.duration.quantile(
            [.1 * i for i in range(1, 11)]).plot(kind='line')
        #plt.title('Duracion de en percentiles')
        plt.xlabel("Percentil")
        plt.ylabel("Duracion en minutos")
        self.__wrpsave(
            self.duracion_en_perceniles.__name__, save=save, csv=csv, show=show)

    def cant_anomalias_xcorredores(self, save=True, csv=False, show=False):
        """
            Cantidad de anomalias por corredor
        """
        self.aux = self.reportdata.copy()
        self.aux = self.aux.groupby(
            ["corr_name", "sentido"]).size().reset_index().rename(columns={0: "size"})
        f, axarr = plt.subplots(1, 2, sharey=True)
        self.aux[self.aux["sentido"] == "centro"].plot(
            x="corr_name", kind="barh", ax=axarr[0])
        self.aux[self.aux["sentido"] == "provincia"].plot(
            x="corr_name", kind="barh", ax=axarr[1])
        plt.xlabel('Duracion en minutos')
        plt.ylabel('Nombre Corredor')
        self.__wrpsave(
            self.cant_anomalias_xcorredores.__name__, save=save, csv=csv, show=show)

    def indice_anomalias_xcuadras(self, save=True, csv=False, show=False):
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
        #display(self.aux[["corr_name", "sentido", "indice", "cuadras", "anomalias"]])
        #sns.barplot(x="corr_name", y="indice", hue="sentido", data=self.aux)
        sns.factorplot(x="corr_name", y="indice", data=self.aux,
                       hue="sentido", kind="bar", size=4, aspect=2)
        plt.xticks(rotation=12, size="8")
        plt.ylabel('Duracion en minutos')
        plt.xlabel('')
        self.__wrpsave(
            self.indice_anomalias_xcuadras.__name__, save=save, csv=csv, show=show)

    def __asignacion_frame(self):
        # def asignacion_frame(self, tabla=Estadisticas, **args):
        """
           valids = asignacion_frame(
               'anomaly', col1="id", col2="timestamp_end", col3="timestamp_end")
           # parse_dates={"timestamp_asignacion": (lambda X: "" if X == None
           # else X)}
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

        #self.valids = pd.read_sql_table(Estadisticas, conn_sql._instanceSQL__engine)
        #, columns=columns)
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
