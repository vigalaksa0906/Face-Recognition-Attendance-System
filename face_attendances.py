import cv2
import face_recognition
import numpy as np
import pickle
import pandas as pd
from datetime import datetime

# Load encoding wajah yang sudah disimpan
with open("encodings.pickle", "rb") as file:
    data = pickle.load(file)

# Buka webcam
video_capture = cv2.VideoCapture(0)

# Fungsi untuk mengecek apakah nama sudah ada di daftar hari ini
def is_already_recorded(name):
    try:
        df = pd.read_excel("kehadiran.xlsx")
        today = datetime.now().strftime("%Y-%m-%d")
        return any((df["Nama"] == name) & (df["Waktu Kehadiran"].str.startswith(today)))
    except FileNotFoundError:
        return False

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Konversi warna untuk face-recognition
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Deteksi wajah
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        # Bandingkan dengan wajah yang dikenal
        matches = face_recognition.compare_faces(data["encodings"], face_encoding)
        name = "Tidak Dikenal"

        if True in matches:
            match_index = matches.index(True)
            name = data["names"][match_index]

            # Cek apakah nama sudah dicatat hari ini
            if not is_already_recorded(name):
                # Simpan kehadiran ke file Excel
                df = pd.DataFrame([[name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]],
                                  columns=["Nama", "Waktu Kehadiran"])
                
                try:
                    old_df = pd.read_excel("kehadiran.xlsx")
                    df = pd.concat([old_df, df], ignore_index=True)
                except FileNotFoundError:
                    pass
                
                df.to_excel("kehadiran.xlsx", index=False)
                print(f"{name} dicatat pada {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Gambar kotak dan nama di wajah
        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Tampilkan hasil
    cv2.imshow("Face Recognition Absensi", frame)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Bersihkan
video_capture.release()
cv2.destroyAllWindows()
