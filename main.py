import os
from services import Services
from application import App
from PyQt5.QtWidgets import QApplication

BASE_URL = 'https://api.olhar.media/'

service = Services()

def main():
    try:
        script = service.fetch_script(f'{BASE_URL}?getconfigupdate&equipid=1')
        if script:
            if service.is_valid_bash(script):
                with open('script.sh', 'wb') as f:
                    f.write(script.encode())
                service.run_bash('./script.sh')
                os.remove('./script.sh')
            elif service.is_valid_python(script):
                with open('script.py', 'wb') as f:
                    f.write(script.encode())
                service.run_python('./script.py')
                os.remove('./script.py')
    except Exception as e:
        print(e)

    try:
        video_data = service.fetch_json(f'{BASE_URL}?getvideos&equipid=1')
    except Exception as e:
        raise e

if __name__ == "__main__":
    app = QApplication([])
    w = App()
    w.load_video_data(video_data)
    w.load_videos(video_data)
    w.show()
    app.exec_()
