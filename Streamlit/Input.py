import streamlit as st
from gradio_client import Client
import tempfile
import json
 
# Title and description
st.title("Gradio Client Streamlit App")
st.write("This app interacts with a Gradio app hosted at https://hysts-controlnet-v1-1.hf.space/")
 
# Multiple image upload
uploaded_files = st.file_uploader("Upload images:", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
image_paths = []
 
if uploaded_files is not None:
    for uploaded_file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            image_paths.append(temp_file.name)
   
    for image_path in image_paths:
        st.image(image_path, caption="Uploaded Image", use_column_width=True)
else:
    st.write("Please upload images.")
 
# Other user inputs
prompt = st.text_input("Enter the main prompt:", "Howdy!")
additional_prompt = ''
negative_prompt = ''
num_images = 1
image_resolution = 657
preprocess_resolution = 430
num_steps = 78
guidance_scale = 23.24
seed = 0
preprocessor = "Openpose"
 
# Button to run the Gradio model
if st.button("Generate Image") and uploaded_files:
    with st.spinner("Generating images..."):
        client = Client("https://hysts-controlnet-v1-1.hf.space/")
        results = []
        for image_path in image_paths:
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
            results.append(result)
            json_file_path = result + '/captions.json'
            with open(json_file_path, 'r') as f:
                image_paths = json.load(f)
 
            for key in image_paths.keys():
                st.image(key)
 
# Instructions and explanation
st.write("Upload images, enter the details above, and click 'Generate Image' to see the results.")