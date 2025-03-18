from cryptography.fernet import Fernet

# Function to generate a key and save it to a file
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Function to load the key from a file
def load_key():
    return open("secret.key", "rb").read()

# Function to encrypt a message
def encrypt_message(message):
    key = load_key()
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())

    # Convert bytes to list of blocks
    block_size = 4  # Example: Rotating in 4-byte blocks
    encrypted_blocks = [encrypted_message[i:i+block_size] for i in range(0, len(encrypted_message), block_size)]

    # Rotate blocks (circular shift right)
    rotated_blocks = encrypted_blocks[-1:] + encrypted_blocks[:-1]
    
    return b''.join(rotated_blocks)

# Function to decrypt a message
def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)

    # Reverse rotation (circular shift left)
    block_size = 4
    encrypted_blocks = [encrypted_message[i:i+block_size] for i in range(0, len(encrypted_message), block_size)]
    original_blocks = encrypted_blocks[1:] + encrypted_blocks[:1]

    original_encrypted_message = b''.join(original_blocks)

    decrypted_message = f.decrypt(original_encrypted_message).decode()
    return decrypted_message

# Example usage
if __name__ == "__main__":
    generate_key()  # Run only once
    message = "Hello, this is a secret message!"
    
    encrypted = encrypt_message(message)
    print(f"Encrypted with rotation: {encrypted}")
    
    decrypted = decrypt_message(encrypted)
    print(f"Decrypted: {decrypted}")
