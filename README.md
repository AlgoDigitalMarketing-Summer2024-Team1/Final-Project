# Final-Project
Link to Project Proposal:
https://codelabs-preview.appspot.com/?file_id=1fHuGWmN9732xF4Ji26UGLFjRi00PhTNXTg_YafygkHs#6


Link To Codelabs Final Presentation: 
https://codelabs-preview.appspot.com/?file_id=1NRmxaS3stuKiR7zLzvo4bAdQ6Suobo8QTOXK4RPAyqI/edit#0

# Anima AI

Anima AI is an application that allows users to upload a video, extract frames, and generate images using a pre-trained model hosted on a Gradio client. The project utilizes FastAPI for backend frame extraction and Streamlit for the frontend interface, enabling seamless interaction with the AI model.

## Project Structure

- **FastAPI Backend**: Handles video upload and frame extraction.
- **Streamlit Frontend**: Provides the user interface for uploading videos, generating images, and displaying results.
- **Gradio Client**: Interacts with an external model to generate images based on extracted frames.

## Prerequisites

Before running this project, ensure you have the following installed:

- Python 3.7+
- pip
- Virtualenv (optional but recommended)

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/anima-ai.git
cd anima-ai
```
 ### 2. Go to the Streamlit directory and Fastapi Directory

#### Streamlit
##### Create a virtual environment
```bash
python -m venv venv
```
##### Activate the virtual environment
```bash
venv\Scripts\activate
```
##### Install requirements
```bash
pip install -r requirements.txt
```
##### Start streamlit server
```bash
streamlit run temp.py
```

#### FastAPI
##### Create a virtual environment
```bash
python -m venv venv
```
##### Activate the virtual environment
```bash
venv\Scripts\activate
```
##### Install requirements
```bash
pip install -r requirements.txt
```
##### Start FastApi server
```bash
uvicorn backend2:app --reload
```

You are all set!!
