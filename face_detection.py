from flask import Flask, render_template, jsonify, request
import subprocess
from cryptography.fernet import Fernet
import os
import base64

app = Flask(__name__)

# -------------------- Encryption Functions -------------------- #
def generate_key():
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)

def load_key():
    if not os.path.exists("secret.key"):
        raise FileNotFoundError("Encryption key not found!")
    return open("secret.key", "rb").read()

def encrypt_message(message):
    key = load_key()
    f = Fernet(key)
    return f.encrypt(message.encode())

def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    return f.decrypt(encrypted_message).decode()

def encrypt_image(image_data):
    key = load_key()
    f = Fernet(key)
    return f.encrypt(image_data.encode())

def decrypt_image(encrypted_image):
    key = load_key()
    f = Fernet(key)
    return f.decrypt(encrypted_image).decode()

# -------------------- Flask Routes -------------------- #
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/authenticate", methods=["POST"])
def authenticate():
    try:
        print("🔍 Running face authentication...")

        # Run face authentication script
        result = subprocess.run(
            ["python", "face_authentication.py"], 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8"
        )

        print("🔹 STDOUT:", result.stdout)
        print("🔻 STDERR:", result.stderr)

        if "Access Granted" in result.stdout:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/encrypt", methods=["POST"])
def encrypt():
    try:
        data = request.json
        message = data.get("message", "")

        if not message:
            return jsonify({"success": False, "error": "No message provided!"})

        encrypted_message = encrypt_message(message)
        return jsonify({"success": True, "encrypted_message": encrypted_message.decode()})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/decrypt", methods=["POST"])
def decrypt():
    try:
        print("🔒 Starting authentication before decryption...")

        # Step 1: Run face authentication first
        result = subprocess.run(
            ["python", "face_authentication.py"], 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8"
        )

        print("🔹 Authentication Output:", result.stdout)

        if "Access Granted" not in result.stdout:
            return jsonify({"success": False, "error": "Face authentication failed. Access Denied!"})

        # Step 2: Proceed with decryption if authentication is successful
        data = request.json
        encrypted_message = data.get("encrypted_message", "")

        if not encrypted_message:
            return jsonify({"success": False, "error": "No encrypted message provided!"})

        try:
            decrypted_message = decrypt_message(encrypted_message.encode())
        except Exception:
            return jsonify({"success": False, "error": "Invalid encrypted message!"})

        return jsonify({"success": True, "decrypted_message": decrypted_message})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/encrypt_image", methods=["POST"])
def encrypt_uploaded_image():
    try:
        image = request.files.get("image")
        if not image:
            return jsonify({"success": False, "error": "No image uploaded!"})

        # Convert image to Base64 and encrypt
        image_data = base64.b64encode(image.read()).decode()
        encrypted_image = encrypt_image(image_data)

        return jsonify({"success": True, "encrypted_image": encrypted_image.decode()})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/decrypt_image", methods=["POST"])
def decrypt_uploaded_image():
    try:
        print("🔒 Authenticating before decrypting image...")

        # Step 1: Authenticate before decrypting
        result = subprocess.run(
            ["python", "face_authentication.py"], 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8"
        )

        print("🔹 Authentication Output:", result.stdout)

        if "Access Granted" not in result.stdout:
            return jsonify({"success": False, "error": "Face authentication failed. Access Denied!"})

        # Step 2: Proceed with decryption if authentication is successful
        data = request.json
        encrypted_image = data.get("encrypted_image", "")

        if not encrypted_image:
            return jsonify({"success": False, "error": "No encrypted image provided!"})

        decrypted_image_data = decrypt_image(encrypted_image.encode())

        return jsonify({"success": True, "decrypted_image": decrypted_image_data})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    generate_key()
    app.run(debug=True)
