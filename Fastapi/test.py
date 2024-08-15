import pytest
from fastapi.testclient import TestClient
from backend2 import app  # Assuming your FastAPI app is in a file named `main.py`
import io
import os
client = TestClient(app)

def test_extract_frames():
    # Create a small dummy video file in memory for testing
    video = create_dummy_video()

    # Send a POST request to the /extract_frames endpoint with the dummy video file
    response = client.post("/extract_frames", files={"file": ("dummy_video.mp4", video, "video/mp4")})

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Get the response data
    response_data = response.json()

    # Assert that the 'frames' key is present in the response
    assert "frames" in response_data

   

def create_dummy_video():
    # Create a dummy video file using OpenCV
    import cv2
    import numpy as np

    width, height = 320, 240
    fps = 10
    duration = 2  # seconds
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter("movement.mp4", fourcc, fps, (width, height))

    for _ in range(fps * duration):
        # Create a dummy frame (plain white image)
        frame = np.ones((height, width, 3), dtype=np.uint8) * 255
        video.write(frame)

    video.release()

    # Read the video file into memory
    with open("movement.mp4", "rb") as f:
        video_bytes = io.BytesIO(f.read())

    # Clean up the dummy video file from the filesystem
    os.remove("movement.mp4")

    return video_bytes

