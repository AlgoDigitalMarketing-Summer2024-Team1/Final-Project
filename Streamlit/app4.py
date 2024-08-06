import cv2
import mediapipe as mp
import streamlit as st

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Streamlit App
st.title("Live Skeleton Mapping using BlazePose")

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
    
    # Process the image to find pose landmarks
    results = pose.process(image)
    
    # Draw the skeleton on the image.
    annotated_image = image.copy()
    if results.pose_landmarks:
        # Draw the pose skeleton
        mp_drawing.draw_landmarks(
            annotated_image, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),  # Joint points
            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)   # Connections
        )
    
    # Convert back to BGR for rendering in Streamlit
    annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
    
    # Display the resulting frame
    frame_window.image(annotated_image)

else:
    cap.release()
    cv2.destroyAllWindows()

st.write("Click the checkbox to start/stop the live video.")
