import os
import hashlib
import urllib
import hmac
import base64
import urlparse
import datetime
import requests
import json
import api
from waypoints import waypoints_config
from analisis import config


class Segment:
    base_url = config.googlemaps['base_url']
    client_id = config.googlemaps['client_id']
    client_secret = config.googlemaps['client_secret']

    def __init__(self, origin, destination, waypoints):
        self._from = origin
        self._to = destination
        self._waypoints = waypoints
        args = {
            "alternatives": False,
            "departure_time": "now",
            "mode": "driving",
            "origin": origin,
            "destination": destination,
            "waypoints": '|'.join(["via:%s" % wp for wp in waypoints])
        }
        input_url = self.base_url + "?" + urllib.urlencode(args)
        self.url = self._sign_url(input_url)
        self.response = None

    def _sign_url(self, input_url):
        input_url += "&client=%s" % self.client_id
        url = urlparse.urlparse(input_url)
        url_to_sign = url.path + "?" + url.query
        decoded_key = base64.urlsafe_b64decode(self.client_secret)
        signature = hmac.new(decoded_key, url_to_sign, hashlib.sha1)
        encoded_signature = base64.urlsafe_b64encode(signature.digest())
        original_url = url.scheme + "://" + url.netloc + url.path + "?" + url.query
        return original_url + "&signature=" + encoded_signature

    def get_directions(self):
        try:
            r = requests.get(self.url, timeout=2, verify=False)
            self.response = json.loads(r.content)
        except Exception as e:
            log('Segment.get_directions ' + str(e))
            return False
        return True

    def get_time(self):
        travel_time = -1
        try:
            travel_time = self.response['routes'][0]['legs'][0]['duration_in_traffic']['value']
        except Exception as e:
            log('get_time ' + str(e))
            log('get_time_error from %s to %s waypoints %s' % (self._from, self._to, self._waypoints))
        return travel_time


def fetch_data():
    google_maps_data = {}
    for config in waypoints_config:
        segment = Segment(config['from'], config['to'], config['waypoints'])
        if segment.get_directions() and segment.get_time() > 0:
            google_maps_data[config['id']] = segment.get_time()
    return google_maps_data


def push_to_api(data_dict, date_now):
    date_string = date_now.strftime('%Y-%m-%dT%H:%M:%S-03:00')
    params = {}
    block = 1
    for key in data_dict:
        params["id%d" % block] = key
        params["data%d" % block] = data_dict[key]
        params["date%d" % block] = date_string
        params["datatype%d" % block] = 'tiempo_viaje'
        block += 1
    log("pushing %s" % str(params))
    try:
        api.Data.dynamic_create(params)
    except Exception as e:
        log(str(e))
    return


def its_time_to_do_stuff():
    now = datetime.datetime.now()
    weekday = now.weekday()
    # 0 = monday ... 6 = sunday
    hour = now.hour
    minute = now.minute
    if 23 <= hour or hour < 7:
        return minute == 00
    elif 7 <= hour < 10:
        if weekday < 5:
            return (minute % 5) == 0
        else:
            return (minute % 20) == 0
    elif 10 <= hour < 17:
        if weekday < 5:
            return (minute % 10) == 0
        else:
            return (minute % 20) == 0
    elif 17 <= hour < 20:
        if weekday < 5:
            return (minute % 5) == 0
        elif weekday == 6:
            return (minute % 10) == 0
        else:
            return (minute % 20) == 0
    else:
        if weekday < 6:
            return (minute % 10) == 0
        else:
            return (minute % 20) == 0


def log(msj):
    repo_dir = os.getenv('OPENSHIFT_REPO_DIR', '.')
    log_path = os.path.join(repo_dir, 'api.log')
    time_string = datetime.datetime.now().isoformat()
    msj = time_string + '  ' + msj
    with open(log_path, "a") as log_file:
        log_file.write("%s\n" % msj)


def getDataFromGoogle():
    now_date = datetime.datetime.now()
    data = fetch_data()
    push_to_api(data, now_date)
    raw_data = []
    timestamp = now_date.strftime('%Y-%m-%dT%H:%M:%S-03:00')
    for k in data.keys():
        raw_data.append({
            'datos': {
                'data': [
                    {
                        'data': data[k],
                        'iddevice': k,
                        'date': timestamp
                    }
                ]
            }
        })
    return raw_data
