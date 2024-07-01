import numpy as np
from qutip import *

# Function to generate a random bit string
def generate_random_bits(n):
    return np.random.randint(2, size=n)

# Function to encode bits into qubits using the BB84 protocol
def encode_bits(bits, bases):
    qubits = []
    for bit, base in zip(bits, bases):
        if base == 0:  # Z-basis
            qubit = basis(2, bit)
        else:  # X-basis
            qubit = (basis(2, 0) + (-1)**bit * basis(2, 1)).unit()
        qubits.append(qubit)
    return qubits

# Function to measure qubits
def measure_qubits(qubits, bases):
    measurements = []
    for qubit, base in zip(qubits, bases):
        if base == 0:  # Z-basis
            result = np.abs((qubit.dag() * basis(2, 0)).full()[0, 0])**2
            measurement = 0 if result > 0.5 else 1
        else:  # X-basis
            result = np.abs((qubit.dag() * (basis(2, 0) + basis(2, 1)).unit()).full()[0, 0])**2
            measurement = 0 if result > 0.5 else 1
        measurements.append(measurement)
    return measurements

# Parameters
n_bits = 100  # Number of bits
eavesdropper_present = False

# Alice's random bits and bases
alice_bits = generate_random_bits(n_bits)
alice_bases = generate_random_bits(n_bits)

# Alice encodes her bits into qubits
alice_qubits = encode_bits(alice_bits, alice_bases)

# If eavesdropper is present, Eve measures qubits randomly
if eavesdropper_present:
    eve_bases = generate_random_bits(n_bits)
    eve_measurements = measure_qubits(alice_qubits, eve_bases)
    alice_qubits = encode_bits(eve_measurements, eve_bases)

# Bob's random bases
bob_bases = generate_random_bits(n_bits)

# Bob measures the qubits
bob_measurements = measure_qubits(alice_qubits, bob_bases)

# Alice and Bob compare bases
matching_bases = alice_bases == bob_bases
alice_key = alice_bits[matching_bases]
bob_key = bob_measurements[matching_bases]

# Display the results
print(f"Alice's key: {alice_key}")
print(f"Bob's key: {bob_key}")
print(f"Matching bits: {np.sum(alice_key == bob_key)} out of {len(alice_key)}")

if eavesdropper_present:
    print(f"Eve's measurements: {eve_measurements}")
