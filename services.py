import os
import requests
import subprocess
import configparser
import geocoder
import ast
import logging


class Services:
    def __init__(self):
        self.logger = self.get_logger('services')
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    def run_bash(self, script_path):
        try:
            subprocess.run(["bash", script_path], capture_output=True)
            self.logs["service.run_bash"] = "Скрипт выполнен успешно."
        except subprocess.CalledProcessError as e:
            self.logs["service.run_bash"] = f"Ошибка при выполнении bash скрипта: {e}"

    def run_python(self, script_path):
        try:
            with open(script_path, 'r') as f:
                script = f.read()
            exec(script)
            self.logs["service.run_python"] = "Скрипт выполнен успешно."
        except Exception as e:
            self.logs["service.run_python"] = f"Ошибка при выполнении python скрипта: {e}"
            
    def fetch_json(self, url):
        response = requests.get(url)
        if (response.status_code != 204 and response.status_code < 300 and
                response.headers["content-type"].strip().startswith("application/json")):
            try:
                return response.json()
            except ValueError:
                return response.status_code
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

