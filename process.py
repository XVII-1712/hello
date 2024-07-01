import base64
from Crypto.Cipher import AES
import requests

def encrypt_file(key, data):
    iv = b'\x00' * 12  # Fixed IV for testing
    cipher = AES.new(bytes.fromhex(key), AES.MODE_GCM, nonce=iv)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return base64.b64encode(ciphertext).decode(), base64.b64encode(tag).decode()

def decrypt_file(key, ciphertext, tag):
    iv = b'\x00' * 12  # Fixed IV for testing
    cipher = AES.new(bytes.fromhex(key), AES.MODE_GCM, nonce=iv)
    data = cipher.decrypt_and_verify(base64.b64decode(ciphertext), base64.b64decode(tag))
    return data

def upload_to_nextcloud(url, username, password, filename, data):
    response = requests.put(
        f"{url}/{filename}",
        auth=(username, password),
        data=data
    )
    response.raise_for_status()

def download_from_nextcloud(url, username, password, filename):
    response = requests.get(
        f"{url}/{filename}",
        auth=(username, password)
    )
    response.raise_for_status()
    return response.content

if __name__ == '__main__':
    key = "c63edde7450839a52c43514dedee13d6"

    # Encrypt
    with open('Djago.txt', 'rb') as file:
        data = file.read()
    ciphertext, tag = encrypt_file(key, data)
    print("Encrypted:", ciphertext)
    print("Tag:", tag)

    # Upload
    nextcloud_url = "http://127.0.0.1:8080/remote.php/webdav"
    username = "xvii"
    password = "tiff2013"
    upload_to_nextcloud(nextcloud_url, username, password, "encrypted.txt", f"{ciphertext}\n{tag}")

    # Download
    downloaded_data = download_from_nextcloud(nextcloud_url, username, password, "encrypted.txt")
    downloaded_ciphertext, downloaded_tag = downloaded_data.decode().split('\n')

    # Decrypt
    try:
        decrypted_data = decrypt_file(key, downloaded_ciphertext, downloaded_tag)
        print("Decrypted:", decrypted_data.decode())
    except ValueError as e:
        print("Decryption failed:", e)
