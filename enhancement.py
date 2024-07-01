import socket
import numpy as np
from qutip import basis, tensor, qeye, sigmax, ket2dm, expect, Qobj
from qutip_qip.operations import hadamard_transform
import hashlib
import pyldpc

def apply_noise(state, noise_level=0.1):  # More realistic noise level
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

def ldpc_decode(encoded_key, H):
    # Ensure encoded_key length matches H shape
    encoded_key = np.array(encoded_key)
    if len(encoded_key) < H.shape[1]:
        encoded_key = np.append(encoded_key, [0] * (H.shape[1] - len(encoded_key)))
    elif len(encoded_key) > H.shape[1]:
        encoded_key = encoded_key[:H.shape[1]]
    
    decoded_key = pyldpc.decode(H, encoded_key, snr=10, maxiter=100)  # Increase maxiter for better convergence
    return decoded_key

def sift_keys(alice_measurements, bob_measurements, bob_bases):
    return [a for a, b, base in zip(alice_measurements, bob_measurements, bob_bases) if a == b]

def privacy_amplification(key, new_length):
    key_str = ''.join(map(str, key))
    hashed_key = hashlib.sha256(key_str.encode()).hexdigest()
    binary_hashed_key = ''.join(format(int(c, 16), '04b') for c in hashed_key)
    return binary_hashed_key[:new_length]

def detect_eavesdropping(alice_key, bob_key):
    return alice_key != bob_key

# Client setup
host = '127.0.0.1'
port = 65432
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

encoded_key_data = client_socket.recv(1024).decode('utf-8')
encoded_key = list(map(int, encoded_key_data.split(','))) if encoded_key_data else []

bob_bases_data = client_socket.recv(1024).decode('utf-8')
bob_bases = bob_bases_data.split(',') if bob_bases_data else []

H_data = client_socket.recv(1024).decode('utf-8')
H_flat = list(map(int, H_data.split(','))) if H_data else []
H = np.array(H_flat).reshape((-1, len(encoded_key))) if H_data else np.array([])

if not encoded_key or not bob_bases or H.size == 0:
    print("Error: Received incomplete data from server.")
else:
    # Initialize Quantum States and Entangle
    zero = basis(2, 0)
    one = basis(2, 1)
    psi0 = tensor(hadamard_transform() * zero, hadamard_transform() * zero)
    psi1 = tensor(hadamard_transform() * zero, zero)
    psi2 = (tensor(qeye(2), qeye(2)) * psi1 + tensor(sigmax(), qeye(2)) * psi1).unit()

    # Apply noise
    psi_noisy = apply_noise(psi2)

    # Measure and compare results
    bob_measurements = [measure_state(psi_noisy.ptrace(1), basis) for basis in bob_bases]
    sifted_keys = sift_keys(encoded_key, bob_measurements, bob_bases)

    # Print shapes for debugging
    print("Shape of sifted_keys:", len(sifted_keys))
    print("Shape of H:", H.shape)

    # Pad sifted_keys to match the dimensions of H
    while len(sifted_keys) < H.shape[1]:
        sifted_keys.append(0)

    # Decode the key using LDPC
    corrected_keys = ldpc_decode(sifted_keys, H)

    if corrected_keys is not None:
        final_alice_key = privacy_amplification(corrected_keys, 16)
        final_bob_key = privacy_amplification(corrected_keys, 16)
    else:
        final_alice_key = final_bob_key = ""

    eavesdropping_detected = detect_eavesdropping(final_alice_key, final_bob_key)

    print("Alice's measurements:", encoded_key)
    print("Bob's measurements:", bob_measurements)
    print("Sifted keys:", sifted_keys)
    print("Corrected keys:", corrected_keys)
    print("Alice's Final Key:", final_alice_key)
    print("Bob's Final Key:", final_bob_key)
    print("Eavesdropping Detected:", eavesdropping_detected)
