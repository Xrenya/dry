import requests
import json 
import numpy as np
import cv2

url = "http://127.0.0.1:8000/files"

multiple_files = [
        ('image1', ('image.png', open('image.png', 'rb'), 'image/png')),
        ('image2', ('image.png', open('image.png', 'rb'), 'image/png'))
]

r = requests.post(url, files=multiple_files)
print(r.text)
