# Ad app

## Description
This is a video advertising processing application developed using PyQt5. It allows users to stream and display videos using a specified URL. The app includes features such as full screen mode, QR code generation, and video response tracking.

## How does it work
The application consists of three main components:
1. `main.py` - Entry point to the application. Initializes the GUI and handles user interactions.
2. `application.py` - Contains the main application logic, including the video player widget and main window.
3. `video_player.py` - PyQt video widget
4. `services.py` - includes additional functions for various services, such as video registration and control settings.

### Main functions
- **Full Screen Video**: Video is displayed in full screen for maximum environmental coverage.
- **QR Code Generation**: sequential application of QR codes that can be used to quickly access additional information.
- **Output Output Monitoring**: The application monitors the video output status and can take actions when the output is completed.

## Dependencies
To run this project you need to install the following dependencies:
- Python 3.x
- PyQt5
- Requests
- QR code
- geocoder
- os
- subprocess


You can install using the following command:
``` bash
pip install PyQt5 requests qrcode geocoder
```


# Приложение для воспроизведения рекламы

## Описание
Это приложение для воспроизведения видео рекламы, разработанное с использованием PyQt5. Оно позволяет пользователям транслировать и отображать видео по указанному URL. Приложение включает в себя функции, такие как полноэкранный режим, генерация QR-кодов и отслеживание статуса воспроизведения видео.

## Как работает
Приложение состоит из трех основных компонентов:
1. `main.py` - Точка входа в приложение. Инициализирует графический интерфейс и обрабатывает взаимодействия с пользователем.
2. `application.py` - Содержит основную логику приложения, включая виджет видеоплеера и главное окно.
3. `services.py` - Включает вспомогательные функции для различных сервисов, таких как регистрация видео и управление конфигурацией.

### Основные функции
- **Полноэкранное воспроизведение видео**: Видео отображается в полноэкранном режиме для максимального охвата аудитории.
- **Генерация QR-кодов**: Приложение генерирует QR-коды, которые могут быть использованы для быстрого доступа к дополнительной информации.
- **Отслеживание статуса воспроизведения**: Приложение отслеживает статус воспроизведения видео и может выполнять действия по завершении воспроизведения.

## Зависимости
Для запуска этого проекта необходимо установить следующие зависимости:
- Python 3.x
- PyQt5
- requests
- qrcode
- geocoder

Вы можете установить зависимости с помощью следующей команды:
```bash
pip install PyQt5 requests qrcode geocoder
```
