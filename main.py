import os
from services import Services
from application import App
from PyQt5.QtWidgets import QApplication
import logging
from datetime import date, timedelta
import screen_brightness_control as sbc
import os

BASE_DIRECTRY = './assets/logs/'


def main():
    service = Services()

    logging.basicConfig(filename=f'{BASE_DIRECTRY}{date.today()}.log', level=logging.DEBUG)
    logger = logging.getLogger('main')

    service.run_maintenance_script()
    delete_old_logs()
    service.set_brightness()
    try:   
        logger.info('Fetching video data...')
        video_data = service.fetch_json(f'?getvideos&equipid=1')
    except Exception as e:
        logger.critical(e)
        raise RuntimeError('Failed to fetch video data') from e
    
    app = QApplication([])
    w = App()
    w.set_video_data(service.filter_video_data(video_data))
    w.start_videos(service.filter_video_data(video_data))
    w.show()
    app.exec_()

def delete_old_logs():
    for filename in os.scandir(BASE_DIRECTRY):
        if not filename.is_file():
            continue
        date_created = filename.name[:10]
        week_ago = date.today() - timedelta(days=7)
        if date_created == str(week_ago):
            os.remove(os.path.join(BASE_DIRECTRY, filename.name))


if __name__ == "__main__":
    main()

sbc.fade_brightness(100, increment = 10)

