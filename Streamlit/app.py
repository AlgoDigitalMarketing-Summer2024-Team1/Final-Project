import streamlit as st
import cv2
import mediapipe as mp
import tempfile
import numpy as np

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

def process_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    out = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert the BGR frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame with MediaPipe Pose
        results = pose.process(rgb_frame)
        
        if results.pose_landmarks:
            # Create a blank image for stickman
            stickman_frame = np.zeros_like(frame)
            
            # Draw the stickman on the blank image
            mp_drawing.draw_landmarks(stickman_frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2))
            
            # Blend the stickman image with the original frame
            blended_frame = cv2.addWeighted(frame, 0.5, stickman_frame, 0.5, 0)
            
            # Write the frame with the stickman to the output video
            if out is None:
                # Initialize video writer
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(output_path, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
            out.write(blended_frame)
    
    cap.release()
    if out:
        out.release()

# Streamlit UI
st.title("BlazePose Stickman Dance Mimicry")
st.write("Upload a video to replicate the dance moves as a stickman!")

# Video file upload
uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # Save the uploaded video to a temporary file
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    
    # Process the video and save the output
    output_path = "output_video.mp4"
    process_video(tfile.name, output_path)
    
    # Display the original and processed videos
    st.video(output_path)
