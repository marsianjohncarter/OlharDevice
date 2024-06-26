import os
import requests
import subprocess
import configparser
import geocoder
import ast

class Services:
    def __init__(self):
        self.logs = {
            "service.run_bash":"",
        }

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
        response = requests.post(url)
        if (response.status_code != 204 and response.status_code < 300 and
                response.headers["content-type"].strip().startswith("application/json")):
            try:
                self.logs["service.fetch_json"] = "JSON успешно загружен."
                return response.json()
            except ValueError:
                self.logs["service.fetch_json"] = "Не удалось прочитать JSON. Статус код: " + str(response.status_code)
                return response.status_code
        return None

    def fetch_script(self, url):
        response = requests.post(url)
        if response.status_code != 204:
            self.logs["service.fetch_script"] = "Скрипт успешно загружен."
            return response.text
        self.logs["service.fetch_script"] = "Не удалось загрузить скрипт. Статус код: " + str(response.status_code)
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
            self.logs["service.register_video_view"] = "Регистрация показа видео прошла успешно."
        else:
            self.logs["service.register_video_view"] = f"Ошибка регистрации показа видео: {response.status_code}"

    def get_param_from_config(self, config_path: str, param_name: str):
        config = configparser.ConfigParser()
        try:
            config.read(f'{config_path}')
            part_number = config['General'][f'{param_name}']
            self.logs["service.get_param_from_config"] = "Чтение конфигурационного файла прошло успешно."
            return part_number
        except Exception as e:
            self.logs["service.get_param_from_config"] = f"Ошибка при чтении конфигурационного файла: {e}"

    def get_lat_lon(self):
        g = geocoder.ip('me')
        return g.latlng

    def get_logs(self, _class):
        return _class.logs
    
    def delete_file(self, path):
        os.remove(path)

