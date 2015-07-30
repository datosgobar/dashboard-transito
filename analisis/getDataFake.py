#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

def getData():

	with open("/home/lmokto/Desktop/dashboard-operativo-transito/analisis/corredores_fake.json") as f:
		output = json.loads(f.read())

	return output
