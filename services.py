import json
import os
import stat
import requests
import subprocess
import configparser
import geocoder
import ast
import logging
from geopy.geocoders import Photon
import serial
import darkdetect
import screen_brightness_control as sbc


SERIAL_PORT = "/dev/ttyUSB0"
BASE_URL = 'https://api.olhar.media/'

logger = logging.getLogger('services')


class Services:
    def fetch_json(self, url):
        response = requests.get(f'{BASE_URL}{url}')
        if not (response.status_code != 204 and response.status_code < 300 and
                response.headers["content-type"].strip().startswith("application/json")):
            raise RuntimeError(f'Error loading json: {response.status_code}')
        return response.json()

    def fetch_script(self, url):
        response = requests.get(url)
        if response.status_code != 204:
            logger.info('Script loaded successfully')
            return response.text
        logger.error(f'Error loading script: {response.status_code}')
        return None

    def is_valid_python(self, code):
        try:
            ast.parse(code)
        except SyntaxError:
            return False
        return True

    def is_valid_bash(self, code):
        result = subprocess.run(["pylint", "--errors-only", "-", code], capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            return False

    def register_video_view(self, video_id: int, equip_id: int, equip_ip: str, gps_lat: float, gps_lon: float):
        url = "https://api.olhar.media/"
        params = {
            'regview': 1,
            'videoid': video_id,
            'equipid': equip_id,
            'equipip': equip_ip,
            'gpsposlat': gps_lat,
            'gpsposlon': gps_lon
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            logger.info('Video view registered successfully')
        else:
            logger.error(f'Error registering video view: {response.status_code}')

    def get_param_from_config(self, config_path: str, param_name: str):
        config = configparser.ConfigParser()
        try:
            config.read(f'{config_path}')
            part_number = config['General'][f'{param_name}']
            return part_number
        except FileNotFoundError:
            logger.error(f'Config file not found: {config_path}')
            return None

    def formatDegreesMinutes(self, coordinates, digits):
    
        parts = coordinates.split(".")

        if (len(parts) != 2):
            return coordinates

        if (digits > 3 or digits < 2):
            return coordinates
        
        left = parts[0]
        right = parts[1]
        degrees = str(left[:digits])
        minutes = str(right[:3])

        return degrees + "." + minutes

    def get_lat_lon(self):
        try:
                gps = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 0.5)
                
                data = gps.readline().decode('utf-8').rstrip()
                message = data[0:6]
                if (message == "$GNRMC"):
                    # GPRMC = Рекомендуемые минимальные конкретные данные GPS / транзит
                    # Чтение фиксированных данных GPS является альтернативным подходом, 
                    # который также работает
                    parts = data.split(",")
                    if parts[2] == 'V':
                        # V = Предупреждение, скорее всего, спутников нет в поле зрения ...
                        raise RuntimeError('No satellites in view')
                    else:
                        # Получить данные о местоположении, которые были переданы с сообщением GPRMC. 
                        # В этом примере интересуют только долгота и широта. Для других значений можно
                        # обратиться к http://aprs.gids.nl/nmea/#rmc
                        longitude = self.formatDegreesMinutes(parts[5], 3)
                        latitude = self.formatDegreesMinutes(parts[3], 2)
                        logger.info("Device position: lon = " + str(longitude) + ", lat = " + str(latitude))
                else:
                    raise RuntimeError('Invalid NMEA message')

                gps.close()
                return [latitude, longitude]
        except Exception as e:
            logger.error(f'Error getting GPS coordinates through serial port: {e}\n Falling back to IP geolocation...')
        try:
            g = geocoder.ip('me')
            return g.latlng
        except Exception as e:
            logger.critical(f'Error getting GPS coordinates through IP geolocation: {e}')
            raise RuntimeError(f'Error getting GPS coordinates through IP geolocation') from e

    def get_current_city(self):

        geolocator = Photon(user_agent="measurements")

        location_lat_lon = self.get_lat_lon()

        latitude = f"{location_lat_lon[0]}"
        longitude = f"{location_lat_lon[1]}"
        
        location = geolocator.reverse(f'{latitude},{longitude}')

        return location.raw['properties']['name']

    def set_brightness(self):
        if darkdetect.isDark():
            sbc.fade_brightness(50)
        else:
            sbc.fade_brightness(100, increment = 10)

    def filter_video_data(self, video_data):
        new_video_data = []
        for i in video_data:
            if 'locations' not in i:
                logger.error(f"Video object {i} has no 'locations' attribute.")
                continue
            for city in i['locations']:
                if 'enname' not in city:
                    logger.error(f"City object {city} has no 'enname' attribute.")
                    continue
                if city['enname'] == self.get_current_city():
                    new_video_data.append(i)
        return new_video_data

    def run_maintenance_script(self):
        try:
            logger.info('Fetching script...')
            script = self.fetch_script(f'{BASE_URL}?getconfigupdate&equipid=1')
            if script:
                script_path = "./maintenance_script"
                with open(script_path, 'w') as f:
                    f.write(script)
                os.chmod(script_path, stat.S_IRWXU)
                subprocess.run([script_path])
        except Exception as e:
            logger.error(e)
