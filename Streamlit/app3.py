import cv2
import mediapipe as mp
import numpy as np
import streamlit as st
import requests

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Streamlit App
st.title("Move like Goku - Live Pose Tracking")

detailed_caption = st.text_input("Enter detailed caption of the character you want to animate:")

if st.button("Generate Image"):
    if detailed_caption:
        # Call the FastAPI service
        try:
            response = requests.get(
                "http://127.0.0.1:8000/generate-image/",
                params={
                    "detailed_caption": detailed_caption  
                }
            )
            response_data = response.json()

            if response.status_code == 200:
                # Display the generated image
                st.image(response_data["image_url"], caption="Generated Image")
            else:
                st.error(f"Error: {response_data['detail']}")

        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please fill in all the fields.")

# Load Goku image
goku_image = cv2.imread("goku.png", cv2.IMREAD_UNCHANGED)

# Function to overlay Goku image at a specified landmark
def overlay_image(background, overlay, x, y, scale=1.0):
    # Resize the overlay image
    overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    h, w, _ = overlay.shape
    rows, cols, _ = background.shape

    # Ensure the overlay does not exceed the background image boundaries
    y1, y2 = max(0, y - h // 2), min(rows, y + h // 2)
    x1, x2 = max(0, x - w // 2), min(cols, x + w // 2)

    # Adjust overlay to fit within the determined bounding box
    overlay_y1 = max(0, h // 2 - y)
    overlay_y2 = overlay_y1 + (y2 - y1)
    overlay_x1 = max(0, w // 2 - x)
    overlay_x2 = overlay_x1 + (x2 - x1)

    # Slice the overlay image and the corresponding part of the background
    overlay = overlay[overlay_y1:overlay_y2, overlay_x1:overlay_x2]

    # Now ensure the sliced overlay matches the background slice dimensions
    background_slice = background[y1:y2, x1:x2]

    # Check dimensions before blending to avoid broadcasting issues
    if overlay.shape[:2] == background_slice.shape[:2]:
        alpha_s = overlay[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            background[y1:y2, x1:x2, c] = (alpha_s * overlay[:, :, c] +
                                           alpha_l * background_slice[:, :, c])
    else:
        print(f"Dimension mismatch: overlay {overlay.shape[:2]} vs background slice {background_slice.shape[:2]}")

    return background


# Video capture
run = st.checkbox('Run')
frame_window = st.image([])

cap = cv2.VideoCapture(0)

while run:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the BGR image to RGB.
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the image and find the pose landmarks
    results = pose.process(image)
    
    # Draw the pose annotation on the image.
    annotated_image = image.copy()
    
    if results.pose_landmarks:
        # Example: Overlay Goku at the nose position
        nose_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]
        h, w, _ = image.shape
        nose_x, nose_y = int(nose_landmark.x * w), int(nose_landmark.y * h)
        
        # Overlay the Goku image on the nose position
        scale = 0.2  # Adjust the scale of Goku relative to the pose
        annotated_image = overlay_image(annotated_image, goku_image, nose_x, nose_y, scale)

    # Convert back to BGR for rendering in Streamlit
    annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
    
    # Display the resulting frame
    frame_window.image(annotated_image)

else:
    cap.release()
    cv2.destroyAllWindows()

st.write("Click the checkbox to start/stop the live video.")


