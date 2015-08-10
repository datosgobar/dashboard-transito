# Dashboard Operativo Transito

Desde el Centro de Control de Tránsito los operadores monitorean el sistema de tránsito y toman decisiones en tiempo real con el objetivo de descomprimir el tránsito.
Este dashboard muestra las anomalías de diferentes corredores prioritarios de la ciudad de acuerdo a un análisis periódico basado en información histórica

La vista principal estará siempre visible en un videowall.
El dashboard también se accede desde las computadoras de los operarios para visualizar en detalle la anomalía, comparar los datos con la vista de tráfico de Google Maps y asignarles una causa. Esta data se recolectará para ser usada en un análisis posterior.

## Instalacion bajo Mac y Linux

Tener instalado MySQL 5.1
```sh
$ apt-get install mysql-server
```
Instalar Dependencias, en openshift correr
```sh
$ source app-root/runtime/dependencies/python/virtenv/bin/activate
```
```sh
$ sudo python setup install
```
O instalamos las dependecias a mano de la siguiente manera:
```sh
$ sudo easy_install bottle
$ sudo easy_install gevent
$ sudo easy_install gevent-socketio
$ sudo easy_install MySQL-python
$ sudo easy_install sqlalchemy
```
## Instalacion bajo Windows
Bajar e instalar [Visual C++ for Python 2.7](http://download.microsoft.com/download/7/9/6/796EF2E4-801B-4FC4-AB28-B59FBF6D907B/VCForPython27.msi) y [MySQL for Python](https://github.com/farcepest/MySQLdb1)

```sh
easy_install bottle
easy_install gevent
easy_install gevent-socketio
easy_install MySQL-python
easy_install sqlalchemy
```

## Corriendo la app
Actualizar datos de conexion a base de datos en (un modelo se puede encontrar en analisis/config.py.sample)

```sh
python analisis/config.py
```

Asegurarse que MySQL está corriendo
```
 mysql.server start
 ```

Crear tabla en MySQL

```sh
$ python analisis/corredores.py
```

Instanciar Python Server
```sh
$ python app.py
```


Abrir el navegador en [http://127.0.0.1:8080/](http://127.0.0.1:8080/)

## Documentación 

  - [bottle](http://bottlepy.org/docs/dev/index.html)
  - [gevent](http://gevent.org/intro.html)
  - [gevent-socketio](https://gevent-socketio.readthedocs.org/en/latest/)

## Licencia
[MIT](http://opensource.org/licenses/MIT)