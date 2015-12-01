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

import random
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
import pygal

from pygal.style import *
from dashboard_logging import dashboard_logging
logger = dashboard_logging(config="logging.json", name=__name__)
logger.info("inicio planificacion - generacion de graficos")

conn_sql = instanceSQL(cfg=config)
conn_sql.createDBEngine()

Estadisticas = conn_sql.instanceTable(unique_table='estadisticas')
Anomaly = conn_sql.instanceTable(unique_table='anomaly')
Historical = conn_sql.instanceTable(unique_table='historical')
Corredores = conn_sql.instanceTable(unique_table='corredores')

style_planificacion = Style(
    plot_background='#FFFFFF',
    label_font_size=16
)


class GraficosPlanificacion(object):

    def __init__(self):

        self.query_all = None
        self.metadata = []
        self.savepath_folder = os.path.abspath(".") + "/static/graficos/{0}/"
        self._mkdir(self.savepath_folder.replace("/{0}/", "/"))
        self.session = conn_sql.session()
        self.name_corredor = None
        # import pdb
        # pdb.set_trace()
        tabla_corredores = self.session.query(Corredores)
        self.corredores = list(
            set([c.corredor.lower().replace(" ", "_") for c in tabla_corredores if c]))

        self.timestamp_end = datetime.datetime.now()
        self.timestamp_start = self.timestamp_end - datetime.timedelta(weeks=4)

        self.__mkdir(self.savepath_folder, [
                     'mensuales', 'corredores', "mensuales/csv", "mensuales/svg"])
        self.__mkdir(self.savepath_folder, [
                     "corredores/{0}".format(c) for c in self.corredores if c])

        for f in ['svg', 'csv']:
            self.__mkdir(self.savepath_folder, [
                         "corredores/{0}/{1}".format(key, f) for key in self.corredores if key])

        append_date = "{0}_{1}".format(
            str(self.timestamp_start.date()).replace("-", ""),
            str(self.timestamp_end.date()).replace("-", "")
        )

        self.folders = {
            "corredores": {
                "svg": "corredores/{0}/svg/" + append_date,
                "csv": "corredores/{0}/csv/" + append_date
            },
            "mensuales": {
                "svg": "mensuales/svg/" + append_date,
                "csv": "mensuales/csv/" + append_date
            }
        }

        for f in ['svg', 'csv']:
            self.__mkdir(self.savepath_folder, [self.folders['mensuales'][f]])
            self.__mkdir(self.savepath_folder, [
                         self.folders['corredores'][f].format(c) for c in self.corredores if c])

        self.__flg = False
        self.corrdata = []
        self.valids = {}
        self.reportdata = None
        self.aux = None

        for (idseg, data) in misc_helpers.corrdata.items():
            d = data.copy()
            d["iddevice"] = idseg
            self.corrdata += [d]

        self.mensuales = {
            "anomalias_ultimo_mes": "Cantidad total de anomalias en las ultimas 4 semanas",
            "duracion_media_anomalias": "Duracion media de anomalias por corredor",
            "duracion_en_percentiles": "Duracion en Percentil",
            "cant_anomalias_xcorredores_capital": "Cantidad de anomalias por corredor - Sentido Capital",
            "cant_anomalias_xcorredores_provincia": "Cantidad de anomalias por corredor - Sentido Provincia",
            "indice_anomalias_xcuadras": "Indice de anomalias por cuadra",
            "distribucion_horaria_sumarizada_laborables": "Distribucion horaria sumarizada - Dias Laborables",
            "distribucion_horaria_sumarizada_sabado": "Distribucion horaria sumarizada - Sabado",
            "distribucion_horaria_sumarizada_domingo": "Distribucion horaria sumarizada - Domingo",
            "duracion_anomalias_media_xfranjahoraria_laborables": "Duracion media de anomalias por franja horaria - Dias Laborables",
            "duracion_anomalias_media_xfranjahoraria_fin_de_semana": "Duracion media de anomalias por franja horaria - Fin de Semana"
        }

        self.folders['mensuales']['svg'] = self.savepath_folder.replace(
            "{0}/",  "") + self.folders['mensuales']['svg']
        self.folders['mensuales']['csv'] = self.savepath_folder.replace(
            "{0}/",  "") + self.folders['mensuales']['csv']
        self.folders['corredores']['svg'] = self.savepath_folder.replace(
            "{0}/",  "") + self.folders['corredores']['svg']
        self.folders['corredores']['csv'] = self.savepath_folder.replace(
            "{0}/",  "") + self.folders['corredores']['csv']

        self.corredores = {}

        self.__grp = {
            'mensuales': self.mensuales.keys(),
            'corredores': self.corredores.keys()
        }

        self.valids = self.__asignacion_frame(
            table=Anomaly, column=Anomaly.timestamp_start)
        self.historico = self.__asignacion_frame(
            table=Historical, column=Historical.timestamp)        
        self.__generacion_dataframe()

    def _mkdir(self, folder):
        # print folder
        if not os.path.exists(folder):
            logger.info("inicio creacion de carpeta {0}".format(folder))
            os.mkdir(folder)

    def __mkdir(self, path, folders):

        for folder in folders:
            __folder = path.format(folder)
            self._mkdir(__folder)

    def generacion_graficos(self, tipo="mensuales"):
        """
           grafico.generacion_graficos(tipo="mensuales")
           grafico.generacion_graficos(tipo="corredores")
        """
        if tipo == "mensuales":
            mensuales = ["anomalias_ultimo_mes", "duracion_media_anomalias", "distribucion_horaria_sumarizada",
                         "duracion_anomalias_media_xfranjahoraria", "duracion_en_percentiles", "cant_anomalias_xcorredores", "indice_anomalias_xcuadras"]

        for grafico in mensuales:
            eval("self.{0}()".format(grafico))

    def generador_csv(self, filename, tipo="mensuales", corredor=None):

        filesave = self.folders[tipo]['csv'] + "/" + filename
        if tipo == "corredores":
            filesave = self.folders[tipo]['csv'].format(
                corredor) + "/" + filename.replace("svg", "csv")
        self.aux.to_csv(filesave)

    def guardar_grafico(self, grafico={}, instancegraph=True):
        """
            grafico.guardar_grafico(grafico={'idg': 'aum3028', 'timestamp_start': datetime.date(2015, 9, 30),
                'timestamp_end': datetime.date(2015, 10, 28), 'name': 'Cantidad total de anomalias en las ultimas 4 semanas',
                'filename': 'anomalias_ultimo_mes_2015_09_30_2015_10_28.png'})
        """
       # import pdb
       # pdb.set_trace()
        if grafico.get("tipo") != "mensuales":
            filesave = self.folders["corredores"]['svg'].format(
                self.name_corredor) + "/" + grafico.get("filename")
        else:
            filesave = self.folders["mensuales"][
                'svg'] + "/" + grafico.get("filename")
        # filesave = self.savepath_file.format(grafico.get("filename"))
        query = self.session.query(Estadisticas)
        if_count_id = query.filter(
            Estadisticas.idg == grafico.get("idg")).count()
        if not if_count_id:
            nuevo_grafico = Estadisticas(
                idg=grafico.get("idg"), name=grafico.get('name'), filename=filesave.replace(os.path.abspath(".") + "/static/", "/_static/"),
                timestamp_start=grafico.get('timestamp_start'), timestamp_end=grafico.get('timestamp_end'), tipo_grafico=grafico.get("tipo").lower()
            )
            self.session.add(nuevo_grafico)
            self.session.commit()
        if not os.path.exists(filesave):
            if instancegraph == True:
                grafico.get("instancegraph").render_to_file(filesave)
            # plt.savefig(filesave, format='png')

    def __instanciar_save(self, **args):
        params = args.get('params')
        if args.get("ifcsv") == True:
            self.generador_csv(params.get("filename"), tipo="mensuales")
        if args.get("ifsave"):
            self.guardar_grafico(grafico=params)
        if args.get("ifshow") == True:
            pass
            # plt.show()
        # plt.close()

    def __wrpsave(self, name_func, **args):
        metadata = self.generar_metadata(name=name_func)
        metadata.update({'instancegraph': args.get('graph')})
        self.__instanciar_save(ifsave=args.get("save"), ifcsv=args.get(
            "csv"), ifshow=args.get("show"), params=metadata)

    def make_id(self, idn):
        start = self.timestamp_start.date()
        end = self.timestamp_end.date()
        idn_f = ['a' + str(x)
                 for x in range(200) if x][random.randrange(0, 199)]
        if len(idn) == 3:
            return "{0}{1}{2}{3}{4}".format(idn_f, idn[1][0], idn[2][0], str(start).replace("-", ""), end.day)
        elif len(idn) == 4:
            return "{0}{1}{2}{3}{4}{5}".format(idn[0][0], idn_f, idn[2][0], idn[3][0], str(start).replace("-", ""), end.day)
        elif len(idn) > 5:
            return "{0}{1}{2}{3}{4}{5}{6}".format(idn[0][0], idn[1][0], idn[2][0], idn[3][0], idn_f, str(start).replace("-", ""), end.day)
        else:
            return "{0}{1}{2}{3}".format(idn[0][0], idn_f, str(start).replace("-", ""), end.day)

    def generar_metadata(self, name, tipo="mensuales", corredor=None):
        """
            grafico.generar_metadata(name=grafico.anomalias_ultimo_mes.__name__)
            Params
                name: Nombre del metodo que genera el grafico, segun el tipo, se guarda en self.mensuales o self.semanales| dic
        """
        start = self.timestamp_start.date()
        end = self.timestamp_end.date()
        filename = "{0}_{1}_{2}.svg".format(
            name, str(start).replace("-", "_"), str(end).replace("-", "_"))
        idn = name.split("_")
        query = self.session.query(Estadisticas)
        while True:
            _id = self.make_id(idn)
            if_count_id = query.filter(Estadisticas.idg == _id).count()
            if if_count_id == 0:
                break
        if tipo == "corredores":
            tipo = corredor
        metadata_grafico = {
            "idg": _id,
            "tipo": tipo,
            "name": self.mensuales.get(name, ''),
            "filename": filename,
            "timestamp_start": start,
            "timestamp_end": end
        }
        self.metadata.append(metadata_grafico)
        return metadata_grafico

    def anomalias_ultimo_mes(self, save=True, csv=True, tipo='mensual', corredor=None, show=False):
        """
            Cantidad total de anomalias en las ultimas 4 semanas
            grafico.anomalias_ultimo_mes(save=False, csv=True, show=True)
        """

        if tipo == 'mensual':
            self.aux = self.reportdata.copy()
            name = self.mensuales[self.anomalias_ultimo_mes.__name__]
            sentidos = list(set(self.aux['sentido']))
        elif tipo == "corredores":
            self.aux = self.reportdata.copy()
            if corredor in list(set(self.reportdata['corr_name'])):
                self.aux = self.aux[self.aux['corr_name'] == corredor]
                sentidos = list(set(self.aux['sentido']))
                self.name_corredor = corredor.replace(" ", "_").lower()
                name = self.name_corredor + "_" + \
                    self.anomalias_ultimo_mes.__name__
            else:
                raise Exception("Corredor Inexistente")

        sentidos.sort()
        self.aux = self.aux.groupby(
            [self.aux["timestamp_start"].dt.week, self.aux["sentido"]]).size()
        self.aux = self.aux.reset_index().rename(
            columns={"level_0": "semana", 0: "count"})
        self.aux = self.aux.pivot(
            index='semana', columns='sentido', values='count').reset_index()
        self.aux.columns.name = "Referencia"
        if sentidos == ["centro", "provincia"]:
            self.aux["promedio"] = (
                self.aux["centro"] + self.aux["provincia"]) / len(sentidos)
        else:
            self.aux["promedio"] = self.aux[sentidos[0]]
        self.aux["semana"] = self.aux["semana"].astype(str)
        # .plot(x='semana', color="r")
        self.ax = self.aux[["semana", "promedio"]]
        # .plot(x='semana', kind='bar', ax=self.ax)
        self.ax = self.aux[['semana'] + sentidos]

        line_chart = pygal.Bar(no_data_text='Sin Datos', include_x_axis=True, style=style_planificacion,
                               x_title='Semanas', y_title='Cantidad')
        line_chart.x_labels = list(self.aux['semana'])

        def set_value(x):
            if str(x) == 'nan':
                x = 0
            return int(x)

        if sentidos == ["centro", "provincia"]:
            line_chart.add('Capital', map(set_value, self.aux['centro']))
            line_chart.add('Provincia', map(set_value, self.aux['provincia']))
        elif sentidos == ["centro"]:
            line_chart.add('Capital', map(set_value, self.aux['centro']))
        elif sentidos == ["provincia"]:
            line_chart.add('Provincia', map(set_value, self.aux['provincia']))
        else:
            raise Exception("Corredor sin Sentidos")

        if tipo == "mensual":
            self.__wrpsave(self.anomalias_ultimo_mes.__name__,
                           graph=line_chart, save=save, csv=csv, show=show)
        else:
            metadata = self.generar_metadata(
                name, tipo='corredores', corredor=corredor)
            metadata['name'] = corredor + " " + \
                self.mensuales[self.anomalias_ultimo_mes.__name__]
            self.generador_csv(
                metadata.get("filename"), tipo="corredores", corredor=self.name_corredor)
            self.guardar_grafico(metadata, instancegraph=False)
            line_chart.render_to_file(self.folders['corredores']['svg'].format(
                self.name_corredor) + "/" + metadata.get("filename"))

    def duracion_media_anomalias(self, save=True, csv=True, tipo='mensual', corredor=None, show=False):
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
        x_label_rotation = 90
        sentidos = list(set(self.aux['sentido']))
        if tipo == 'corredores':
            if corredor in list(set(self.reportdata['corr_name'])):
                self.aux = self.aux[self.aux['corr_name'] == corredor]
                sentidos = list(set(self.aux['sentido']))
                self.name_corredor = corredor.replace(" ", "_").lower()
                name = self.name_corredor + "_" + \
                    self.duracion_media_anomalias.__name__
                x_label_rotation = 0
            else:
                raise Exception("Corredor Inexistente")

        sentidos.sort()
        lcent, lprov = [], []

        def set_items(array, sentido):
            for key, value in lc.iteritems():
                if sentido in value.keys():
                    array.append(value[sentido])
                else:
                    array.append(None)
            return array

        lc = {c: {} for c in list(self.aux['corr_name']) if c}
        for co in lc.keys():
            lc[co] = dict(self.aux[self.aux['corr_name'] == co].groupby(
                ['sentido', 'duration'])['duration'].all().to_dict().keys())

        bar_chart = pygal.Bar(no_data_text='Sin Datos', y_title='Duracion en Minutos',
                              style=style_planificacion, x_label_rotation=x_label_rotation)
        bar_chart.x_labels = list(set(self.aux['corr_name']))

        if sentidos == ["centro", "provincia"]:
            bar_chart.add('Capital', set_items(lcent, 'centro'))
            bar_chart.add('Provincia', set_items(lprov, 'provincia'))
        elif sentidos == ["centro"]:
            bar_chart.add('Capital', set_items(lcent, 'centro'))
        elif sentidos == ["provincia"]:
            bar_chart.add('Provincia', set_items(lprov, 'provincia'))
        else:
            raise Exception("Corredor sin Sentidos")

        if tipo == "mensual":
            self.__wrpsave(self.duracion_media_anomalias.__name__,
                           graph=bar_chart, save=save, csv=csv, show=show)
        else:
            metadata = self.generar_metadata(
                name, tipo='corredores', corredor=corredor)
            metadata['name'] = corredor + " " + \
                self.mensuales[self.duracion_media_anomalias.__name__]
            self.generador_csv(
                metadata.get("filename"), tipo="corredores", corredor=self.name_corredor)
            self.guardar_grafico(metadata, instancegraph=False)
            bar_chart.render_to_file(self.folders['corredores']['svg'].format(
                self.name_corredor) + "/" + metadata.get("filename"))

    def distribucion_horaria_sumarizada(self, save=True, csv=True, tipo='mensual', corredor=None, show=False):
        """
            Distribucion horaria sumarizada
        """

        self.aux = self.reportdata.copy()
        self.aux["Franja Horaria"] = self.aux["timestamp_start"].dt.hour
        self.aux = self.aux.rename(columns={'daytype': 'Tipos de Dias'})
        rplc = self.aux['Tipos de Dias'].str.replace(
            "workingday", "Dias Laborables")
        rplc = rplc.str.replace("saturday", "Sabado")
        rplc = rplc.str.replace("sunday", "Domingo")
        self.aux['Tipos de Dias'] = rplc

        sentidos = list(set(self.aux['sentido']))
        if tipo == 'corredores':
            if corredor in list(set(self.reportdata['corr_name'])):
                self.aux = self.aux[self.aux['corr_name'] == corredor]
                sentidos = list(set(self.aux['sentido']))
                self.name_corredor = corredor.replace(" ", "_").lower()
                x_label_rotation = 0
            else:
                raise Exception("Corredor Inexistente")
        sentidos.sort()

        diaslaborables = self.aux[
            self.aux['Tipos de Dias'] == 'Dias Laborables']
        sabado = self.aux[self.aux['Tipos de Dias'] == 'Sabado']
        domingo = self.aux[self.aux['Tipos de Dias'] == 'Domingo']

        def set_franja(franja):
            franja_horaria = {i: 0 for i in range(0, 25) if i}
            for key in franja_horaria.keys():
                if key in franja.keys():
                    franja_horaria[key] = franja[key]
            return franja_horaria

        def make_bar(tipodia, name_dia):

            bar_chart = pygal.Bar(y_title="Cantidad",
                                  style=style_planificacion)
            bar_chart.x_labels = map(lambda x: str(x), range(1, 25))

            franjacentro = tipodia[tipodia['sentido'] == 'centro'][
                'Franja Horaria'].value_counts().to_dict()
            franjaprovincia = tipodia[tipodia['sentido'] == 'provincia'][
                'Franja Horaria'].value_counts().to_dict()

            if sentidos == ["centro", "provincia"]:
                bar_chart.add('Capital', set_franja(franjacentro).values())
                bar_chart.add(
                    'Provincia', set_franja(franjaprovincia).values())
            elif sentidos == ["centro"]:
                bar_chart.add('Capital', set_franja(franjacentro).values())
            elif sentidos == ["provincia"]:
                bar_chart.add(
                    'Provincia', set_franja(franjaprovincia).values())
            else:
                raise Exception("Corredor sin Sentidos")

            if tipo == "mensual":
                name_m = self.distribucion_horaria_sumarizada.__name__ + \
                    "_" + name_dia
                self.__wrpsave(
                    name_m, graph=bar_chart, save=save, csv=csv, show=show)
            else:
                name = self.name_corredor + "_" + \
                    self.distribucion_horaria_sumarizada.__name__ + \
                    "_" + name_dia
                metadata = self.generar_metadata(
                    name, tipo='corredores', corredor=corredor)
                metadata['name'] = corredor + " " + self.mensuales[
                    self.distribucion_horaria_sumarizada.__name__ + "_" + name_dia]
                self.generador_csv(
                    metadata.get("filename"), tipo="corredores", corredor=self.name_corredor)
                self.guardar_grafico(metadata, instancegraph=False)
                bar_chart.render_to_file(self.folders['corredores']['svg'].format(
                    self.name_corredor) + "/" + metadata.get("filename"))

        make_bar(diaslaborables, "laborables")
        make_bar(sabado, "sabado")
        make_bar(domingo, "domingo")

    def duracion_anomalias_media_xfranjahoraria(self, save=True, csv=True, tipo='mensual', corredor=None, show=False, franjas=[]):
        """
            Duracion media de anomalias por franja horaria
        """

        if tipo == "mensual":
            self.aux = self.reportdata.copy()
        else:
            if corredor in list(set(self.reportdata['corr_name'])):
                self.aux = self.reportdata.copy()
                self.aux = self.aux[self.aux['corr_name'] == corredor]
                sentidos = list(set(self.aux['sentido']))
                self.name_corredor = corredor.replace(" ", "_").lower()
            else:
                raise Exception("Corredor Inexistente")

        if franjas == []:
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

        self.aux["franja"] = self.aux["franja"].astype(int)
        self.aux = self.aux.rename(
            columns={'daytype': 'Tipos de Dias', 'duration': 'Duracion en Minutos'})
        self.aux.loc[self.aux["Tipos de Dias"].isin(
            ["saturday", "sunday"]), "Tipos de Dias"] = "weekend"
        rplc = self.aux['Tipos de Dias'].str.replace(
            "workingday", "Dias Laborables")
        rplc = rplc.str.replace("weekend", "Fin de Semana")
        self.aux['Tipos de Dias'] = rplc

        diaslaborables = self.aux[
            self.aux['Tipos de Dias'] == 'Dias Laborables']
        findesemana = self.aux[self.aux['Tipos de Dias'] == 'Fin de Semana']

        def make_box(franja, name_dia):
            box_plot = pygal.Box(
                no_data_text='Sin Datos', y_title='Duracion en Minutos', style=style_planificacion)

            box_plot.add(
                '00hs - 07hs', list(franja[franja['franja'] == 0]['Duracion en Minutos']))
            box_plot.add(
                '07hs - 10hs', list(franja[franja['franja'] == 1]['Duracion en Minutos']))
            box_plot.add(
                '10hs - 17hs', list(franja[franja['franja'] == 2]['Duracion en Minutos']))
            box_plot.add(
                '17hs - 20hs', list(franja[franja['franja'] == 3]['Duracion en Minutos']))
            box_plot.add(
                '20hs - 24hs', list(franja[franja['franja'] == 4]['Duracion en Minutos']))
            name_dia = name_dia.replace(" ", "_")
            if tipo == "mensual":
                name_m = self.duracion_anomalias_media_xfranjahoraria.__name__ + \
                    "_" + name_dia
                self.__wrpsave(
                    name_m, graph=box_plot, save=save, csv=csv, show=show)
            else:
                name = self.name_corredor + "_" + \
                    self.duracion_anomalias_media_xfranjahoraria.__name__ + \
                    "_" + name_dia
                metadata = self.generar_metadata(
                    name, tipo='corredores', corredor=corredor)
                metadata['name'] = corredor + " " + self.mensuales[
                    self.duracion_anomalias_media_xfranjahoraria.__name__ + "_" + name_dia]
                self.generador_csv(
                    metadata.get("filename"), tipo="corredores", corredor=self.name_corredor)
                self.guardar_grafico(metadata, instancegraph=False)
                box_plot.render_to_file(self.folders['corredores']['svg'].format(
                    self.name_corredor) + "/" + metadata.get("filename"))

        make_box(diaslaborables, 'laborables')
        make_box(findesemana, 'fin de semana')

    def duracion_en_percentiles(self, save=True, csv=True, tipo='mensual', corredor=None, show=False):
        """
            Duracion en Perceniles
        """
        if tipo == "mensual":
            self.aux = self.reportdata.duration.quantile(
                [.1 * i for i in range(1, 11)])
        else:
            if corredor in list(set(self.reportdata['corr_name'])):
                self.aux = self.reportdata[
                    self.reportdata['corr_name'] == corredor]
                self.aux = self.aux.duration.quantile(
                    [.1 * i for i in range(1, 11)])
                self.name_corredor = corredor.replace(" ", "_").lower()
            else:
                raise Exception("Corredor Inexistente")

        def formatTime(x):
            x = int(x)
            s = "%s" % (x / 60)
            if (x % 60) != 0:
                s = "%s %s" % (s, x % 60)
            return s

        x = [.1 * i for i in range(1, 11)]
        y = list(self.aux)
        line_chart = pygal.Line(style=style_planificacion)
        line_chart.x_labels = x
        line_chart.x_title = 'Percentil'
        line_chart.y_title = 'Duracion en Minutos'
        line_chart.add("Duracion", map(lambda x: int(x), y))

        if tipo == "mensual":
            self.__wrpsave(self.duracion_en_percentiles.__name__,
                           graph=line_chart, save=save, csv=csv, show=show)
        else:
            name = self.name_corredor + "_" + \
                self.duracion_en_percentiles.__name__
            metadata = self.generar_metadata(
                name, tipo='corredores', corredor=corredor)
            metadata['name'] = corredor + " " + \
                self.mensuales[self.duracion_en_percentiles.__name__]
            self.generador_csv(
                metadata.get("filename"), tipo="corredores", corredor=self.name_corredor)
            self.guardar_grafico(metadata, instancegraph=False)
            line_chart.render_to_file(self.folders['corredores']['svg'].format(
                self.name_corredor) + "/" + metadata.get("filename"))

    def cant_anomalias_xcorredores(self, save=True, csv=True, show=False):
        """
            Cantidad de anomalias por corredor
        """
        self.aux = self.reportdata.copy()
        self.aux = self.aux.groupby(["corr_name", "sentido"]).size().reset_index().rename(
            columns={0: "cantidad", "corr_name": "corredor"})
        centro = self.aux[self.aux["sentido"] == "centro"].groupby(
            ['corredor', 'cantidad']).all().reset_index()[['corredor', 'cantidad']]
        provincia = self.aux[self.aux["sentido"] == "provincia"].groupby(
            ['corredor', 'cantidad']).all().reset_index()[['corredor', 'cantidad']]

        def add_chart(sentido, name):
            bar_chart = pygal.HorizontalBar(
                no_data_text='Sin Datos', x_title='Sentido {0}'.format(name.title()), style=style_planificacion)
            for key in sentido.values:
                bar_chart.add(key[0], key[1])

            name = self.cant_anomalias_xcorredores.__name__ + \
                "_" + name.replace(" ", "_")
            self.__wrpsave(
                name, graph=bar_chart, save=save, csv=csv, show=show)

        add_chart(centro, 'capital')
        add_chart(provincia, 'provincia')

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
        lcent, lprov = [], []

        def set_items(array, sentido):
            for key, value in lc.iteritems():
                if sentido in value.keys():
                    array.append(value[sentido])
                else:
                    array.append(None)
            return array

        lc = {c: {} for c in list(self.aux['corr_name']) if c}
        for co in lc.keys():
            lc[co] = dict(self.aux[self.aux['corr_name'] == co].groupby(
                ['sentido', 'indice'])['indice'].all().to_dict().keys())
        bar_chart = pygal.Bar(no_data_text='Sin Datos', y_title='Indice',
                              style=style_planificacion, x_label_rotation=90)
        bar_chart.x_labels = list(set(self.aux['corr_name']))
        bar_chart.add('Provincia', set_items(lprov, 'provincia'))
        bar_chart.add('Capital', set_items(lcent, 'centro'))
        self.__wrpsave(self.indice_anomalias_xcuadras.__name__,
                       graph=bar_chart, save=save, csv=csv, show=show)

    def __asignacion_frame(self, **config):
        """
           valids = asignacion_frame(
               'anomaly', col1="id", col2="timestamp_end", col3="timestamp_end")
           # parse_dates={"timestamp_asignacion": (lambda X: "" if X == None
           # else X)}
        """
        Table = config.pop("table")
        Column = config.pop("column")
        self.query = self.session.query(Table)
        result = pd.read_sql(self.query.filter(
            Column >= self.timestamp_start).statement, self.query.session.bind)
        return result

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
        self.corredores = list(set(self.reportdata['corr_name']))


