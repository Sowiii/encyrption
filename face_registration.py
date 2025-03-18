import cv2
import face_recognition
import pickle
import os

# Create/Open the file to store authorized faces
file_path = "authorized_faces.pkl"

if os.path.exists(file_path):
    with open(file_path, "rb") as file:
        authorized_faces = pickle.load(file)
else:
    authorized_faces = {}

# Initialize webcam
video_capture = cv2.VideoCapture(0)

name = input("Enter your name: ")
print("Look at the camera to register your face...")

while True:
    ret, frame = video_capture.read()
    if not ret:
        continue

    # Convert BGR (OpenCV format) to RGB (face_recognition format)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detect faces and encode them
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    if face_encodings:
        authorized_faces[name] = face_encodings[0]  # Store the first detected face
        break

    cv2.imshow("Face Registration", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release webcam
video_capture.release()
cv2.destroyAllWindows()

# Save the face encoding
with open(file_path, "wb") as file:
    pickle.dump(authorized_faces, file)

print(f"Face registered successfully for {name}!")
