import streamlit as st
import requests
import os
import json
import tempfile
import time
import shutil
from gradio_client import Client
from PIL import Image

# Streamlit app
st.title("Anima AI")

# Upload video file
uploaded_video = st.file_uploader("Upload a video", type=["mp4", "avi", "mov", "mkv"])

if uploaded_video is not None:
    # Save uploaded video to a temporary location
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(uploaded_video.getbuffer())
    video_path = temp_file.name
    
    # Send the video to FastAPI backend for frame extraction
    with st.spinner("Extracting frames..."):
        files = {'file': open(video_path, 'rb')}
        response = requests.post("http://localhost:8000/extract_frames", files=files)
    
    if response.status_code == 200:
        st.success("Frames extracted successfully.")
        frame_files = response.json()['frames']

        # Create a directory to save the frames
        output_frames_dir = "output_frames"
        os.makedirs(output_frames_dir, exist_ok=True)

        # Save the frames to the directory
        for frame in frame_files:
            # Get the frame name and destination path
            frame_name = os.path.basename(frame)
            destination_path = os.path.join(output_frames_dir, frame_name)
            
            # Copy the frame to the output directory
            shutil.copy(frame, destination_path)

        st.success(f"All frames have been saved in the '{output_frames_dir}' directory.")


time.sleep(3)

# Create a directory for downloads if it doesn't exist
download_dir = "downloaded_images"
skeleton_dir="skeleton_images"
os.makedirs(download_dir, exist_ok=True)
os.makedirs(skeleton_dir, exist_ok=True)
# Load files from 'output_frames' directory
output_frames_dir = "output_frames"
if os.path.exists(output_frames_dir):
    uploaded_files = [os.path.join(output_frames_dir, f) for f in os.listdir(output_frames_dir) if os.path.isfile(os.path.join(output_frames_dir, f))]
else:
    st.write("The 'output_frames' directory does not exist.")
    uploaded_files = []

image_paths = []

if uploaded_files:
    for file_path in uploaded_files:
        with open(file_path, "rb") as f:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(f.read())
                image_paths.append(temp_file.name)
else:
    st.write("No files found in 'output_frames' directory.")

# Other user inputs
prompt = st.text_input("Enter the main prompt:", "Howdy!")
additional_prompt = 'black background'
negative_prompt = ''
num_images = 1
image_resolution = 700
preprocess_resolution = 480
num_steps = 78
guidance_scale = 23.24
seed = 0
preprocessor = "Openpose"

# Button to run the Gradio model
if st.button("Generate Image") and uploaded_files:
    with st.spinner("Generating images..."):
        client = Client("https://hysts-controlnet-v1-1.hf.space/")
        for index, image_path in enumerate(image_paths):
            result = client.predict(
                image_path,             # Local file path of the uploaded image
                prompt,                 # Prompt
                additional_prompt,      # Additional prompt
                negative_prompt,        # Negative prompt
                num_images,             # Number of images
                image_resolution,       # Image resolution
                preprocess_resolution,  # Preprocess resolution
                num_steps,              # Number of steps
                guidance_scale,         # Guidance scale
                seed,                   # Seed
                preprocessor,           # Preprocessor
                api_name="/openpose"    # API endpoint
            )
            st.write(f"Creating image {index + 1}/{len(image_paths)}")

            json_file_path = result + '/captions.json'
            with open(json_file_path, 'r') as f:
                image_info = json.load(f)
                st.write(image_info.keys)
            first_key = list(image_info.keys())[0]
            second_key=list(image_info.keys())[1]
            new_file_path = os.path.join(skeleton_dir, f"image{index + 1}.jpg")
            new_file_path2 = os.path.join(download_dir, f"image{index + 1}.jpg")
            shutil.copy(first_key, new_file_path)
            shutil.copy(second_key, new_file_path2)
            
            # Download generated images directly into the folder with specified naming convention
            #for key in image_info.keys():
            #    print(key)
            #    # Define the new file path with custom name
            #    new_file_path = os.path.join(download_dir, f"image{index + 1}.jpg")
            #    new_file_path2 = os.path.join(skeleton_dir, f"image{index + 1}.jpg")
            #    # Copy file to the download directory with the new name
            #    shutil.copy(key, new_file_path)
            #    shutil.copy(key, new_file_path2)
                

# Instructions and explanation
st.write("...")

def load_images_from_folder(folder):
    images = []
    for filename in sorted(os.listdir(folder)):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            img_path = os.path.join(folder, filename)
            images.append(img_path)
    return images

# Set the number of frames per second
fps = 20
frame_duration = 1.0 / fps

# Layout with two columns
col1, col2 = st.columns(2)

# Load images for both columns
image_folder_skeleton = 'skeleton_images'
images_skeleton = load_images_from_folder(image_folder_skeleton)

image_folder = 'downloaded_images'
images = load_images_from_folder(image_folder)

# Display images in the first column
if images_skeleton:
    img_display1 = col1.image(Image.open(images_skeleton[0]))

# Display images in the second column
if images:
    img_display2 = col2.image(Image.open(images[0]))

# Ensure the videos play infinitely in both columns
while True:
    for i in range(max(len(images_skeleton), len(images))):
        if images_skeleton:
            img_display1.image(Image.open(images_skeleton[i % len(images_skeleton)]))
        if images:
            img_display2.image(Image.open(images[i % len(images)]))
        time.sleep(frame_duration)
