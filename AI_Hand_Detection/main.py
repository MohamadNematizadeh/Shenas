import time
import random
import requests
import mediapipe as mp
from fastapi import FastAPI
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

app = FastAPI()
base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)

@app.get("/")
def root():
    return {"Hello": "👋🏻"}


@app.post("/auth/gesture")
async def gesture():
    images = []
    results = []
    for image_file_name in IMAGE_FILENAMES:
    image = mp.Image.create_from_file(image_file_name)
    recognition_result = recognizer.recognize(image)
    images.append(image)
    top_gesture = recognition_result.gestures[0][0]
    hand_landmarks = recognition_result.hand_landmarks
    results.append((top_gesture, hand_landmarks))
    return {"result": results}
