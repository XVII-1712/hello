import socket
import ssl

# Secure Client Setup
context = ssl.create_default_context()
context.load_verify_locations('cert.pem')

# Connect to Secure Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_client = context.wrap_socket(client, server_hostname='localhost')
secure_client.connect(('127.0.0.1', 443))

# Send Transaction Data
transaction_data = "amount=1000&currency=USD&recipient=account123"
secure_client.sendall(transaction_data.encode('utf-8'))

# Receive Confirmation
confirmation = secure_client.recv(1024)
print(confirmation.decode('utf-8'))
secure_client.close()
