#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import gevent
import os
import bottle
import time

from analisis import * 
from bottle import error
from socketio import socketio_manage
from socketio.mixins import BroadcastMixin
from socketio.namespace import BaseNamespace
from gevent import monkey

monkey.patch_all()
app = bottle.Bottle()

# inicio condicional para evaluar si estoy en openshift
if os.environ.get('OPENSHIFT_PYTHON_DIR'):
    #en caso de estarlo, activo entorno virtual y agarro las variables de entorno para ip y puerto
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

    # metodo que escucha on_<<CHANNELL>>(self, msg) enviado desde el front
    def on_receive(self, msg):

      self.init()

      if msg:
        
        print "connect"

        while True:
          #estadocero = getData()
          #parserEmitDataFake(self, estadocero)
          self.init()
          parserEmitData(self, self.template)
          #time.sleep(300)
          time.sleep(10)

    def recv_disconnect(self):
      print "disconnect"

# genero ruta / que envia template index
@app.get('/')
def root():
    return bottle.template('index')

# path para datos estaticos en el front
@app.get('/_static/<filepath:path>')
def get_static(filepath):
    return bottle.static_file(filepath, root='./static/')

# resuelve errores 404 y 500, en un decorador, para rutear a la funcion handler
@error(404)
@error(500)
def handler_error(error):
    return 'Nothing here, sorry'

# genero ruta /alertas para el manejo de socket.io, con xhr-polling y websocket
@app.get('/socket.io/<path:path>')
def socketio_service(path):
    socketio_manage(bottle.request.environ, {'/alertas': dataSemaforos}, bottle.request)

if __name__ == '__main__':
    print 'Listening on port {0} ip {1}'.format(ip, port)
    # inicia la server python
    bottle.run(app=app,
               host=ip,
               port=port,
               server='geventSocketIO',
               debug=False,
               reloader=False,
               )