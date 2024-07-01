import socket
import ssl

# Secure Client Setup
context = ssl.create_default_context()
context.load_verify_locations('C:/Users/mike/qlf_project/backend/backend/cert.pem')

# Disable certificate verification for self-signed certificates (only for testing)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Connect to Secure Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_client = context.wrap_socket(client, server_hostname='localhost')
secure_client.connect(('127.0.0.1', 443))

# Receive Message
message = secure_client.recv(1024)
print(message.decode('utf-8'))
secure_client.close()
