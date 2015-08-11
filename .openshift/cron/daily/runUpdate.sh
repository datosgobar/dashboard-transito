#!/bin/bash

/var/lib/openshift/55bbc87dca988e695100000e/python/virtenv/bin/python ${OPENSHIFT_REPO_DIR}analisis/dailyUpdate.py >> ${OPENSHIFT_PYTHON_LOG_DIR}dailyUpdate.log 2>&1 &