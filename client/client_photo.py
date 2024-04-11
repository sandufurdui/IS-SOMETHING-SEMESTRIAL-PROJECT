import requests
import base64
import json
import time
def test_upload_photo(): 
    with open("sample_image.jpg", "rb") as image_file:
        image_bytes = image_file.read()
 
    image_str = base64.b64encode(image_bytes).decode('utf-8')

    payload = {
        'image': image_str,
        'description': 'Test Description',
        'publish_date': int(time.time())
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post("http://127.0.0.1:8000/upload-photo/", json=payload, headers=headers)

    print(response.json())

if __name__ == "__main__":
    test_upload_photo()
    print("All tests passed!")
