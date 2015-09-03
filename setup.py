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
    install_requires=['bottle==0.12.8', 'gevent==1.1b1', 'gevent-socketio==0.3.5', 'requests==2.7.0', 'requests[security]',
                      'MySQL-python==1.2.3', 'sqlalchemy==1.0.8', 'pandas==0.16.2', 'dateutil==2.4.2', 'sqlalchemy-migrate']
)
