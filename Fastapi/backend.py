from fastapi import FastAPI, HTTPException
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize FastAPI
app = FastAPI()



# Load your OpenAI API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.get("/generate-image/")
async def generate_image(detailed_caption):
    try:
        # Construct the prompt
        prompt = (
            f"{detailed_caption}. Given is the description of a character. "
            f"Generate the FULL BODY image (NOT CLOSE UPS) of the character (standing straight) (including hands,legs,face,torso) in a white background and MAKE SURE THERE IS ONLY ONE PERSON/FIGURE IN THE IMAGE and nothing else"
        )
        
        # Call OpenAI API to generate the image
        response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                #size="1024x1024",
                quality="standard",
                n=1,
            )
        print(response)

        # Return the image URL
        return {"image_url": response.data[0].url}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



