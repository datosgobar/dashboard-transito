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
    ip = "0.0.0.0"
    port = 8080

def parserEmitData(self, result):

  if len(result):
    self.emit('independencia', result['corredores'][0][result['corredores'][0].keys()[0]])
    self.emit('illia', result['corredores'][1][result['corredores'][1].keys()[0]])
    self.emit('nueve_de_julio', result['corredores'][2][result['corredores'][2].keys()[0]])
    self.emit('alem', result['corredores'][3][result['corredores'][3].keys()[0]])
    self.emit('corrientes', result['corredores'][4][result['corredores'][4].keys()[0]])
    self.emit('rivadavia', result['corredores'][5][result['corredores'][5].keys()[0]])
    self.emit('av_de_mayo', result['corredores'][6][result['corredores'][6].keys()[0]])
    self.emit('san_martin', result['corredores'][7][result['corredores'][7].keys()[0]])
    self.emit('juan_b_justo', result['corredores'][8][result['corredores'][8].keys()[0]])
    self.emit('cordoba', result['corredores'][9][result['corredores'][9].keys()[0]])
    self.emit('paseo_colon', result['corredores'][10][result['corredores'][10].keys()[0]])
    self.emit('cabildo', result['corredores'][11][result['corredores'][11].keys()[0]])
    self.emit('pueyrredon', result['corredores'][12][result['corredores'][12].keys()[0]])
    self.emit('alcorta', result['corredores'][13][result['corredores'][13].keys()[0]])
  else:
    self.emit('info', "sin datos")

# clase que hereda funcionalidades de socketio
class dataSemaforos(BaseNamespace, BroadcastMixin):

    # metodo que escucha on_<<CHANNELL>>(self, msg) enviado desde el front
    def on_receive(self, msg):

      if msg:

        estadocero = {}
        parserEmitData(self, estadocero)

        while True:

          estadocero = getData()
          parserEmitData(self, data)
          time.sleep(300)


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