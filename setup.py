#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
	name='dashboard operativo transito',
	version='1.0',
	description='dashboard de trafico',
	author='lab gcba',
	author_email='',
	url='http://git.gcba.gob.ar/labgcba/dashboard-operativo-transito.git',
	install_requires=['bottle', 'gevent', 'gevent-socketio', 'MySQL-python']
)