import cv2
import face_recognition
import pickle
import time

# Load authorized face encodings
try:
    with open("authorized_faces.pkl", "rb") as file:
        authorized_faces = pickle.load(file)
except FileNotFoundError:
    print("❌ Error: authorized_faces.pkl not found!")
    exit()

# Open webcam
video_capture = cv2.VideoCapture(0)

print("🔍 Scanning for face... (Will timeout in 10 seconds)")

start_time = time.time()
face_detected = False

while True:
    ret, frame = video_capture.read()
    
    if not ret:
        print("❌ Error: Could not access the camera!")
        break

    # Detect faces
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(authorized_faces, face_encoding)
        
        if True in matches:
            print("✅ Face recognized! Access Granted.")
            face_detected = True
            break
    
    # Break loop if face is detected
    if face_detected:
        break

    # Timeout after 10 seconds if no face is found
    if time.time() - start_time > 5:
        print("❌ No face detected! Access Denied.")
        break

# Release the webcam
video_capture.release()
cv2.destroyAllWindows()

# Return authentication result
if face_detected:
    exit(0)  # Success
else:
    exit(1)  # Failure
