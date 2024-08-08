# MiDaS Depth Estimation Flask App

This is a Flask web application that uses the MiDaS model to generate depth maps from a live video feed. The depth maps are displayed alongside the video feed.

## Requirements

- Python 3.7 or later
- The required Python packages are listed in the `requirements.txt` file.

## Installation

1. Create a new virtual environment and activate it:
   ```
   python -m venv venv
    source venv/bin/activate
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask app

2. Open your web browser and go to `http://localhost:5000/`. You should see the live video feed with depth estimation and a bar graph displaying the depth values.

## Endpoints

- **`/`** (GET): This is the root endpoint that renders the `index.html` template, which displays the video feed with depth estimation.
- **`/video_feed`** (GET): This endpoint generates the video frames with depth estimation and returns them as a multipart/x-mixed-replace response, which allows the client to continuously display the video feed.

## Files

- `app.py`: The main Flask application file that handles the video capture, depth estimation, and rendering.
- `templates/index.html`: The Jinja template file that displays the video feed and depth plot.

## Customization

You can customize the following aspects of the application:

- **MiDaS Model Type**: The current implementation uses the `'MiDaS_small'` model. You can change this by modifying the `model_type` parameter in the `midas_depth_maps()` function. The available options are `'DPT_Large'`, `'DPT_Hybrid'`, or `'MiDaS_small'`.
- **Video Resolution**: The video resolution is set to the default camera resolution. You can modify the video capture settings by changing the `cap = cv2.VideoCapture(0)` line in the `capture_video()` function.
- **Depth Plot Appearance**: The appearance of the depth value bar graph can be customized by modifying the Matplotlib code in the `generate_frames()` function.

## License

This project is licensed under the [MIT License](LICENSE).


