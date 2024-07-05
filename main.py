import os
from services import Services
from application import App
from PyQt5.QtWidgets import QApplication
import logging
from datetime import date, timedelta
import screen_brightness_control as sbc
import darkdetect

BASE_URL = 'https://api.olhar.media/'

service = Services()

current_city = service.get_current_city()


logging.basicConfig(filename=f'./assets/logs/{date.today()}.log', level=logging.DEBUG)
logger = logging.getLogger('main')

logger.setLevel(logging.DEBUG)

def set_brightness():
    if darkdetect.isDark():
        sbc.fade_brightness(50)
    else:
        sbc.fade_brightness(100, increment = 10)
    

def delete_old_logs():
    directory = './assets/logs'
    for filename in os.scandir(directory):
        if not filename.is_file():
            continue
        date_created = filename.name[:10]
        week_ago = date.today() - timedelta(days=7)
        if date_created == str(week_ago):
            os.remove(os.path.join(directory, filename.name))

def filter_video_data(video_data):
    new_video_data = []
    for i in video_data:
        if 'locations' not in i:
            logger.error(f"Video object {i} has no 'locations' attribute.")
            continue
        for city in i['locations']:
            if 'enname' not in city:
                logger.error(f"City object {city} has no 'enname' attribute.")
                continue
            if city['enname'] == current_city:
                new_video_data.append(i)
    return new_video_data


# def run_maintenance_script():
#     try:
#         logger.info('Fetching script...')
#         script = service.fetch_script(f'{BASE_URL}?getconfigupdate&equipid=1')
#         if script:
#             if service.is_valid_bash(script):
#                 with open('script.sh', 'wb') as f:
#                     f.write(script.encode())
#                 service.run_bash('./script.sh')
#                 os.remove('./script.sh')
#                 logger.info('Script executed successfully')
#             elif service.is_valid_python(script):
#                 with open('script.py', 'wb') as f:
#                     f.write(script.encode())
#                 service.run_python('./script.py')
#                 os.remove('./script.py')
#                 logger.info('Script executed successfully')
#     except Exception as e:
#         logger.error(e)



def main():
    # run_maintenance_script()
    delete_old_logs()
    set_brightness()
    try:   
        logger.info('Fetching video data...')
        video_data = service.fetch_json(f'{BASE_URL}?getvideos&equipid=1')
    except Exception as e:
        logger.critical(e)
        raise RuntimeError('Failed to fetch video data') from e
    app = QApplication([])
    w = App()
    # w.set_video_data(video_data)
    # w.load_videos(video_data)
    w.set_video_data(filter_video_data(video_data))
    w.load_videos(filter_video_data(video_data))
    w.show()
    app.exec_()

if __name__ == "__main__":
    main()
    sbc.get_brightness()
    sbc.fade_brightness(100, increment = 10)

