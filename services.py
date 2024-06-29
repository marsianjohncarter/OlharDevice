import os
import requests
import subprocess
import configparser
import geocoder
import ast
import logging
from geopy.geocoders import Nominatim

class Services:
    def __init__(self):
        self.logger = self.get_logger('services')
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    def run_bash(self, script_path):
        try:
            subprocess.run(["bash", script_path], capture_output=True)
            self.logger.info('Script executed successfully')
        except subprocess.CalledProcessError as e:
            self.logger.error(f'Error running bash script: {e}')

    def run_python(self, script_path):
        try:
            with open(script_path, 'r') as f:
                script = f.read()
            exec(script)
            self.logger.info('Script executed successfully')
        except Exception as e:
            self.logger.error(f'Error running python script: {e}')
            
    def fetch_json(self, url):
        response = requests.get(url)
        if (response.status_code != 204 and response.status_code < 300 and
                response.headers["content-type"].strip().startswith("application/json")):
            try:
                return response.json()
            except ValueError:
                self.logger.critical(f'Error loading JSON: {response.status_code}')
                return response.status_code
        self.logger.critical(f'Error loading JSON: {response.status_code}')
        return None

    def fetch_script(self, url):
        response = requests.get(url)
        if response.status_code != 204:
            self.logger.info('Script loaded successfully')
            return response.text
        self.logger.error(f'Error loading script: {response.status_code}')
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
            self.logger.info('Video view registered successfully')
        else:
            self.logger.error(f'Error registering video view: {response.status_code}')

    def get_param_from_config(self, config_path: str, param_name: str):
        config = configparser.ConfigParser()
        try:
            config.read(f'{config_path}')
            part_number = config['General'][f'{param_name}']
            return part_number
        except FileNotFoundError:
            self.logger.error(f'Config file not found: {config_path}')
            return None

    def get_lat_lon(self):
        g = geocoder.ip('me')
        return g.latlng

    def delete_file(self, path):
        if os.path.exists(path):
            try:
                os.remove(path)
                self.logger.info(f'Deleted file: {path}')
            except PermissionError:
                self.logger.error(f'Error deleting file: {path}')


    def get_logger(self, name):
        log_format = '%(asctime)s  %(name)8s  %(levelname)5s  %(message)s'
        logging.basicConfig(level=logging.DEBUG,
                            format=log_format,
                            filename='dev.log',
                            filemode='w')
        return logging.getLogger(name)


    def get_city_from_coordinates(self, latitude, longitude):
        geoLoc = Nominatim(user_agent="GetLoc")

        loc = self.get_lat_lon()
        locname = geoLoc.reverse(f'50.0 40.0')
        address = locname.raw['address']['village'] # type: ignore
        print(address)

    # latitude, longitude = get_current_location()
    # if latitude and longitude:
    #     city = get_city_from_coordinates(latitude, longitude)
    #     if city:
    #         print(f"The current city is: {city}")
    #     else:
    #         print("Could not determine the city.")
    # else:
    #     print("Could not determine the current location.")
