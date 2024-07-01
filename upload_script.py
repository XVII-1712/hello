import os
import requests
from Crypto.Cipher import AES
import base64

def encrypt_file(key, data):
    iv = b'\x00' * 12  # Fixed IV for testing
    cipher = AES.new(bytes.fromhex(key), AES.MODE_GCM, nonce=iv)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return base64.b64encode(ciphertext).decode(), base64.b64encode(tag).decode()

def upload_to_nextcloud(url, username, password, file_path, key):
    with open(file_path, 'rb') as file:
        data = file.read()
    ciphertext, tag = encrypt_file(key, data)
    
    response = requests.put(
        f"{url}/remote.php/webdav/{os.path.basename(file_path)}",
        data=ciphertext,
        auth=(username, password)
    )
    print(f"Upload status for {file_path}: {response.status_code}")

key = "c63edde7450839a52c43514dedee13d6"
nextcloud_url = "http://localhost:8080"
username = "xvii"
password = "tiff2013"
directory = "/path/to/your/files"

for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path):
        upload_to_nextcloud(nextcloud_url, username, password, file_path, key)
