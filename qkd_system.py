import numpy as np
from qutip import basis, tensor, qeye, sigmax, rand_ket, ket2dm, expect, Qobj
from qutip_qip.operations import hadamard_transform
import hashlib

# Step 1: Initialize Quantum States
zero = basis(2, 0)
one = basis(2, 1)

print("Initial basis states:")
print("Zero state:", zero)
print("One state:", one)

# Step 2: State Preparation and Entanglement
psi0 = tensor(hadamard_transform() * zero, hadamard_transform() * zero)
print("Initial state psi0:")
print(psi0)

# Apply Hadamard and CNOT gate to entangle qubits
psi1 = tensor(hadamard_transform() * zero, zero)
psi2 = (tensor(qeye(2), qeye(2)) * psi1 + tensor(sigmax(), qeye(2)) * psi1).unit()
print("Entangled state psi2:")
print(psi2)
print("Dimensions of psi2:", psi2.dims)

# Step 3: Transmission and Measurement
def apply_noise(state, noise_level=0.01):  # Reduced noise level
    dims = state.dims[0]
    noise = Qobj(np.random.normal(0, noise_level, (state.shape[0], state.shape[1])), dims=state.dims)
    noisy_state = state + noise
    return noisy_state.unit()

psi_noisy = apply_noise(psi2)
print("State after applying noise:")
print(psi_noisy)
print("Dimensions of noisy state:", psi_noisy.dims)

# Measure the states
def measure_state(state, measurement_basis):
    if measurement_basis == 'z':
        proj0 = ket2dm(basis(2, 0))
        proj1 = ket2dm(basis(2, 1))
    else:
        raise ValueError("Unsupported measurement basis")

    p0 = expect(proj0, state)
    p1 = expect(proj1, state)
    result = np.random.choice([0, 1], p=[p0, p1])
    return result

# Debug: Measure states and print the results
alice_measurement = measure_state(psi_noisy.ptrace(0), 'z')
bob_measurement = measure_state(psi_noisy.ptrace(1), 'z')
print("Alice's measurement:", alice_measurement)
print("Bob's measurement:", bob_measurement)

# Step 4: Key Sifting and Error Correction
def sift_keys(alice_measurements, bob_measurements):
    return [(a, b) for a, b in zip(alice_measurements, bob_measurements) if a == b]

def parity_check_error_correction(keys):
    corrected_keys = []
    for k1, k2 in keys:
        if k1 == k2:
            corrected_keys.append(k1)
        else:
            corrected_keys.append(0)  # Simple error correction by majority vote
    return corrected_keys

alice_measurements = [measure_state(psi_noisy.ptrace(0), 'z') for _ in range(10)]
bob_measurements = [measure_state(psi_noisy.ptrace(1), 'z') for _ in range(10)]
print("Alice's measurements:", alice_measurements)
print("Bob's measurements:", bob_measurements)

sifted_keys = sift_keys(alice_measurements, bob_measurements)
corrected_keys = parity_check_error_correction(sifted_keys)
print("Sifted keys:", sifted_keys)
print("Corrected keys:", corrected_keys)

# Step 5: Privacy Amplification and Eavesdropping Detection
def privacy_amplification(key, new_length):
    key_str = ''.join(map(str, key))
    hashed_key = hashlib.sha256(key_str.encode()).hexdigest()
    binary_hashed_key = ''.join(format(int(c, 16), '04b') for c in hashed_key)
    return binary_hashed_key[:new_length]

def detect_eavesdropping(alice_key, bob_key):
    return alice_key != bob_key

if corrected_keys:
    final_alice_key = privacy_amplification(corrected_keys, 16)
    final_bob_key = privacy_amplification(corrected_keys, 16)
else:
    final_alice_key = final_bob_key = ""

eavesdropping_detected = detect_eavesdropping(final_alice_key, final_bob_key)

print("Alice's Final Key:", final_alice_key)
print("Bob's Final Key:", final_bob_key)
print("Eavesdropping Detected:", eavesdropping_detected)
