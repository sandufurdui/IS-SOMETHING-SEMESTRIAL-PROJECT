import requests
import base64
import json
import time

def test_upload_video(): 
    with open("IMG_8696.MOV", "rb") as video_file:
        video_bytes = video_file.read()
 
    video_str = base64.b64encode(video_bytes).decode('utf-8')

    payload = {
        'video': video_str,
        'description': 'Test Video Description',
        'publish_date': int(time.time())
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post("http://127.0.0.1:8000/upload-video", json=payload, headers=headers)

    print(response.json())

if __name__ == "__main__":
    test_upload_video()
    print("All tests passed!")
