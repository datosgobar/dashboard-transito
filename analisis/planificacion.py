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
import pygal

from pygal.style import *

conn_sql = instanceSQL(cfg=config)
conn_sql.createDBEngine()

Estadisticas = conn_sql.instanceTable(unique_table='estadisticas')
Anomaly = conn_sql.instanceTable(unique_table='anomaly')
Historical = conn_sql.instanceTable(unique_table='historical')


class GraficosPlanificacion(object):

    def __init__(self):

        self.query_all = None
        self.metadata = []
        self.savepath_folder = os.path.abspath(".") + "/static/graficos/{0}/"
        self._mkdir(self.savepath_folder.replace("/{0}/", "/"))

        self.timestamp_end = datetime.datetime.now()
        self.timestamp_start = self.timestamp_end - datetime.timedelta(weeks=8)

        self.__mkdir(self.savepath_folder, ['csv', 'svg'])

        self.savepath_folder = self.savepath_folder + "{0}_{1}".format(
            str(self.timestamp_start.date()).replace("-", ""),
            str(self.timestamp_end.date()).replace("-", "")
        )

        self.__mkdir(self.savepath_folder, ['csv', 'svg'])

        self.savepath_file = self.savepath_folder.format('svg') + "/{0}"
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
            "duracion_en_perceniles": "Duracion en Percentil",
            "cant_anomalias_xcorredores_capital": "Cantidad de anomalias por corredor - Sentido Capital",
            "cant_anomalias_xcorredores_provincia": "Cantidad de anomalias por corredor - Sentido Provincia",
            "indice_anomalias_xcuadras": "Indice de anomalias por cuadra",
            "distribucion_horaria_sumarizada_laborables": "Distribucion horaria sumarizada - Dias Laborables",
            "distribucion_horaria_sumarizada_sabado": "Distribucion horaria sumarizada - Sabado",
            "distribucion_horaria_sumarizada_domingo": "Distribucion horaria sumarizada - Domingo",
            "duracion_anomalias_media_xfranjahoraria_laborables": "Duracion media de anomalias por franja horaria - Dias Laborables",
            "duracion_anomalias_media_xfranjahoraria_fin_de_semana": "Duracion media de anomalias por franja horaria - Fin de Semana",
            "duracion_anomalias_xfranjahoraria_laborables": "Duracion de anomalias por franja horaria - Dias Laborables",
            "duracion_anomalias_xfranjahoraria_fin_de_semana": "Duracion de anomalias por franja horaria - Fin de Semana",
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
           grafico.generacion_graficos(tipo="corredores")
        """
        if tipo == "mensuales":
            mensuales = ["anomalias_ultimo_mes", "duracion_media_anomalias", "distribucion_horaria_sumarizada", "duracion_anomalias_xfranjahoraria", "duracion_anomalias_media_xfranjahoraria", "duracion_en_perceniles", "cant_anomalias_xcorredores", "indice_anomalias_xcuadras"]

        for grafico in mensuales:
            eval("self.{0}()".format(grafico))

    def generador_csv(self, filename, tabla):

        filesave = self.savepath_csv.format(filename.replace(".svg", ".csv"))
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
            grafico.get("instancegraph").render_to_file(filesave)
            #plt.savefig(filesave, format='png')

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
        metadata.update({'instancegraph':args.get('graph')})
        self.__instanciar_save(ifsave=args.get("save"), ifcsv=args.get("csv"), ifshow=args.get("show"), params=metadata)

    def generar_metadata(self, name):
        """
            grafico.generar_metadata(name=grafico.anomalias_ultimo_mes.__name__)
            Params
                name: Nombre del metodo que genera el grafico, segun el tipo, se guarda en self.mensuales o self.semanales| dic
        """
        start = self.timestamp_start.date()
        end = self.timestamp_end.date()
        filename = "{0}_{1}_{2}.svg".format(name, str(start).replace("-", "_"), str(end).replace("-", "_"))
        idn = name.split("_")
        if len(idn) == 3:
            _id = "{0}{1}{2}{3}{4}".format(idn[0][0], idn[1][0], idn[2][0], str(start).replace("-", ""), end.day)
        elif len(idn) > 3:
            _id = "{0}{1}{2}{3}{4}{5}".format(idn[0][0], idn[1][0], idn[2][0], idn[3][0], str(start).replace("-", ""), end.day)
        else:
            _id = "{0}{1}{2}{3}{4}{5}".format(idn[0][0], idn[0][1], str(start).replace("-", ""), end.day)
        metadata_grafico = {
            "idg": _id,
            "name": self.mensuales[name],
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
            name = self.anomalias_ultimo_mes.__name__
        else:
            corredor = "Juan B. Justo"
            self.aux = self.reportdata.copy()
            self.aux = self.aux[self.aux['corr_name'] == corredor]
            name = self.anomalias_ultimo_mes.__name__ + "_" + corredor

        self.aux = self.aux.groupby(
            [self.aux["timestamp_start"].dt.week, self.aux["sentido"]]).size()
        self.aux = self.aux.reset_index().rename(
            columns={"level_0": "semana", 0: "count"})
        self.aux = self.aux.pivot(
            index='semana', columns='sentido', values='count').reset_index()
        self.aux.columns.name = "Referencia"
        self.aux["promedio"] = (self.aux["centro"] + self.aux["provincia"]) / 2
        self.aux["semana"] = self.aux["semana"].astype(str)
        # .plot(x='semana', color="r")
        self.ax = self.aux[["semana", "promedio"]]
        # .plot(x='semana', kind='bar', ax=self.ax)
        self.ax = self.aux[["semana", "centro", "provincia"]]

        CustomGraph = LightGreenStyle(background='white')
        custom_style = Style(label_font_size=12, background='transparent')
        line_chart = pygal.Bar(no_data_text='Sin Datos', include_x_axis=True, tyle=CleanStyle(no_data_font_size=40),
                               tooltip_border_radius=10, x_title='Semanas', human_readable=False, y_title='Duracion en Minutos', width=600, height=400,
                               legend_at_bottom=True, fill=False, interpolate='cubic', style=CustomGraph, stroke_style={'width': 2},
                               explicit_size=True, show_y_guides=True)
        line_chart.x_labels = list(self.aux['semana'])

        def set_value(x):
            if str(x) == 'nan':
                x = 0
            return int(x)

        line_chart.add('Capital', map(set_value, self.aux['centro']))
        line_chart.add('Provincia', map(set_value, self.aux['provincia']))
        self.__wrpsave(name, graph=line_chart, save=save, csv=csv, show=show)

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

        # graph = sns.factorplot(x="corr_name", y="duration", hue='sentido', data=self.aux, kind="bar", size=4, aspect=2.3)
        # graph.set_axis_labels("", "Duracion en Minutos").despine(left=True)
        # graph.despine(left=True)
        # plt.xticks(rotation=17)
        # plt.legend(loc="upper right", frameon=True, fancybox=True, shadow=True)
        # plt.show()

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

        custom_style = Style(label_font_size=12, background='white')
        bar_chart = pygal.Bar(no_data_text='Sin Datos', tooltip_border_radius=10, y_title='Duracion en Minutos',
                              width=700, height=450, legend_at_bottom=True, style=custom_style, explicit_size=True, x_label_rotation=90)
        bar_chart.x_labels = list(set(self.aux['corr_name']))
        bar_chart.add('Provincia', set_items(lprov, 'provincia'))
        bar_chart.add('Capital', set_items(lcent, 'centro'))
        self.__wrpsave(self.duracion_media_anomalias.__name__, graph=bar_chart, save=save, csv=csv, show=show)

    def distribucion_horaria_sumarizada(self, save=True, csv=True, show=False):
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

        def make_bar(tipodia, name):

            franjacentro = tipodia[tipodia['sentido'] == 'centro'][
                'Franja Horaria'].value_counts().to_dict()
            franjaprovincia = tipodia[tipodia['sentido'] == 'provincia'][
                'Franja Horaria'].value_counts().to_dict()

            bar_chart = pygal.Bar(explicit_size=True, width=700, height=450)
            bar_chart.title = 'Distribucion Horaria Sumarizada - {0}'.format(
                name.title())
            bar_chart.x_labels = map(lambda x: str(x), range(1, 25))
            bar_chart.add('provincia', set_franja(franjaprovincia).values())
            bar_chart.add('capital', set_franja(franjacentro).values())
            name = self.distribucion_horaria_sumarizada.__name__  + "_" + name.replace(" ", "_")
            self.__wrpsave(name, graph=bar_chart, save=save, csv=csv, show=show)

        make_bar(diaslaborables, "laborables")
        make_bar(sabado, "sabado")
        make_bar(domingo, "domingo")
        # sns.factorplot("Franja Horaria", col="Tipos de Dias",hue="sentido", kind="count", data=self.aux, order=range(0, 24))
        # plt.ylabel("Duracion en Minutos")

    def duracion_anomalias_xfranjahoraria(self, save=True, csv=False, show=False):
        """
            Duracion de anomalias por franja horaria
        """
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

        self.aux["franja"] = self.aux["franja"].astype(int)

        self.aux.loc[self.aux["daytype"] == "saturday", "daytype"] = "weekend"
        self.aux.loc[self.aux["daytype"] == "sunday", "daytype"] = "weekend"
        self.aux = self.aux.sort("franja")

        self.aux = self.aux.rename(
            columns={'daytype': 'Tipos de Dias', 'duration': 'Duracion en Minutos'})
        rplc = self.aux['Tipos de Dias'].str.replace(
            "workingday", "Dias Laborables")
        rplc = rplc.str.replace("weekend", "Fin de Semana")
        self.aux['Tipos de Dias'] = rplc

        diaslaborables = self.aux[
            self.aux['Tipos de Dias'] == 'Dias Laborables']
        findesemana = self.aux[self.aux['Tipos de Dias'] == 'Fin de Semana']

        def make_box(franja, name):
            from pygal.style import LightGreenStyle
            custom_style = LightGreenStyle(
                mode='pstdev', label_font_size=12, background='white')
            box_plot = pygal.Box(no_data_text='Sin Datos', fill=True, interpolate='cubic', tooltip_border_radius=10,
                                 width=700, height=450, style=custom_style, explicit_size=True)
            box_plot.title = '{0}'.format(name.title())
            box_plot.add('0hs - 07hs', list(franja[franja['franja'] == 0]['Duracion en Minutos']))
            box_plot.add('07hs - 10hs', list(franja[franja['franja'] == 1]['Duracion en Minutos']))
            box_plot.add('10hs - 17hs', list(franja[franja['franja'] == 2]['Duracion en Minutos']))
            box_plot.add('17hs - 20hs', list(franja[franja['franja'] == 3]['Duracion en Minutos']))
            box_plot.add('20hs - 24hs', list(franja[franja['franja'] == 4]['Duracion en Minutos']))
            
            name = self.duracion_anomalias_xfranjahoraria.__name__ + "_" + name.replace(" ", "_")
            self.__wrpsave(name, graph=box_plot, save=save, csv=csv, show=show)

        make_box(diaslaborables, 'laborables')
        make_box(findesemana, 'fin de semana')
        # sns.factorplot(x="Franja Horaria", y="Duracion en Minutos", col="Tipos de Dias", hue_order=[0, 1, 2, 3, 4], data=self.aux, kind="box")
        # plt.legend(('23hs - 07hs', '08hs - 10hs', '11hs - 17hs', '18hs - 20hs', '21hs - 24hs'), loc="upper right", frameon=True, fancybox=True, shadow=True)
        # ltext = plt.gca().get_legend().get_texts()
        # ltext[0].set_color('b')
        # ltext[1].set_color('g')
        # ltext[2].set_color('r')
        # ltext[3].set_color('m')
        # ltext[4].set_color('y')
        # plt.show()

    def duracion_anomalias_media_xfranjahoraria(self, save=True, csv=True, show=False, **args):
        """
            Duracion media de anomalias por franja horaria
        """
        #sentido = args.pop('sentido')
        #self.aux = self.reportdata[self.reportdata['sentido'] == sentido].copy()
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
                (self.aux["timestamp_start"].dt.hour <= end), "franja"] = i
        self.aux["franja"] = self.aux["franja"].astype(int)
        self.aux = self.aux.rename(
            columns={'daytype': 'Tipos de Dias', 'duration': 'Duracion en Minutos'})
        self.aux.loc[self.aux["Tipos de Dias"].isin(
            ["saturday", "sunday"]), "Tipos de Dias"] = "weekend"
        rplc = self.aux['Tipos de Dias'].str.replace(
            "workingday", "Dias Laborables")
        rplc = rplc.str.replace("weekend", "Fin de Semana")
        self.aux['Tipos de Dias'] = rplc

        diaslaborables = self.aux[self.aux['Tipos de Dias'] == 'Dias Laborables']
        findesemana = self.aux[self.aux['Tipos de Dias'] == 'Fin de Semana']

        def make_box(franja, name):
            custom_style = Style(mode='pstdev', label_font_size=12, background='white')
            box_plot = pygal.Box(no_data_text='Sin Datos', tooltip_border_radius=10,
                                 width=700, height=450, style=custom_style, explicit_size=True)
            box_plot.title = '{0}'.format(name.title())
            box_plot.add('0hs - 07hs', list(franja[franja['franja'] == 0]['Duracion en Minutos']))
            box_plot.add('07hs - 10hs', list(franja[franja['franja'] == 1]['Duracion en Minutos']))
            box_plot.add('10hs - 17hs', list(franja[franja['franja'] == 2]['Duracion en Minutos']))
            box_plot.add('17hs - 20hs', list(franja[franja['franja'] == 3]['Duracion en Minutos']))
            box_plot.add('20hs - 24hs', list(franja[franja['franja'] == 4]['Duracion en Minutos']))
            name = self.duracion_anomalias_media_xfranjahoraria.__name__  + "_" + name.replace(" ", "_")
            self.__wrpsave(name, graph=box_plot, save=save, csv=csv, show=show)

        make_box(diaslaborables, 'laborables')
        make_box(findesemana, 'fin de semana')
        # try:
        #     sns.boxplot(x="Tipos de Dias", y="Duracion en Minutos",
        #                 hue='franja', hue_order=[0, 1, 2, 3, 4], data=self.aux)
        # except:
        #     pass
        # finally:
        #     #
        #     plt.legend(('23hs - 07hs', '08hs - 10hs', '11hs - 17hs',
        #                 '18hs - 20hs', '21hs - 24hs'), loc=(0.01, 0.55))
        #     ltext = plt.gca().get_legend().get_texts()
        #     ltext[0].set_color('b')
        #     ltext[1].set_color('g')
        #     ltext[2].set_color('r')
        #     ltext[3].set_color('m')
        #     ltext[4].set_color('y')
        # plt.show()
        

    def duracion_en_perceniles(self, save=True, tipo='mensual', corredor=None, csv=False, show=False):
        """
            Duracion en Perceniles
        """
        if tipo == 'mensual':
            self.aux = self.reportdata.duration.quantile([.1 * i for i in range(1, 11)])
        else:
            corredor = 'Juan B. Justo'
            self.aux = self.reportdata[
                self.reportdata['corr_name'] == corredor]
            self.aux = self.aux.duration.quantile(
                [.1 * i for i in range(1, 11)])

        # self.aux.plot(kind='line')
        #plt.title('Duracion de en percentiles')

        #vals = [0] + list(self.aux)

        #plt.yticks(np.arange(vals[0], vals[len(vals)-1], self.aux.mean()))

        def formatTime(x):
            x = int(x)
            s = "%s" % (x / 60)
            if (x % 60) != 0:
                s = "%s %s" % (s, x % 60)
            return s

        #plt.gca().set_yticklabels(map(formatTime, vals))
        # plt.xlabel("Percentil")
        #plt.ylabel("Duracion en minutos")
        # plt.show()
        from pygal.style import BlueStyle
        x = [.1 * i for i in range(1, 11)]
        y = list(self.aux)
        custom_style = BlueStyle(label_font_size=12, background='white')
        line_chart = pygal.Line(interpolate='quadratic', interpolation_precision=3, tooltip_border_radius=10,
                                width=700, legend_at_bottom=True, height=500, explicit_size=True, style=custom_style)
        line_chart.x_labels = x
        line_chart.x_title = 'Percentil'
        line_chart.y_title = 'Duracion en Minutos'
        line_chart.add("Duracion", map(lambda x : int(x), y))
        self.__wrpsave(self.duracion_en_perceniles.__name__, graph=line_chart, save=save, csv=csv, show=show)

    def cant_anomalias_xcorredores(self, save=True, csv=True, show=False):
        """
            Cantidad de anomalias por corredor
        """
        self.aux = self.reportdata.copy()
        self.aux = self.aux.groupby(["corr_name", "sentido"]).size().reset_index().rename(columns={0: "cantidad", "corr_name": "corredor"})
        #f, axarr = plt.subplots(1, 2)
        #centro = self.aux[self.aux["sentido"] == "centro"].plot(x="Nombre de Corredor", kind="barh", ax=axarr[0], figsize=(11, 5))
        centro = self.aux[self.aux["sentido"] == "centro"].groupby(
            ['corredor', 'cantidad']).all().reset_index()[['corredor', 'cantidad']]
        provincia = self.aux[self.aux["sentido"] == "provincia"].groupby(
            ['corredor', 'cantidad']).all().reset_index()[['corredor', 'cantidad']]
        #provincia = self.aux[self.aux["sentido"] == "provincia"].plot(x="Nombre de Corredor", kind="barh", ax=axarr[1], figsize=(11, 5))
        #plt.xlabel('Duracion en minutos')
        # plt.ylabel('')
        custom_style = Style(label_font_size=12, background='white')

        def add_chart(sentido, name):
            bar_chart = pygal.HorizontalBar(no_data_text='Sin Datos', tooltip_border_radius=10, 
                x_title='Cantidad de Anomalias, Sentido {0}'.format(name.title()), width=600, height=400,  style=custom_style, explicit_size=True)
            for key in sentido.values:
                bar_chart.add(key[0], key[1])

            name = self.cant_anomalias_xcorredores.__name__ + "_" + name.replace(" ", "_")
            self.__wrpsave(name, graph=bar_chart, save=save, csv=csv, show=show)

        add_chart(centro, 'capital')
        add_chart(provincia, 'provincia')


    def indice_anomalias_xcuadras(self, save=True, csv=True, show=False):
        """
            Indice de anomalias por cuadra
        """
        from pygal.style import CleanStyle

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
        # sns.factorplot(x="corr_name", y="indice", data=self.aux, hue="sentido", kind="bar", size=4, aspect=2)
        # plt.xticks(rotation=12, size="8")
        # plt.ylabel('Duracion en minutos')
        # plt.xlabel('')
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
        custom_style = CleanStyle(label_font_size=12, background='white')
        bar_chart = pygal.Bar(no_data_text='Sin Datos', tooltip_border_radius=10, y_title='Indice',
                              width=700, height=450, legend_at_bottom=True, style=custom_style, explicit_size=True, x_label_rotation=90)
        bar_chart.x_labels = list(set(self.aux['corr_name']))
        bar_chart.add('Provincia', set_items(lprov, 'provincia'))
        bar_chart.add('Capital', set_items(lcent, 'centro'))
        self.__wrpsave(self.indice_anomalias_xcuadras.__name__, graph=bar_chart, save=save, csv=csv, show=show)

    def __asignacion_frame(self):
        """
           valids = asignacion_frame(
               'anomaly', col1="id", col2="timestamp_end", col3="timestamp_end")
           # parse_dates={"timestamp_asignacion": (lambda X: "" if X == None
           # else X)}
        """
        self.query = self.session.query(Anomaly)
        self.query_all = self.query.filter(
            Anomaly.timestamp_start >= self.timestamp_start).all()
        self.valids = pd.read_sql(
            self.query.statement, self.query.session.bind)

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
