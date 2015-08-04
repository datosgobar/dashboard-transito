# Dashboard Operativo Transito

## Instalacion Mac y Linux

Tener instalado MySQL 5.1

```sh
$ sudo python setup install
```
O instalamos las dependecias a mano de la siguiente manera:
```sh
$ sudo easy_install bottle
$ sudo easy_install gevent
$ sudo easy_install gevent-socketio
```
## Instalacion Windows
Bajar e instalar [Visual C++ for Python 2.7](http://download.microsoft.com/download/7/9/6/796EF2E4-801B-4FC4-AB28-B59FBF6D907B/VCForPython27.msi)
```sh
easy_install bottle
easy_install gevent
easy_install gevent-socketio
```

## Corriendo la app

Ejecutar
```sh

Crea la tabla en MySQL
$ python analisis/corredores.py

Instancia la App
$ python app.py
```

Abrir el navegador en [http://127.0.0.1:8080/](http://127.0.0.1:8080/)

## Documentación 

  - [bottle](http://bottlepy.org/docs/dev/index.html)
  - [gevent](http://gevent.org/intro.html)
  - [gevent-socketio](https://gevent-socketio.readthedocs.org/en/latest/)

## Licencia
[MIT](http://opensource.org/licenses/MIT)