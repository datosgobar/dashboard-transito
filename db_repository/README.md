# Repositorio de Database Migration

Utiliza la librería SQLalchemy-migrate
> Leer [documentación](https://sqlalchemy-migrate.readthedocs.org/en/latest/versioning.html)

## Pasos a seguir

1. Modificar archivo de configuración con datos correspondientes a la base de datos
    Sampler en db_repository/config.py.sample
2. Instalar librería de SQLalchemy-migrate o correr setup.py
```sh
$ pip install sqlalchemy-migrate
```
3. Correr script de init para arrancar a versionar la base
```sh
$ python db_repository/__init__.py
```
4. Actualizar DB a última versión
```sh
$ python manage.py upgrade
```