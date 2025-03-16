# encode_faces.py
import os
import cv2
import numpy as np
import face_recognition
import pickle

# Folder dataset
dataset_path = "dataset/"
known_encodings = []
known_names = []

# Baca semua gambar dalam folder
def process_images():
    for file_name in os.listdir(dataset_path):
        img_path = os.path.join(dataset_path, file_name)
        image = cv2.imread(img_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Ekstrak encoding wajah
        encodings = face_recognition.face_encodings(rgb_image)
        if len(encodings) > 0:
            known_encodings.append(encodings[0])
            known_names.append(os.path.splitext(file_name)[0])  # Gunakan nama file sebagai nama siswa

# Proses gambar dalam dataset
process_images()

# Simpan encoding wajah ke dalam file
with open("encodings.pickle", "wb") as file:
    pickle.dump({"encodings": known_encodings, "names": known_names}, file)

print("Encoding wajah berhasil disimpan!")
