from fastapi import FastAPI, HTTPException
import requests
import base64
from pydantic import BaseModel
import time
app = FastAPI()


REGISTER_SERVICE_URL = 'http://127.0.0.1:8050/'
PHOTO_SERVICE_URL = 'http://127.0.0.1:8051/photo'
VIDEO_SERVICE_URL = 'http://127.0.0.1:8052/video'

class ServiceRegister(BaseModel):
    service_name: str
class VideoUpload(BaseModel):
    video: str
    description: str
    publish_date: int

class PhotoUpload(BaseModel):
    image: str
    description: str
    publish_date: int
    

@app.post("/register")
async def register_service(data: ServiceRegister):
    print(data.service_name)
    payload = {
        'service_name': data.service_name, 
        'start_date': int(time.time())
    }
    
    # headers = {'Content-Type': 'application/json'}
    response = requests.post(f"{REGISTER_SERVICE_URL}register_service", json=payload)
    if response.status_code == 200:
            return {"message": "Service registered successfully"}
    else:
            raise HTTPException(status_code=500, detail="Failed to upload video")
 
    # return "urmom"

@app.post("/upload-video")
async def upload_video(data: VideoUpload):
    try: 
        video_bytes = base64.b64decode(data.video.encode('utf-8'))

        payload = {
            'video': data.video,
            'description': data.description,
            'publish_date': data.publish_date
        }

        response = requests.post(VIDEO_SERVICE_URL, json=payload)

        if response.status_code == 200:
            return {"message": "Video uploaded successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to upload video")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-photo/")
async def upload_photo(data: PhotoUpload):
    try: 
        image_bytes = base64.b64decode(data.image.encode('utf-8'))

        payload = {
            'image': data.image,
            'description': data.description,
            'publish_date': data.publish_date
        }

        response = requests.post(PHOTO_SERVICE_URL, json=payload)

        if response.status_code == 200:
            return {"message": "Photo uploaded successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to upload photo")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("Starting gateway...")
    # uvicorn gateway:app --reload --host 127.0.0.1 --port 8000
    # uvicorn.run(app, host="127.0.0.1", port=5000)