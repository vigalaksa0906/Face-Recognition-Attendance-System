import cv2
import face_recognition
import numpy as np
import pickle
import pandas as pd
from datetime import datetime

# Load previously saved face encodings
with open("encodings.pickle", "rb") as file:
    data = pickle.load(file)

# Open the webcam
video_capture = cv2.VideoCapture(0)

# Function to check if the name has already been recorded today
def is_already_recorded(name):
    try:
        df = pd.read_excel("kehadiran.xlsx")
        today = datetime.now().strftime("%Y-%m-%d")
        return any((df["Name"] == name) & (df["Attendance Time"].str.startswith(today)))
    except FileNotFoundError:
        return False

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Convert frame color for face recognition
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        # Compare with known faces
        matches = face_recognition.compare_faces(data["encodings"], face_encoding)
        name = "Unknown"

        if True in matches:
            match_index = matches.index(True)
            name = data["names"][match_index]

            # Check if the name has already been recorded today
            if not is_already_recorded(name):
                # Save attendance to Excel file
                df = pd.DataFrame([[name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]],
                                  columns=["Name", "Attendance Time"])
                
                try:
                    old_df = pd.read_excel("kehadiran.xlsx")
                    df = pd.concat([old_df, df], ignore_index=True)
                except FileNotFoundError:
                    pass
                
                df.to_excel("kehadiran.xlsx", index=False)
                print(f"{name} recorded at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Draw a box and name on the face
        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show the result
    cv2.imshow("Face Recognition Attendance", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
video_capture.release()
cv2.destroyAllWindows()
