import requests


class Point(object):

    def __init__(self, client_credentials_manager=None):
        self._client_credentials_manager = client_credentials_manager

        self._session = requests.Session()
        self.prefix = 'https://api.minut.com/v1/'

    def doit(self):
        token = self._client_credentials_manager.get_access_token()
        print(token)

    def _create_auth_headers(self):
        token = self._client_credentials_manager.get_access_token()
        return {'Authorization': 'Bearer {0}'.format(token)}

    def _internal_call(self, method, url, payload=None):
        if not url.startswith('http'):
            url = self.prefix + url

        headers = self._create_auth_headers()

        return self._session.request(method, url,
                                     headers=headers, params=payload)

    def _get(self, url, payload=None):
        return self._internal_call('GET', url, payload)

    def devices(self):
        resonpose = self._get('devices')
        return resonpose.json().get('devices')

    def device(self, device_id):
        response = self._get('devices/%s' % device_id)
        return response.json()

    def _get_time_series(self, url, **options):
        payload = {
            'start_at': options.get('start_at'),
            'end_at': options.get('end_at'),
            'raw': options.get('raw')
        }
        response = self._get(url, payload)
        return response.json()

    def temperature(self, device_id, **options):
        return self._get_time_series('devices/%s/temperature' % device_id,
                                     **options)

    def humidity(self, device_id, **options):
        return self._get_time_series('devices/%s/humidity' % device_id,
                                     **options)

    def sound_level(self, device_id, **options):
        return self._get_time_series('devices/%s/sound_level' % device_id,
                                     **options)

    def battery(self, device_id, **options):
        return self._get_time_series('devices/%s/battery' % device_id,
                                     **options)

    def part_als(self, device_id, **options):
        return self._get_time_series('devices/%s/part_als' % device_id,
                                     **options)

    def part_als_ir(self, device_id, **options):
        return self._get_time_series('devices/%s/part_als_ir' % device_id,
                                     **options)