def main():

    grafico = GraficosPlanificacion()
    logger.info("Generando Grafico Generales periodo {0} - {1}".format(
        grafico.timestamp_start, grafico.timestamp_end))
    grafico.generacion_graficos()
    logger.info(
        "-------------------------------------------------------------------")
    logger.info("Generando Grafico por Corredor periodo {0} - {1}".format(
        grafico.timestamp_start, grafico.timestamp_end))
    for nombre_corredor in grafico.corredores:
        logger.info("Corredor {0} - Grafico {1}".format(nombre_corredor,
                                                        grafico.mensuales[grafico.anomalias_ultimo_mes.__name__]))
        grafico.anomalias_ultimo_mes(
            tipo="corredores", corredor=nombre_corredor)
        logger.info("Corredor {0} - Grafico {1}".format(nombre_corredor,
                                                        grafico.mensuales[grafico.duracion_media_anomalias.__name__]))
        grafico.duracion_media_anomalias(
            tipo="corredores", corredor=nombre_corredor)
        logger.info(
            "Corredor {0} - Grafico {1}".format(nombre_corredor, "Distribucion horaria sumarizada"))
        grafico.distribucion_horaria_sumarizada(
            tipo="corredores", corredor=nombre_corredor)
        logger.info("Corredor {0} - Grafico {1}".format(nombre_corredor,
                                                        "Duracion media de anomalias por franja horaria"))
        grafico.duracion_anomalias_media_xfranjahoraria(
            tipo="corredores", corredor=nombre_corredor)
        logger.info("Corredor {0} - Grafico {1}".format(nombre_corredor,
                                                        grafico.mensuales[grafico.duracion_en_percentiles.__name__]))
        grafico.duracion_en_percentiles(
            tipo="corredores", corredor=nombre_corredor)
    logger.info(
        "-------------------------------------------------------------------")
    logger.info("Graficos Generados")

if __name__ == '__main__':
    main()
