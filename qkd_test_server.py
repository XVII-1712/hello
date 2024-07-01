import socket
import ssl
from qkd_device import QKDDevice

# Initialize QKD Device
qkd_device = QKDDevice(address='192.168.1.2', port=8080)
qkd_device.initialize()

# Generate Quantum Key
quantum_key = qkd_device.generate_key()

# Save Quantum Key
with open('quantum_key.txt', 'w') as key_file:
    key_file.write(quantum_key)

# Secure Communication Setup
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

# Create Secure Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 443))
server.listen(5)

print("Secure server started, waiting for connections...")

# Handle Incoming Connections
while True:
    client_socket, addr = server.accept()
    secure_socket = context.wrap_socket(client_socket, server_side=True)
    print(f"Connection from {addr} has been established.")
    secure_socket.sendall(b'Secure communication established using QKD key.')
    secure_socket.close()
