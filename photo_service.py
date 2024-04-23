from fastapi import FastAPI, HTTPException, Form
import base64
from pydantic import BaseModel
import httpx
import os
import psycopg2
import psycopg2.pool 
# from fastapi import FastAPI, HTTPException 
# from pydantic import BaseModel

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
POOL_MIN_CONN = 1  # Minimum number of connections in the pool
POOL_MAX_CONN = 10  # Maximum number of connections in the pool
 

pool = psycopg2.pool.SimpleConnectionPool(
    POOL_MIN_CONN,
    POOL_MAX_CONN,
    DATABASE_URL
)

def get_connection(): 
    return pool.getconn() 

def return_connection(conn):
    pool.putconn(conn)


import uuid


app = FastAPI()

class PhotoUpload(BaseModel):
    image: str
    uid: str
    description: str
    publish_date: int
    

@app.post("/photo")
async def upload_photo(data: PhotoUpload):
    conn = None
    try:
        # print(DATABASE_URL)  
        conn = get_connection()
        cur = conn.cursor()
        photo_id = str(uuid.uuid4())
        cur.execute("INSERT INTO photos (id, uid, description, publish_date, image_str) VALUES (%s, %s, %s, %s, %s)",
                    (photo_id, data.uid, data.description, data.publish_date, data.image))
        conn.commit()
        return {"photo_id": photo_id, "message": "Photo uploaded successfully"}
    except Exception as e:
        if conn:
            conn.rollback()
            
        raise HTTPException(status_code=500, detail="Failed to upload photo")
    finally:
        if conn:
            conn.close()


async def make_http_request():
    async with httpx.AsyncClient() as client:
        payload = {"service_name": "photo_service"}   
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
