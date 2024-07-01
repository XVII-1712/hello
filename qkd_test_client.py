# qkd_test_client.py
import socket
import ssl

# Secure Client Setup
context = ssl.create_default_context()
context.load_verify_locations('cert.pem')
context.check_hostname = False  # Disable hostname checking for testing

# Connect to Secure Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_client = context.wrap_socket(client, server_hostname='localhost', do_handshake_on_connect=True)
secure_client.connect(('127.0.0.1', 443))

# Receive Message
message = secure_client.recv(1024)
print(message.decode('utf-8'))
secure_client.close()
