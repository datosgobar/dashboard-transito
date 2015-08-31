#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(url='postgresql+psycopg2://lmokto:hacura@localhost/dashboardoperativo', debug='False', repository='db_repository')
