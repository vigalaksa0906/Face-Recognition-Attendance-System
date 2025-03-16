# encode_faces.py
import os
import cv2
import numpy as np
import face_recognition
import pickle

# Dataset folder
dataset_path = "dataset/"
known_encodings = []
known_names = []

# Read all images in the folder
def process_images():
    for file_name in os.listdir(dataset_path):
        img_path = os.path.join(dataset_path, file_name)
        image = cv2.imread(img_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Extract face encoding
        encodings = face_recognition.face_encodings(rgb_image)
        if len(encodings) > 0:
            known_encodings.append(encodings[0])
            known_names.append(os.path.splitext(file_name)[0])  # Use the file name as the student's name

# Process images in the dataset
process_images()

# Save face encodings to a file
with open("encodings.pickle", "wb") as file:
    pickle.dump({"encodings": known_encodings, "names": known_names}, file)

print("Face encodings have been successfully saved!")
