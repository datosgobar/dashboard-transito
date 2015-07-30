#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

def getData():

	with open("corredores_fake.json") as f:
		output = json.loads(f.read())

	return output
