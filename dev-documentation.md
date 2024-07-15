## Documentation for Developers

### Overview
This documentation is intended for developers who are familiar with the program's purpose. It provides detailed information on the functions, classes, and overall structure of the codebase.

### Dependencies
Ensure the following dependencies are installed:
- PyQt5
- requests
- qrcode
- geopy
- darkdetect
- screen-brightness-control

Install the dependencies using:
```bash
pip install PyQt5 requests qrcode geopy darkdetect screen-brightness-control 
```

### `main.py`

#### `Main` Class
- **Attributes:**
  - `service`: Instance of `Services` class.
  - `app`: Instance of `App` class.
- **Methods:**
  - `__init__(self)`: Initializes the `Main` class, creates a QApplication, an `App` instance, and sets up a timer for checking video list and updating the UI.

#### `start(self)`
Starts the application by entering the Qt main event loop.

### `application.py`

#### `App` Class
- Inherits from `QMainWindow`.
- **Attributes:**
  - `service`: Instance of `Services`.
  - `current_city`: Current city retrieved from `service`.
  - `logger`: Logger instance.
  - `central_widget`, `layout`, `video_player`, `message_label`, `qr_code_label`: UI components.
  - `current_video_index`, `video_list`: Video management attributes.
  - `diagnostic_menu`: Instance of `DiagnosticMenu`.
- **Methods:**
  - `__init__(self)`: Initializes the application window, sets up UI components, and configures logging.
  - `update_ui(self)`: Updates the UI components, including the current video.
  - `create_qr_code(self, url)`: Generates a QR code for the given URL.
  - `show_message(self)`: Displays a message.
  - `hide_message(self)`: Hides the message.
  - `show_qr_code(self, url)`: Displays the QR code for the given URL.
  - `hide_qr_code(self)`: Hides the QR code.
  - `load_video_list(self)`: Loads the video list from the service.
  - `play_next_video(self)`: Plays the next video in the list.
  - `check_video_status(self)`: Checks the video player status and updates the UI.
  - `send_video_ended_signal(self)`: Sends a signal to the server when a video ends.

### `services.py`

#### `Services` Class
- **Methods:**
  - `__init__(self)`: Initializes the service class.
  - `get_current_city(self)`: Retrieves the current city based on the user's location.
  - `get_lat_lon(self)`: Gets the current latitude and longitude.
  - `get_location(self)`: Uses the latitude and longitude to get the current city name.
  - `set_brightness(self)`: Adjusts the screen brightness based on the time of day.

### `video_player.py`

#### `VideoPlayer` Class
- Inherits from `QWidget`.
- **Attributes:**
  - `finished`: Signal emitted when a video finishes.
  - `layout`, `video_widget`, `media_player`: UI and media player components.
- **Methods:**
  - `__init__(self)`: Initializes the video player UI components.
  - `show_local_video(self, video_path)`: Plays a local video file.
  - `check_status(self, status)`: Checks the media player status and emits the `finished` signal when a video ends.
