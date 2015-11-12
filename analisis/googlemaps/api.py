import endpoints_config
import urllib
import urllib2
import json
import sys
from ..analisis import config

log_requests = False
token = config.api['token']


class Endpoint(object):
    config = {}

    def __init__(self, attrs):
        self.attrs = attrs

    @staticmethod
    def request(config, params=None):
        params = params or {}
        params['_format'] = 'json'
        data = urllib.urlencode(params)
        if config['method'] == 'GET':
            url = config['url'] + '?' + data
            request = urllib2.Request(url, {}, {'Content-Type': 'application/x-www-form-urlencoded'})
        else:
            url = config['url']
            request = urllib2.Request(url, data, {'Content-Type': 'application/x-www-form-urlencoded'})
        request.get_method = lambda: config['method']
        request.add_header("token", token)

        response = urllib2.urlopen(request).read()
        if len(response) > 0:
            json_response = json.loads(response)
        else:
            json_response = {'codigo': 204, 'error': []}

        if log_requests:
            sys.stdout.write("%s %s\n" % (config['method'], url))
            sys.stdout.write("%s %s\n" % (json_response['codigo'], json_response['mensaje']))
            sys.stdout.write("%d bytes sent in the request's body\n" % sys.getsizeof(data))
            sys.stdout.write("%d bytes received response's body\n" % sys.getsizeof(response))
        if len(json_response['error']) > 0:
            raise ValueError(str(json_response['error']) + '\n')

        return json_response

    @classmethod
    def _replace_id(cls, endpoint_name, obj_id):
        config_copy = cls.config[endpoint_name].copy()
        config_copy['url'] = config_copy['url'].replace('{id}', str(obj_id))
        return config_copy

    @classmethod
    def create(cls, attrs=None):
        response = cls.request(cls.config['create'], attrs)
        return cls(response['datos'])

    @classmethod
    def get(cls, obj_id):
        get_config = cls._replace_id('get', obj_id)
        response = cls.request(get_config)
        return cls(response['datos'])

    @classmethod
    def get_all(cls):
        response = cls.request(cls.config['get_all'])
        objects = []
        for obj in response['datos']:
            objects.append(cls(obj))
        return objects

    @classmethod
    def delete(cls, obj_id):
        delete_config = cls._replace_id('delete', obj_id)
        response = cls.request(delete_config)
        return response

    @classmethod
    def update(cls, params):
        update_config = cls._replace_id('update', params['id'])
        response = cls.request(update_config, params)
        return response

    def save(self):
        return self.update(self.attrs)

    def remove(self):
        return self.delete(self.attrs['id'])

    def __repr__(self):
        return '%s<%d, %s>' % (self.__class__.__name__, int(self.attrs['id']), self.attrs['nombre'])


class Account(Endpoint):
    config = endpoints_config.account


class Sensor(Endpoint):
    config = endpoints_config.sensor

    @classmethod
    def change_state(cls, params):
        response = cls.request(cls.config['change_state'], params)
        return response

    @classmethod
    def get_all_with_datatypes(cls):
        response = cls.request(cls.config['get_all_with_datatypes'])
        sensors = []
        for sensor in response['datos']:
            sensors.append(cls(sensor))
        return sensors

    def get_datatypes(self):
        return DataType.get_from_sensor(self.attrs['id'])

    def get_last_data(self):
        return Data.get_last(self.attrs['id'])

    def get_multiple_last_data(self):
        return Data.get_multiple_lasts(self.attrs['id'])


class DataType(Endpoint):
    config = endpoints_config.datatype

    @classmethod
    def get_from_sensor_type(cls, sensor_type_id):
        get_config = cls._replace_id('get_from_sensor_type', sensor_type_id)
        response = cls.request(get_config)
        datatypes = []
        for datatype in response['datos']:
            datatypes.append(cls(datatype))
        return datatypes

    @classmethod
    def get_from_sensor(cls, sensor_id):
        get_config = cls._replace_id('get_from_sensor', sensor_id)
        response = cls.request(get_config)
        datatypes = []
        for datatype in response['datos']:
            datatypes.append(cls(datatype))
        return datatypes


class SensorType(Endpoint):
    config = endpoints_config.sensor_type

    @classmethod
    def get_from_sensor(cls, sensor_id):
        get_config = cls._replace_id('get_from_sensor', sensor_id)
        response = cls.request(get_config)
        sensor_type = cls(response['datos'])
        return sensor_type


class Data(Endpoint):
    config = endpoints_config.data

    def __init__(self, attrs):
        super(Data, self).__init__(attrs)
        self.empty = len(self.attrs) == 0

    @classmethod
    def dynamic_create(cls, params):
        response = cls.request(cls.config['dynamic_create'], params)
        return response

    @classmethod
    def get_last(cls, sensor_id, params=None):
        get_last_config = cls._replace_id('get_last', sensor_id)
        response = cls.request(get_last_config, params)
        data = []
        if 'datos' in response:
            if len(response['datos']) == 1:
                data.append(cls(response['datos'][0]))
            if len(response['datos']) > 1:
                for d in response['datos']:
                    data.append(cls(d))
        return data

    @classmethod
    def get_multiple_lasts(cls, sensor_id, params=None):
        get_multiple_lasts_config = cls._replace_id('get_multiple_lasts', sensor_id)
        response = cls.request(get_multiple_lasts_config, params)
        data = []
        if 'datos' in response:
            for d in response['datos']:
                data.append(cls(d))
        return data

    @classmethod
    def get(cls, sensor_id, params=None):
        get_config = cls._replace_id('get', sensor_id)
        response = cls.request(get_config, params)
        data = []
        for d in response['datos']['data']:
            data.append(cls(d))
        return data

    def __repr__(self):
        if self.empty:
            return '%s<Empty>' % self.__class__.__name__
        else:
            return '%s<%s, %s>' % (self.__class__.__name__, self.attrs['date'], self.attrs['data'])


class MeasurementMethodology(Endpoint):
    config = endpoints_config.methodology


class MeasuredUnit(Endpoint):
    config = endpoints_config.unit


class MeasuredParameter(Endpoint):
    config = endpoints_config.parameter


class MeasureFrequency(Endpoint):
    config = endpoints_config.frequency


class Homologation(Endpoint):
    config = endpoints_config.homologation


class Brand(Endpoint):
    config = endpoints_config.brand


class Model(Endpoint):
    config = endpoints_config.model


class User(Endpoint):
    config = endpoints_config.user

    @classmethod
    def add_roles(cls, user_id, params):
        add_roles_config = cls._replace_id('add_roles', user_id)
        cls.request(add_roles_config, params)
        return True

    @classmethod
    def remove_roles(cls, user_id, params):
        remove_roles_config = cls._replace_id('remove_roles', user_id)
        cls.request(remove_roles_config, params)
        return True

    def __repr__(self):
        return '%s<%s, %s>' % (self.__class__.__name__, self.attrs['id'], self.attrs['name'])
