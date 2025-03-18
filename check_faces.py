import pickle

# Load the stored face encodings
try:
    with open("authorized_faces.pkl", "rb") as file:
        data = pickle.load(file)
    print("Data type of stored faces:", type(data))
    print("Stored face data:", data)
except FileNotFoundError:
    print("Error: 'authorized_faces.pkl' file not found!")
except Exception as e:
    print("Error loading file:", e)
