base_url = "https://apisensores.buenosaires.gob.ar/api"
account = {
    "get_all": {
        "method": "GET",
        "url": "%s/cuenta"
    },
    "create": {
        "method": "POST",
        "url": "%s/cuenta/create"

    },
    "get": {
        "method": "GET",
        "url": "%s/cuenta/{id}"
    },
    "delete": {
        "method": "PUT",
        "url": "%s/cuenta/{id}/baja"

    },
    "update": {
        "method": "PUT",
        "url": "%s/cuenta/{id}/update"

    }
}
sensor = {
    "change_state": {
        "method": "PUT",
        "url": "%s/sensor/cambiarestado"
    },
    "create": {
        "method": "POST",
        "url": "%s/sensor/create"
    },
    "get": {
        "method": "GET",
        "url": "%s/sensor/{id}"
    },
    "delete": {
        "method": "PUT",
        "url": "%s/sensor/{id}/baja"
    },
    "update": {
        "method": "PUT",
        "url": "%s/sensor/{id}/update"
    },
    "get_all": {
        "method": "GET",
        "url": "%s/sensores"
    },
    "get_all_with_datatypes": {
        "method": "GET",
        "url": "%s/sensorestipodato"
    }
}
datatype = {
    "create": {
        "method": "POST",
        "url": "%s/sensor/tipo/data_type/create"
    },
    "get": {
        "method": "GET",
        "url": "%s/sensor/tipo/data_type/{id}"
    },
    "update": {
        "method": "PUT",
        "url": "%s/sensor/tipo/data_type/{id}/update"
    },
    "get_from_sensor_type": {
        "method": "GET",
        "url": "%s/sensor/tipo/{id}/data_type"
    },
    "get_from_sensor": {
        "method": "GET",
        "url": "%s/sensor/{id}/tipo/data_type"
    }
}
sensor_type = {
    "get_all": {
        "method": "GET",
        "url": "%s/sensor/tipo"
    },
    "create": {
        "method": "POST",
        "url": "%s/sensor/tipo/create"
    },
    "get": {
        "method": "GET",
        "url": "%s/sensor/tipo/{id}"
    },
    "update": {
        "method": "PUT",
        "url": "%s/sensor/tipo/{id}/update"
    },
    "get_from_sensor": {
        "method": "GET",
        "url": "%s/sensor/{id}/tipo"
    }
}
data = {
    "create": {
        "method": "POST",
        "url": "%s/data/create"
    },
    "dynamic_create": {
        "method": "POST",
        "url": "%s/data/dynamic/create"
    },
    "get": {
        "method": "GET",
        "url": "%s/data/{id}"
    },
    "get_last": {
        "method": "GET",
        "url": "%s/data/{id}/last"
    },
    "get_multiple_lasts": {
        "method": "GET",
        "url": "%s/data/{id}/status"
    }
}
methodology = {
    "get_all": {
        "method": "GET",
        "url": "%s/metodologia_medicion"
    },
    "create": {
        "method": "POST",
        "url": "%s/metodologia_medicion/create"
    },
    "get": {
        "method": "GET",
        "url": "%s/metodologia_medicion/{id}"
    },
    "update": {
        "method": "PUT",
        "url": "%s/metodologia_medicion/{id}/update"
    }
}
unit = {
    "get_all": {
        "method": "GET",
        "url": "%s/unidad_medida"
    },
    "create": {
        "method": "POST",
        "url": "%s/unidad_medida/create"
    },
    "get": {
        "method": "GET",
        "url": "%s/unidad_medida/{id}"
    },
    "update": {
        "method": "PUT",
        "url": "%s/unidad_medida/{id}/update"
    }
}
parameter = {
    "get_all": {
        "method": "GET",
        "url": "%s/parametro_medido"
    },
    "create": {
        "method": "POST",
        "url": "%s/parametro_medido/create"
    },
    "get": {
        "method": "GET",
        "url": "%s/parametro_medido/{id}"
    },
    "update": {
        "method": "PUT",
        "url": "%s/parametro_medido/{id}/update"
    }
}
frequency = {
    "get_all": {
        "method": "GET",
        "url": "%s/frecuencia_medicion"
    },
    "create": {
        "method": "POST",
        "url": "%s/frecuencia_medicion/create"
    },
    "get": {
        "method": "GET",
        "url": "%s/frecuencia_medicion/{id}"
    },
    "update": {
        "method": "PUT",
        "url": "%s/frecuencia_medicion/{id}/update"
    }
}
homologation = {
    "get_all": {
        "method": "GET",
        "url": "%s/hml_metodologia_medicion"
    },
    "create": {
        "method": "POST",
        "url": "%s/hml_metodologia_medicion/create"
    },
    "get": {
        "method": "GET",
        "url": "%s/hml_metodologia_medicion/{id}"
    },
    "update": {
        "method": "PUT",
        "url": "%s/hml_metodologia_medicion/{id}/update"
    }
}
brand = {
    "get_all": {
        "method": "GET",
        "url": "%s/marca"
    },
    "create": {
        "method": "POST",
        "url": "%s/marca/create"
    },
    "get": {
        "method": "GET",
        "url": "%s/marca/{id}"
    },
    "update": {
        "method": "PUT",
        "url": "%s/marca/{id}/update"
    }
}
model = {
    "get_all": {
        "method": "GET",
        "url": "%s/modelo"
    },
    "create": {
        "method": "POST",
        "url": "%s/modelo/create"
    },
    "get": {
        "method": "GET",
        "url": "%s/modelo/{id}"
    },
    "update": {
        "method": "PUT",
        "url": "%s/modelo/{id}/update"
    }
}
user = {
    "get_all": {
        "method": "GET",
        "url": "%s/usuario"
    },
    "create": {
        "method": "POST",
        "url": "%s/usuario/create"
    },
    "get": {
        "method": "GET",
        "url": "%s/usuario/{id}"
    },
    "add_roles": {
        "method": "POST",
        "url": "%s/usuario/{id}/agregar_rol"
    },
    "delete": {
        "method": "PUT",
        "url": "%s/usuario/{id}/baja"
    },
    "remove_roles": {
        "method": "DELETE",
        "url": "%s/usuario/{id}/eliminar_rol"
    },
    "update": {
        "method": "PUT",
        "url": "%s/usuario/{id}/update"
    }
}
for endpoint in [account, sensor, datatype, sensor_type, data, methodology,
                 unit, parameter, frequency, homologation, brand, model, user]:
    for action in endpoint:
        endpoint[action]['url'] %= base_url
