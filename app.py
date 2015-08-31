#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import gevent
import os
import bottle
import time
import datetime
import logging

from analisis import *
from bottle import error, request
from socketio import socketio_manage
from socketio.mixins import BroadcastMixin
from socketio.namespace import BaseNamespace
from gevent import monkey
from dashboard_logging import setup_logging

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

Base = automap_base()
db_url = config.db_url
engine = create_engine(db_url)
Base.prepare(engine, reflect=True)
Anomaly = Base.classes.anomaly

monkey.patch_all()
app = bottle.Bottle()

# inicio condicional para evaluar si estoy en openshift
if os.environ.get('OPENSHIFT_PYTHON_DIR'):
    # en caso de estarlo, activo entorno virtual y agarro las variables de
    # entorno para ip y puerto
    zvirtenv = os.path.join(os.environ['OPENSHIFT_PYTHON_DIR'],
                            'virtenv', 'bin', 'activate_this.py')
    execfile(zvirtenv, dict(__file__=zvirtenv))
    ip = os.environ['OPENSHIFT_PYTHON_IP']
    port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
else:
    # caso contrario, entiendo que estoy en ambiente local
    ip = "127.0.0.1"
    port = 8080

# clase que hereda funcionalidades de socketio


class dataSemaforos(BaseNamespace, BroadcastMixin):

    def init(self):
        with open(os.path.abspath("analisis/template.json")) as templatecorredores:
            template_buffer = buffer(templatecorredores.read())
            self.template = json.loads(template_buffer.__str__())

    def clean(self):

        for key, value in self.template['corredores'].iteritems():
            self.template['corredores'][key]['segmentos_provincia'] = []
            self.template['corredores'][key]['segmentos_capital'] = []

    # metodo que escucha on_<<CHANNELL>>(self, msg) enviado desde el front
    def on_receive(self, msg):

        if msg:
            print msg

    def recv_connect(self):

        self.init()

        print "connect, emit data"
        while True:
            self.clean()
            parserEmitData(self, self.template)
            time.sleep(300)

    def recv_disconnect(self):
        print "disconnect"

# genero ruta / que envia template index


@app.get('/')
def root():
    return bottle.template('index')


@app.get('/desktop')
def root():
    return bottle.template('desktop')

# path para datos estaticos en el front


@app.get('/_static/<filepath:path>')
def get_static(filepath):
    return bottle.static_file(filepath, root='./static/')

# resuelve errores 404 y 500, en un decorador, para rutear a la funcion handler


@app.post("/")
def send_data():

    if set(['anomaly_id', 'comentario', 'causa_id']) == set(request.forms.keys()):

        session = Session(engine)
        anomaly_id = request.forms.get('anomaly_id', False)
        causa_id = request.forms.get("causa_id", False)
        comentario = request.forms.get("comentario", False)

        if anomaly_id and causa_id:
            queryAnomaly = session.query(Anomaly).filter_by(id=anomaly_id)
            if queryAnomaly.count():
                queryAnomaly.update({
                    'causa_id': causa_id,
                    'comentario_causa': comentario,
                    'timestamp_asignacion': datetime.datetime.now()
                })
                session.commit()
                session.close()
                return "guardado"
            else:
                return "no encontre anomaly {}".format(anomaly_id)
        else:
            return "no encontre valor en campos anomaly_id y causa_id"


@error(404)
@error(500)
def handler_error(error):
    return 'Nothing here, sorry'

# genero ruta /alertas para el manejo de socket.io, con xhr-polling y websocket


@app.get('/socket.io/<path:path>')
def socketio_service(path):
    socketio_manage(
        bottle.request.environ, {'/alertas': dataSemaforos}, bottle.request)


if __name__ == '__main__':

    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Listening on port {0} ip {1}".format(ip, port))

    # inicia la server python
    bottle.run(app=app,
               host=ip,
               port=port,
               server='geventSocketIO',
               debug=False,
               reloader=False,
               )
