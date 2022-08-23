import os, sys, io
import PIL
import cv2
import requests
from urllib.request import urlopen
from urllib.parse import urlparse
import numpy as np

min_attributes = ('scheme', 'netloc')

def is_valid(url, qualifying=min_attributes):
    tokens = urlparse(url)
    return all([getattr(tokens, qualifying_attr) for qualifying_attr in qualifying])

def read_img_path(path:str):
    if is_valid(path):
        # response = requests.get(path)
        # image_bytes = io.BytesIO(response.content)
        # img = PIL.Image.open(image_bytes)
        response = urlopen(path)
        arr = np.array(bytearray(response.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    else:
        img = cv2.imread(path)
    return img