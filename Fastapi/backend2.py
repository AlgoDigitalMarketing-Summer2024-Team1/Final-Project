from fastapi import FastAPI, File, UploadFile
import os
import cv2
import tempfile

app = FastAPI()

@app.post("/extract_frames")
async def extract_frames(file: UploadFile = File(...)):
    # Save uploaded video to a temporary location
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(await file.read())
    video_path = temp_file.name
    
    # Create output folder for frames
    output_folder = tempfile.mkdtemp()

    # Load the video
    vidcap = cv2.VideoCapture(video_path)

    # Calculate the total number of frames and fps
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    interval = total_frames // 20 if total_frames > 20 else 1

    count = 0
    frame_count = 0
    frames = []

    while frame_count < 20:
        success, image = vidcap.read()
        if not success:
            break
        if count % interval == 0:
            # Save the frame as a jpeg
            frame_filename = os.path.join(output_folder, f'frame{frame_count}.jpg')
            cv2.imwrite(frame_filename, image)
            frames.append(frame_filename)
            frame_count += 1
        count += 1

    vidcap.release()

    return {"frames": frames}
