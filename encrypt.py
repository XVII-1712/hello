from Crypto.Cipher import AES
import base64

def encrypt_file(key, data):
    cipher = AES.new(bytes.fromhex(key), AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return base64.b64encode(ciphertext).decode(), base64.b64encode(tag).decode()

if __name__ == '__main__':
    # Use the generated QKD key
    key = "c63edde7450839a52c43514dedee13d6"
    data = b"Example data to encrypt."

    ciphertext, tag = encrypt_file(key, data)
    print("Encrypted:", ciphertext)
    print("Tag:", tag)
