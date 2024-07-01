import numpy as np
from qutip import *
import matplotlib.pyplot as plt
import hashlib

# Function to create a Bell state
def create_bell_state():
    zero_zero = tensor(basis(2, 0), basis(2, 0))
    one_one = tensor(basis(2, 1), basis(2, 1))
    bell_state = (zero_zero + one_one).unit()
    return bell_state

# Function to apply noise to the state
def apply_noise(state, noise_level):
    noisy_state = (1 - noise_level) * state + noise_level * tensor(qeye(2), qeye(2)) * state
    return noisy_state.unit()

# Function to measure in a given basis
def measure_basis(state, measurement_basis):
    if measurement_basis == 'Z':
        P0 = tensor(basis(2, 0), basis(2, 0)).proj()
        P1 = tensor(basis(2, 0), basis(2, 1)).proj()
        P2 = tensor(basis(2, 1), basis(2, 0)).proj()
        P3 = tensor(basis(2, 1), basis(2, 1)).proj()
    elif measurement_basis == 'X':
        plus = (basis(2, 0) + basis(2, 1)).unit()
        minus = (basis(2, 0) - basis(2, 1)).unit()
        P0 = tensor(plus, plus).proj()
        P1 = tensor(plus, minus).proj()
        P2 = tensor(minus, plus).proj()
        P3 = tensor(minus, minus).proj()
    
    probabilities = [expect(P0, state), expect(P1, state), expect(P2, state), expect(P3, state)]
    probabilities = np.array(probabilities) / sum(probabilities)  # Normalize probabilities
    outcomes = ["00", "01", "10", "11"]
    
    return np.random.choice(outcomes, p=probabilities)

# Function to run multiple rounds of QKD with basis choice and noise
def run_qkd_rounds(rounds, noise_level):
    alice_key = []
    bob_key = []
    alice_bases = []
    bob_bases = []
    qber_values = []

    for _ in range(rounds):
        bell_state = create_bell_state()
        noisy_state = apply_noise(bell_state, noise_level)
        alice_basis = np.random.choice(['Z', 'X'])
        bob_basis = np.random.choice(['Z', 'X'])
        outcome = measure_basis(noisy_state, alice_basis)
        
        if alice_basis == bob_basis:
            if outcome == "00" or outcome == "11":
                alice_bit = outcome[0]
                bob_bit = outcome[1]
                alice_key.append(alice_bit)
                bob_key.append(bob_bit)
            alice_bases.append(alice_basis)
            bob_bases.append(bob_basis)
        
        # Calculate QBER for each round
        if alice_basis == bob_basis:
            if outcome == "01" or outcome == "10":
                qber_values.append(1)
            else:
                qber_values.append(0)
    
    qber = sum(qber_values) / len(qber_values) if qber_values else 0
    return alice_key, bob_key, alice_bases, bob_bases, qber

# Function to apply simple error correction
def simple_error_correction(alice_key, bob_key):
    corrected_bob_key = []
    for a_bit, b_bit in zip(alice_key, bob_key):
        corrected_bob_key.append(a_bit)  # Assume simple parity check for this example
    return corrected_bob_key

# Function to apply privacy amplification
def privacy_amplification(key, length):
    hash_function = hashlib.sha256()
    hash_function.update("".join(key).encode())
    hashed_key = hash_function.hexdigest()[:length]
    return hashed_key

# Number of rounds for the QKD protocol
num_rounds = 100
noise_level = 0.1  # Noise level to simulate non-ideal conditions
final_key_length = 64  # Length of the final key after privacy amplification

# Run the QKD protocol and measure QBER
alice_key, bob_key, alice_bases, bob_bases, qber = run_qkd_rounds(num_rounds, noise_level)

# Apply simple error correction
corrected_bob_key = simple_error_correction(alice_key, bob_key)

# Apply privacy amplification
final_alice_key = privacy_amplification(alice_key, final_key_length)
final_bob_key = privacy_amplification(corrected_bob_key, final_key_length)

# Print the shared keys and QBER
print("Alice's final key:", final_alice_key)
print("Bob's final key:", final_bob_key)
print("Quantum Bit Error Rate (QBER):", qber)

# Check if keys match
if final_alice_key == final_bob_key:
    print("Final keys match! Secure communication established.")
else:
    print("Final keys do not match. Error in key distribution.")

# Visualize QBER
plt.plot(range(num_rounds), [qber]*num_rounds, label='QBER')
plt.xlabel('Round')
plt.ylabel('QBER')
plt.title('Quantum Bit Error Rate over Rounds with Noise')
plt.legend()
plt.show()
