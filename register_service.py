from fastapi import FastAPI, HTTPException, Form
import base64
from pydantic import BaseModel
import httpx

app = FastAPI()

class GetService(BaseModel):
    service_name: str
    start_date: int
    
class RegisterService(BaseModel):
    service_name: str
    start_date: int

@app.get("/get_service")
async def upload_photo(data: GetService):
    try:
        return {"service_name": data.service_name, "is_active": True}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/register_service")
async def upload_photo(data: RegisterService):
    try:
        return {"message": f"Service {data.service_name} registered successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
 
if __name__ == "__main__":
    print("Starting Service...") 
    # uvicorn register_service:app --reload --host 127.0.0.1 --port 8050