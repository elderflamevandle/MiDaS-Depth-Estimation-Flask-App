import cv2
import torch
import numpy as np
from flask import Flask, Response, render_template
from threading import Thread

app = Flask(__name__)

# Download the MiDaS model
midas = torch.hub.load('intel-isl/MiDaS', 'MiDaS_small')
midas.to('cpu')
midas.eval()

# Input transformation pipeline
transforms = torch.hub.load('intel-isl/MiDaS', 'transforms')
transform = transforms.small_transform 

# Global variables for frame sharing
current_frame = None
current_depth_map = None

def generate_depth_map(frame):
    global current_depth_map
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    imgbatch = transform(img).to('cpu')

    with torch.no_grad():
        prediction = midas(imgbatch)
        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=img.shape[:2],
            mode='bicubic',
            align_corners=False
        ).squeeze()
        
    output = prediction.cpu().numpy()
    
    # Normalize the depth map for visualization
    depth_map = cv2.normalize(output, None, 0, 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    depth_map = (depth_map * 255).astype(np.uint8)
    depth_map = cv2.applyColorMap(depth_map, cv2.COLORMAP_INFERNO)
    
    current_depth_map = depth_map

def capture_video():
    global current_frame
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret:
            current_frame = frame
            generate_depth_map(frame)
        else:
            break
    cap.release()

def generate_frames():
    while True:
        if current_depth_map is not None:
            ret, buffer = cv2.imencode('.jpg', current_depth_map)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Start video capture in a separate thread
    Thread(target=capture_video).start()
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)