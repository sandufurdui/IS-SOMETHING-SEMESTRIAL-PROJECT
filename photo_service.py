from fastapi import FastAPI, HTTPException, Form
import base64
from pydantic import BaseModel
import httpx

app = FastAPI()

class PhotoUpload(BaseModel):
    image: str
    description: str
    publish_date: int

@app.post("/photo/")
async def upload_photo(data: PhotoUpload):
    try: 
        image_bytes = base64.b64decode(data.image.encode('utf-8'))
 
        with open(f"photos/{data.publish_date}.jpg", "wb") as img_file:
            img_file.write(image_bytes)

        return {"message": "Photo uploaded successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def make_http_request():
    async with httpx.AsyncClient() as client:
        payload = {"service_name": "photo_service"}  # Add service_name field with a value
        response = await client.post('http://127.0.0.1:8000/register', json=payload)
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Failed to make HTTP request, status code: {response.status_code}")
        
        print("successfully registered")

@app.on_event("startup")
async def startup_event():
    await make_http_request()
    
if __name__ == "__main__":
    print("Starting Service...")
    # uvicorn photo_service:app --reload --host 127.0.0.1 --port 8051
    # uvicorn.run(app, host="127.0.0.2", port=10000)
