#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import gevent
import os
import bottle

from bottle import error
from socketio import socketio_manage
from socketio.mixins import BroadcastMixin
from socketio.namespace import BaseNamespace
from gevent import monkey

monkey.patch_all()
app = bottle.Bottle()

if os.environ.get('OPENSHIFT_PYTHON_DIR'):
    zvirtenv = os.path.join(os.environ['OPENSHIFT_PYTHON_DIR'],
                            'virtenv', 'bin', 'activate_this.py')
    execfile(zvirtenv, dict(__file__=zvirtenv))
    ip = os.environ['OPENSHIFT_PYTHON_IP']
    port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
else:
    ip = "0.0.0.0"
    port = 8080

class dataSemaforos(BaseNamespace, BroadcastMixin):

    def on_receive(self, msg):
        print(msg) # Connected
        self.emit("nada", "ok")


@app.get('/')
def root():
    return bottle.template('index')


@app.get('/_static/<filepath:path>')
def get_static(filepath):
    return bottle.static_file(filepath, root='./static/')


@error(404)
@error(500)
def handler_error(error):
    return 'Nothing here, sorry'


@app.get('/socket.io/<path:path>')
def socketio_service(path):
    socketio_manage(bottle.request.environ, {'/alertas': dataSemaforos}, bottle.request)


if __name__ == '__main__':
    print 'Listening on port {0} ip {1}'.format(ip, port)
    bottle.run(app=app,
               host=ip,
               port=port,
               server='geventSocketIO',
               debug=False,
               reloader=False,
               )