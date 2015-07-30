#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo

if os.environ.get('OPENSHIFT_MONGODB_DIR'):
	host = os.environ.get('OPENSHIFT_MONGODB_DB_URL')
    client = pymongo.MongoClient(host)
else:
    client = pymongo.MongoClient("localhost", 27017)

db = client.anomalias

def write(**args):
	"""
		write(sub_seg_id="", timestamp_init="", timestamp_end="", causa="")
	"""
	db.anomalias.insert({
		"sub_seg_id" : args['sub_seg_id'],
		"timestamp_init": args['timestamp_init'],
		"timestamp_end": args['timestamp_end'],
		"causa": args['causa']
	})


db.close()