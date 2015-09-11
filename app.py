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

from beaker.middleware import SessionMiddleware
from cork import Cork
from cork.backends import SqlAlchemyBackend

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

bottle.debug(True)
Base = automap_base()
db_url = config.db_url
engine = create_engine(db_url)
Base.prepare(engine, reflect=True)
Anomaly = Base.classes.anomaly

monkey.patch_all()

logger = dashboard_logging(config="analisis/logging.json", name=__name__)


def auth_sqlalchemy():
    sqlalchemy_backend = SqlAlchemyBackend(config.db_url)
    return sqlalchemy_backend

auth = auth_sqlalchemy()
bottle_auth = Cork(backend=auth)

app = bottle.app()
session_opts = {
    #'session.cookie_expires': True,
    #'session.encrypt_key': 'please use a random key and keep it secret!',
    #'session.httponly': False,
    'session.timeout': 3600 * 24,  # 1 day
    #'session.type': 'cookie'
    #'session.validate_key': True,
}
app = SessionMiddleware(app, session_opts)

# inicio condicional para evaluar si estoy en openshift
if os.environ.get('OPENSHIFT_PYTHON_DIR'):
    # en caso de estarlo, activo entorno virtual y agarro las variables de
    # entorno para ip y puerto
    zvirtenv = os.path.join(os.environ['OPENSHIFT_PYTHON_DIR'],
                            'virtenv', 'bin', 'activate_this.py')
    execfile(zvirtenv, dict(__file__=zvirtenv))
    ip = os.environ['OPENSHIFT_PYTHON_IP']
    port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
    logger.info("OPENSHIFT Listening on port {0} ip {1}".format(ip, port))
else:
    # caso contrario, entiendo que estoy en ambiente local
    ip = "0.0.0.0"
    port = 8080

# clase que hereda funcionalidades de socketio

logger.info("Listening on port {0} ip {1}".format(ip, port))


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
            logger.info("{0}".format(msg))

    def recv_connect(self):

        self.init()
        logger.info("connect, emit data")
        while True:
            self.clean()
            parserEmitData(self, self.template)
            time.sleep(300)

    def recv_disconnect(self):
        logger.info("discconect")

# genero ruta / que envia template index


@bottle.route('/')
def views_login():
    """Serve login form"""
    if bottle_auth.user_is_anonymous:
        return bottle.template('login')
    else:
        return bottle.template('index')


@bottle.route('/salir')
def logout():
    bottle_auth.logout(success_redirect='/')


@bottle.post('/login')
def login_post():
    """Authenticate users"""
    username = request.POST.get("username", "").strip()
    password = request.POST.get("password", "").strip()
    logger.info("login {0}".format(username))
    bottle_auth.login(
        username, password, success_redirect='/index', fail_redirect='/')


@bottle.route('/index')
def views_index():
    bottle_auth.require(fail_redirect='/')
    return bottle.template('index')


@bottle.route('/desktop')
def root():
    bottle_auth.require(fail_redirect='/')
    return bottle.template('desktop')


@bottle.route('/_public/<filepath:path>')
def get_static_js(filepath):
    return bottle.static_file(filepath, root='./public/')


@bottle.route('/_static/<filepath:path>')
def get_static(filepath):
    bottle_auth.require(fail_redirect='/')
    return bottle.static_file(filepath, root='./static/')


@bottle.post("/index")
def send_data():
    bottle_auth.require(fail_redirect='/')
    if set(['anomaly_id', 'comentario', 'causa_id', 'tipo_corte']) == set(request.forms.keys()):
        session = Session(engine)
        anomaly_id = request.forms.get('anomaly_id', False)
        causa_id = request.forms.get("causa_id", False)
        comentario = request.forms.get("comentario", False)
        tipo_corte = request.forms.get("tipo_corte", False)
        if anomaly_id and causa_id:
            queryAnomaly = session.query(Anomaly).filter_by(id=anomaly_id)
            if queryAnomaly.count():
                queryAnomaly.update({
                    'causa_id': causa_id,
                    'comentario_causa': comentario,
                    'tipo_corte': tipo_corte,
                    'timestamp_asignacion': datetime.datetime.now()
                })
                session.commit()
                session.close()
                logger.info("post guardado")
                return "guardado"
            else:
                logger.info("no encontre anomaly {}".format(anomaly_id))
        else:
            logger.info("no encontro valor en campos anomaly_id y causa_id")
    else:
        logger.error("post mal generado")


@error(404)
@error(500)
def handler_error(error):
    return 'Nothing here, sorry'


@bottle.get('/socket.io/<path:path>')
def socketio_service(path):
    bottle_auth.require(fail_redirect='/')
    logger.info("connect socket io")
    socketio_manage(
        bottle.request.environ, {'/alertas': dataSemaforos}, bottle.request)


if __name__ == '__main__':

    # inicia la server python
    bottle.run(app=app,
               host=ip,
               port=port,
               server='geventSocketIO',
               debug=True,
               reloader=False,
               )
