import socket
import hmac
import hashlib
import pyldpc
import numpy as np
from qutip import basis, tensor, qeye, sigmax, ket2dm, expect
from qutip_qip.operations import hadamard_transform

shared_secret_key = b'supersecretkey'

def generate_hmac(message, key):
    return hmac.new(key, message, hashlib.sha256).hexdigest()

def ldpc_encode(key):
    n = len(key)
    d_v = 3
    d_c = 6
    H, G = pyldpc.make_ldpc(n, d_v, d_c, systematic=True, sparse=True)
    encoded_key = pyldpc.encode(G, np.array(key), snr=10)
    return encoded_key, H

host = '127.0.0.1'
port = 65432
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)
print("Server is listening on port", port)

conn, addr = server_socket.accept()
print("Connected by", addr)

# Prepare quantum states (simplified example)
alice_basis = 'z'
alice_measurement = [1 if np.random.random() > 0.5 else 0 for _ in range(24)]

# Encode the key
encoded_key, H = ldpc_encode(alice_measurement)

# Prepare data to send
encoded_key_data = ','.join(map(str, encoded_key))
bob_bases_data = ','.join(['z' if np.random.random() > 0.5 else 'x' for _ in range(len(encoded_key))])
H_data = ','.join(map(str, H.flatten()))
decoy_flags = [0 if np.random.random() > 0.1 else 1 for _ in range(len(encoded_key))]

message = f"{encoded_key_data}|{bob_bases_data}|{H_data}|{decoy_flags}"
hmac_digest = generate_hmac(message.encode(), shared_secret_key)
message_with_hmac = f"{message}|{hmac_digest}"

conn.sendall(message_with_hmac.encode('utf-8'))
conn.close()
