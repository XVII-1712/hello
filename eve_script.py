import socket

# Eve's server to intercept data from Alice
eve_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
eve_host = '127.0.0.1'
eve_port = 65434  # Different port to avoid conflict

eve_server_socket.bind((eve_host, eve_port))
eve_server_socket.listen(1)
print("Eve's server is listening on port", eve_port)

# Accept connection from Alice
conn_from_alice, addr_from_alice = eve_server_socket.accept()
print("Eve connected by Alice", addr_from_alice)

# Eve's client to forward data to Bob
eve_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bob_host = '127.0.0.1'
bob_port = 65432

try:
    eve_client_socket.connect((bob_host, bob_port))
except ConnectionRefusedError:
    print("Bob's server is not running or not accessible.")
    conn_from_alice.close()
    eve_server_socket.close()
    exit()

# Intercept and forward data
data_from_alice = conn_from_alice.recv(4096)
print("Eve intercepted data:", data_from_alice.decode('utf-8'))

# Optionally, Eve can try to decode or modify the data here
# (for the sake of this simulation, we will just forward it)

eve_client_socket.sendall(data_from_alice)

# Close the connections
conn_from_alice.close()
eve_client_socket.close()
eve_server_socket.close()
