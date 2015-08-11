import os

if os.environ.get('OPENSHIFT_MYSQL_DIR'):
    mysql = dict(
        user=os.environ.get('OPENSHIFT_MYSQL_DB_USERNAME'),
        password=os.environ.get('OPENSHIFT_MYSQL_DB_PASSWORD'),
        host=os.environ.get('OPENSHIFT_MYSQL_DB_HOST'),
        db='dashboardoperativo'
    )
else:
    mysql = dict(
        user='root',
        password='password',
        host='localhost',
        db='dashboardoperativo'
    )
