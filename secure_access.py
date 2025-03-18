import subprocess

print("🔒 Authenticating with face recognition...")

# Run face authentication script and capture the output
result = subprocess.run(["python", "face_authentication.py"], capture_output=True, text=True)

# Debugging: Print the raw output
print("DEBUG OUTPUT:", result.stdout)

# Check if "Access Granted" is in the output
if "Access Granted" in result.stdout:
    print("✅ Authentication successful! Access granted.")
else:
    print("❌ Authentication failed! Access denied.")


