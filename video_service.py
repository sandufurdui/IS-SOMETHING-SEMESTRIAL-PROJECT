

from fastapi import FastAPI, HTTPException, BackgroundTasks
import base64
from pydantic import BaseModel
import time
import httpx

app = FastAPI()

class VideoUpload(BaseModel):
    video: str
    description: str
    publish_date: int

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/video")
async def upload_video(data: VideoUpload):
    try:
        video_bytes = base64.b64decode(data.video.encode('utf-8'))

        with open(f"videos/{data.publish_date}.mp4", "wb") as video_file:
            video_file.write(video_bytes)

        return {"message": "Video uploaded successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def make_http_request():
    async with httpx.AsyncClient() as client:
        payload = {"service_name": "video_service"}  
        response = await client.post('http://127.0.0.1:8000/register', json=payload)
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Failed to make HTTP request, status code: {response.status_code}")
        
        print("successfully registered")

@app.on_event("startup")
async def startup_event():
    await make_http_request()

if __name__ == "__main__":
    print("urmom") 
    # uvicorn video_service:app --reload --host 127.0.0.1 --port 8052
