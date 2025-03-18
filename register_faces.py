import cv2
import face_recognition
import pickle
import os
import numpy as np

# File where authorized faces will be stored
FACE_DATA_FILE = "authorized_faces.pkl"

# Load existing faces if the file exists
if os.path.exists(FACE_DATA_FILE):
    with open(FACE_DATA_FILE, "rb") as f:
        try:
            authorized_faces = pickle.load(f)
            if not isinstance(authorized_faces, list):  # Ensure it's a list
                authorized_faces = []
        except Exception:
            authorized_faces = []
else:
    authorized_faces = []

# Start webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Error: Could not access the camera!")
    exit()

name = input("Enter your name: ")
print(f"📸 Look directly at the camera, {name}, to register your face...")

registered = False

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Error: Failed to capture image. Try again.")
        break

    # Detect face
    face_locations = face_recognition.face_locations(frame)
    if face_locations:
        face_encoding = face_recognition.face_encodings(frame, face_locations)[0]

        # Check if this face is already registered
        if any(np.array_equal(face_encoding, face) for face in authorized_faces):
            print(f"⚠️ Face already registered for {name}.")
        else:
            authorized_faces.append(face_encoding)
            print(f"✅ Face registered successfully for {name}.")

            # Save to file
            with open(FACE_DATA_FILE, "wb") as f:
                pickle.dump(authorized_faces, f)

        registered = True
        break  # Exit loop after successful registration

    print("⚠️ No face detected. Please adjust your position.")

# Release resources
cap.release()
cv2.destroyAllWindows()

if not registered:
    print("❌ Face registration failed. Please try again.")
