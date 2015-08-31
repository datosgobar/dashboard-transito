#!/usr/bin/env python
from migrate.versioning.shell import main
import config

if __name__ == '__main__':
    main(url=config.db_url,
         debug=config.db['debug'], repository='db_repository')
