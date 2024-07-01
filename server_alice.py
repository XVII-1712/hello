import socket
import numpy as np
from qutip import basis, tensor, qeye, sigmax, ket2dm, expect, Qobj
from qutip_qip.operations import hadamard_transform
import pyldpc

def apply_noise(state, noise_level=0.1):
    dims = state.dims[0]
    noise = Qobj(np.random.normal(0, noise_level, (state.shape[0], state.shape[1])), dims=state.dims)
    noisy_state = state + noise
    return noisy_state.unit()

def measure_state(state, measurement_basis):
    if measurement_basis == 'z':
        proj0 = ket2dm(basis(2, 0))
        proj1 = ket2dm(basis(2, 1))
    elif measurement_basis == 'x':
        proj0 = ket2dm((basis(2, 0) + basis(2, 1)).unit())
        proj1 = ket2dm((basis(2, 0) - basis(2, 1)).unit())
    else:
        raise ValueError("Unsupported measurement basis")

    p0 = expect(proj0, state)
    p1 = expect(proj1, state)
    result = np.random.choice([0, 1], p=[p0, p1])
    return result

def ldpc_encode(key):
    n = len(key)
    d_v = 3  # Number of 1s per column (variable nodes)
    d_c = 6  # Number of 1s per row (check nodes)

    # Ensure n is divisible by d_c
    while n % d_c != 0:
        n += 1
        key.append(0)  # Append 0s to the key to match the new length

    # Generate LDPC matrices
    H, G = pyldpc.make_ldpc(n, d_v, d_c)

    # Adjust the key length to match the dimensions of G
    key = np.array(key)
    if len(key) < G.shape[1]:
        key = np.append(key, [0] * (G.shape[1] - len(key)))
    elif len(key) > G.shape[1]:
        key = key[:G.shape[1]]
    
    # Ensure key values are binary (0 or 1)
    key = np.mod(key, 2)

    encoded_key = pyldpc.encode(G, key, snr=10)
    encoded_key = np.round(encoded_key).astype(int)  # Ensure values are integers
    return encoded_key, H

# Server setup
host = '127.0.0.1'
port = 65432
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)
print("Server is listening on port", port)

conn, addr = server_socket.accept()
print("Connected by", addr)

# Initialize Quantum States and Entangle
zero = basis(2, 0)
one = basis(2, 1)
psi0 = tensor(hadamard_transform() * zero, hadamard_transform() * zero)
psi1 = tensor(hadamard_transform() * zero, zero)
psi2 = (tensor(qeye(2), qeye(2)) * psi1 + tensor(sigmax(), qeye(2)) * psi1).unit()

# Apply noise
psi_noisy = apply_noise(psi2)

# Measure and send results
bob_measurement_bases = ['z' if np.random.random() < 0.5 else 'x' for _ in range(10)]
alice_measurement_results = [measure_state(psi_noisy.ptrace(0), basis) for basis in bob_measurement_bases]

# Encode key using LDPC
encoded_key, H = ldpc_encode(alice_measurement_results)
encoded_key_str = ','.join(map(str, encoded_key))

# Send data to client
conn.sendall(bytes(encoded_key_str, 'utf-8'))
conn.sendall(bytes(','.join(bob_measurement_bases), 'utf-8'))
conn.sendall(bytes(','.join(map(str, H.flatten())), 'utf-8'))  # Send LDPC parity-check matrix H

conn.close()
print("Measurements sent to client.")
