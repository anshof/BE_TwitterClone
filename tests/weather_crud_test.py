from unittest import mock
from unittest.mock import patch
from . import app, client, cache, create_token
import json

class TestWeather():
    def mocked_request_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        if len(args)>0:
            if args[0]==app.config['WIO_HOST']+"/ip":
                return MockResponse(
                    {'offset': '-7', 'longitude': -117.2521, 'city': 'La Jolla', 'timezone': 'America/Los_Angeles', 'latitude': 32.8455, 'area_code': '858', 'region': 'California', 'dma_code': '825', 'organization': 'AS25876 Los Angeles Department of Water & Power', 'country': 'United States', 'ip': '134.201.250.155', 'country_code3': 'USA', 'postal_code': '92037', 'continent_code': 'NA', 'country_code': 'US', 'region_code': 'CA'}, 200)
            elif args[0] == app.config['WIO_HOST']+"/current":
                return MockResponse(
                    {'data': [{'rh': 66, 'pod': 'n', 'lon': -117.25, 'pres': 1016, 'timezone': 'America/Los_Angeles', 'ob_time': '2020-04-20 11:00', 'country_code': 'US', 'clouds': 54, 'ts': 1587380400, 'solar_rad': 0, 'state_code': 'CA', 'city_name': 'La Jolla', 'wind_spd': 2.24, 'last_ob_time': '2020-04-20T11:00:00', 'wind_cdir_full': 'northwest', 'wind_cdir': 'NW', 'slp': 1018.1, 'vis': 5, 'h_angle': -90, 'sunset': '02:23', 'dni': 0, 'dewpt': 8.7, 'snow': 0, 'uv': 0, 'precip': 0, 'wind_dir': 320, 'sunrise': '13:12', 'ghi': 0, 'dhi': 0, 'aqi': 32, 'lat': 32.85, 'weather': {'icon': 'c02n', 'code': '802', 'description': 'Scattered clouds'}, 'datetime': '2020-04-20:11', 'temp': 15, 'station': 'F3225', 'elev_angle': -26.07, 'app_temp': 15}], 'count': 1}, 200
                )
        else:
            return MockResponse(None, 404)

    @mock.patch('requests.get', side_effect=mocked_request_get)
    def test_check_weather_ip(self, get_mock, client):
        token = create_token()
        res = client.get(
            '/weather/ip',
            query_string={"ip":"167.520.430"}, 
            headers={'Authorization':'Bearer ' + token}
            )

        res_json = json.loads(res.data)
        assert res.status_code == 200
