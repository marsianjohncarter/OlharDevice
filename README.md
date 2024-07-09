

## Documentation

### Overview
This documentation is aimed at programmers who are unfamiliar with the codebase. It explains the purpose and functionality of each file and class in detail.

### Dependencies
Ensure the following dependencies are installed:
- PyQt5
- requests
- qrcode
- geopy
- darkdetect
- screen-brightness-control
- logging

Install the dependencies using:
```bash
pip install PyQt5 requests qrcode geopy darkdetect screen-brightness-control logging
```

### `main.py`

#### Purpose
The `main.py` file is the entry point of the application. It initializes the main components and starts the event loop.

#### `Main` Class
- **Initialization (`__init__`)**:
  - Creates an instance of `Services` to interact with external services.
  - Initializes the main application window (`App`).
  - Sets up a timer to periodically update the video list and UI.

- **Starting the Application (`start`)**:
  - Enters the Qt main event loop to start the application.

### `application.py`

#### Purpose
The `application.py` file contains the main application window, which manages the user interface and interactions.

#### `App` Class
- **Initialization (`__init__`)**:
  - Sets up the application window with a title and full-screen mode.
  - Initializes the `Services` class to get the current city.
  - Configures logging to record application events.
  - Sets up the central widget and layout for the UI components.
  - Adds a video player, message label, and QR code label to the layout.
  - Initializes the video list and diagnostic menu.

- **QR Code Generation (`create_qr_code`)**:
  - Generates a QR code from a given URL.

- **Message Display (`show_message`, `hide_message`)**:
  - Shows or hides the message label.

- **QR Code Display (`show_qr_code`, `hide_qr_code`)**:
  - Shows or hides the QR code label.

- **Video Management (`load_video_list`, `play_next_video`)**:
  - Loads the video list from the service and plays the next video in the list.

- **Video Status Check (`check_video_status`)**:
  - Checks the media player status and updates the UI accordingly.

- **Video Ended Signal (`send_video_ended_signal`)**:
  - Sends a signal to the server when a video ends.

### `services.py`

#### Purpose
The `services.py` file provides services related to location and screen brightness.

#### `Services` Class
- **Initialization (`__init__`)**:
  - Initializes the service class without any parameters.

- **Location Retrieval (`get_current_city`, `get_lat_lon`, `get_location`)**:
  - Gets the current latitude and longitude.
  - Retrieves the city name based on the latitude and longitude.

- **Screen Brightness (`set_brightness`)**:
  - Adjusts the screen brightness based on whether it's day or night.

### `video_player.py`

#### Purpose
The `video_player.py` file contains the video player component that plays videos.

#### `VideoPlayer` Class
- **Initialization (`__init__`)**:
  - Sets up the video player UI components.
  - Initializes the media player and connects it to the video widget.

- **Playing Videos (`show_local_video`)**:
  - Plays a local video file and handles any errors that occur.

- **Media Status Check (`check_status`)**:
  - Checks the media player status and emits a `finished` signal when a video ends.

