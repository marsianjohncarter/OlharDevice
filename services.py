from datetime import date
import json
import requests
import subprocess
import configparser
import geocoder
import ast
import logging
from geopy.geocoders import Photon
import serial

SERIAL_PORT = "/dev/ttyUSB0"


logging.basicConfig(filename=f'./assets/logs/{date.today()}.log', level=logging.DEBUG)

logger = logging.getLogger('services')
logger.setLevel(logging.DEBUG)

class Services:
    def __init__(self):

        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    def run_bash(self, script_path):
        try:
            subprocess.run(["bash", script_path], capture_output=True)
            logger.info('Script executed successfully')
        except subprocess.CalledProcessError as e:
            logger.error(f'Error running bash script: {e}')

    def run_python(self, script_path):
        try:
            with open(script_path, 'r') as f:
                script = f.read()
            exec(script)
            logger.info('Script executed successfully')
        except Exception as e:
            logger.error(f'Error running python script: {e}')
            
    def fetch_json(self, url):
        response = requests.get(url)
        if not (response.status_code != 204 and response.status_code < 300 and
                response.headers["content-type"].strip().startswith("application/json")):
            logger.error(f'Error loading json: {response.status_code}')
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
                # print(message)
                if (message == "$GNRMC"):
                    # GPRMC = Рекомендуемые минимальные конкретные данные GPS / транзит
                    # Чтение фиксированных данных GPS является альтернативным подходом, 
                    # который также работает
                    parts = data.split(",")
                    print(parts)
                    if parts[2] == 'V':
                        # V = Предупреждение, скорее всего, спутников нет в поле зрения ...
                        print ("GPS receiver warning")
                    else:
                        # Получить данные о местоположении, которые были переданы с сообщением GPRMC. 
                        # В этом примере интересуют только долгота и широта. Для других значений можно
                        # обратиться к http://aprs.gids.nl/nmea/#rmc
                        longitude = self.formatDegreesMinutes(parts[5], 3)
                        latitude = self.formatDegreesMinutes(parts[3], 2)
                        logger.info("Device position: lon = " + str(longitude) + ", lat = " + str(latitude))
                else:
                    # Обрабатывать другие сообщения NMEA и неподдерживаемые строки
                    pass

                gps.close()
                return [latitude, longitude]
        except Exception as e:
            logger.error(f'Error getting GPS coordinates through serial port: {e}\n Falling back to IP geolocation...')
            g = geocoder.ip('me')
            return g.latlng
    # TODO: Check if delete_file is needed
    # def delete_file(self, path):
    #     if os.path.exists(path):
    #         try:
    #             os.remove(path)
    #             logger.info(f'Deleted file: {path}')
    #         except PermissionError:
    #             logger.error(f'Error deleting file: {path}')



    def save_json(self, dictionary, path: str):
        with open(path, "w") as outfile:
            json.dump(dictionary, outfile, indent=4)

    def get_current_city(self):

        geolocator = Photon(user_agent="measurements")

        location_lat_lon = self.get_lat_lon()

        Latitude = f"{location_lat_lon[0]}"
        Longitude = f"{location_lat_lon[1]}"
        
        location = geolocator.reverse(Latitude+","+Longitude)

        return location
