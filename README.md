# Face Recognition Attendance System
This project is an attendance system based on face recognition using Python. The system automatically records student attendance by detecting their faces through a webcam. Registered student faces are compared to the images captured by the webcam and their attendance time is recorded in an Excel file.

## Features

- Face recognition for automatic attendance.
- Attendance records stored in an Excel file (`kehadiran.xlsx`)
- Real-time face detection using a webcam.
- The system only records students who are present on the current day.

## Prerequisites
Ensure you have Python 3.10–3.11 installed.

The following Python libraries are required (with tested compatible versions):
```bash
numpy==1.23.5
opencv-python==4.11.0.86
face-recognition==1.3.0
face_recognition_models==0.3.0
dlib==19.24.1
pandas==2.2.3
openpyxl==3.1.5
Pillow==11.2.1
```
To install them, run:
```bash
pip install -r requirements.txt
```
Or manually:
```bash
pip install numpy==1.23.5 opencv-python==4.11.0.86 face-recognition==1.3.0 \
dlib==19.24.1 pandas==2.2.3 openpyxl==3.1.5 Pillow==11.2.1
```

## Folder Structures
```bash

face_recognition_attendance/
│── dataset/                   # Folder containing student face images
│   ├── Alice.jpg
│   ├── Bob.jpg
│   ├── Charlie.jpg
│── encode_faces.py             # Script to save face encodings to database
│── face_attendance.py          # Main script for attendance
│── encodings.pickle            # File containing face encodings (generated)
│── kehadiran.xlsx              # Excel file for recording attendance (generated automatically)
```

## Usage Steps

### 1. Prepare the Dataset
Place the student face images in the `dataset/` folder. Make sure the filenames of the images match the student names (e.g., `Alice.jpg`, `Bob.jpg`).

### 2. Save Face Encodings
Run the `encode_faces.py` script to generate the `encodings.pickle` file that contains the face encodings for the students.

```bash  
python encode_faces.py
```
### 3. Use the Attendance System
Run the `face_attendance.py` script to start using the face recognition-based attendance system. The program will use your webcam to detect students' faces and record their attendance.
```bash
python face_attendance.py
```
Once a face is detected and matched with a registered student, their attendance will be recorded in the kehadiran.xlsx file along with the timestamp.

### 4. Exiting the Program
To exit the program, press the `q` key while the video window is open.

## Handling Errors

If you encounter an issue installing the `dlib` library, which is used by the `face-recognition` package, you can refer to the following video tutorial for installation instructions:

[Video Tutorial: Dlib Installation](https://www.youtube.com/watch?v=pO150OCX-ac)

