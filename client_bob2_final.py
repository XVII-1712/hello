import socket
import numpy as np
import pyldpc
import hmac
import hashlib
from qutip import basis, tensor, qeye, sigmax, ket2dm, expect
from qutip_qip.operations import hadamard_transform

shared_secret_key = b'supersecretkey'

def generate_hmac(message, key):
    return hmac.new(key, message, hashlib.sha256).hexdigest()

def verify_hmac(message, received_hmac, key):
    computed_hmac = hmac.new(key, message, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed_hmac, received_hmac)

def apply_noise(state, noise_level=0.1):
    dims = state.dims[0]
    noise = tensor([qeye(2)] * len(dims)).data
    noisy_state = state + noise_level * noise
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
    encoded_key = np.array(encoded_key)
    if len(encoded_key) < H.shape[1]:
        encoded_key = np.append(encoded_key, [0] * (H.shape[1] - len(encoded_key)))
    elif len(encoded_key) > H.shape[1]:
        encoded_key = encoded_key[:H.shape[1]]
    decoded_key = pyldpc.decode(H, encoded_key, snr=10, maxiter=5000)
    return decoded_key

def sift_keys(alice_measurements, bob_measurements, bob_bases, decoy_flags):
    print("Alice's measurements:", alice_measurements)
    print("Bob's measurements:", bob_measurements)
    print("Bob's bases:", bob_bases)
    print("Decoy flags:", decoy_flags)
    
    sifted_keys = [a for a, b, base, decoy in zip(alice_measurements, bob_measurements, bob_bases, decoy_flags) if a == b and decoy == 0]
    
    print("Sifted keys:", sifted_keys)
    return sifted_keys

def privacy_amplification(key, new_length):
    key_str = ''.join(map(str, key))
    hashed_key = hashlib.sha256(key_str.encode()).hexdigest()
    binary_hashed_key = ''.join(format(int(c, 16), '04b') for c in hashed_key)
    return binary_hashed_key[:new_length]

def detect_eavesdropping(alice_key, bob_key):
    return alice_key != bob_key

host = '127.0.0.1'
port = 65432
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

received_data = client_socket.recv(4096).decode('utf-8').split('|')
encoded_key_data = received_data[0]
bob_bases_data = received_data[1]
H_data = received_data[2]
decoy_flags_data = received_data[3]
received_hmac = received_data[4]

# Verify HMAC
message = f"{encoded_key_data}|{bob_bases_data}|{H_data}|{decoy_flags_data}"
if not verify_hmac(message.encode(), received_hmac, shared_secret_key):
    print("Error: HMAC verification failed. The message may have been tampered with.")
    client_socket.close()
else:
    encoded_key = list(map(int, encoded_key_data.split(','))) if encoded_key_data else []
    bob_bases = bob_bases_data.split(',') if bob_bases_data else []
    H_flat = list(map(int, H_data.split(','))) if H_data else []
    H = np.array(H_flat).reshape((len(encoded_key), -1)) if H_data else np.array([])
    decoy_flags = list(map(int, decoy_flags_data.split(','))) if decoy_flags_data else []

    if not encoded_key or not bob_bases or H.size == 0 or not decoy_flags:
        print("Error: Received incomplete data from server.")
    else:
        zero = basis(2, 0)
        one = basis(2, 1)
        psi0 = tensor(hadamard_transform() * zero, hadamard_transform() * zero)
        psi1 = tensor(hadamard_transform() * zero, zero)
        psi2 = (psi0 + psi1).unit()
        psi_noisy = apply_noise(psi2)

        # Measure the quantum states based on Bob's bases
        bob_measurements = [measure_state(psi_noisy, base) for base in bob_bases]

        # Sift keys
        sifted_keys = sift_keys(encoded_key, bob_measurements, bob_bases, decoy_flags)

        # LDPC decoding
        corrected_keys = ldpc_decode(sifted_keys, H)

        # Privacy amplification (if needed)
        final_key_length = min(len(sifted_keys), 128)
        alice_final_key = privacy_amplification(sifted_keys, final_key_length)
        bob_final_key = privacy_amplification(corrected_keys, final_key_length)

        # Eavesdropping detection
        eavesdropping_detected = detect_eavesdropping(alice_final_key, bob_final_key)

        print("Alice's Final Key:", alice_final_key)
        print("Bob's Final Key:", bob_final_key)
        print("Eavesdropping Detected:", eavesdropping_detected)
        
client_socket.close()
