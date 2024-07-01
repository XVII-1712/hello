import numpy as np
from qutip import *

# Function to create a Bell state
def create_bell_state():
    zero_zero = tensor(basis(2, 0), basis(2, 0))
    one_one = tensor(basis(2, 1), basis(2, 1))
    bell_state = (zero_zero + one_one).unit()
    return bell_state

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

# Function to run multiple rounds of QKD with basis choice
def run_qkd_rounds(rounds):
    alice_key = []
    bob_key = []
    alice_bases = []
    bob_bases = []

    for _ in range(rounds):
        bell_state = create_bell_state()
        alice_basis = np.random.choice(['Z', 'X'])
        bob_basis = np.random.choice(['Z', 'X'])
        outcome = measure_basis(bell_state, alice_basis)
        
        if alice_basis == bob_basis:
            if outcome == "00" or outcome == "11":
                alice_bit = outcome[0]
                bob_bit = outcome[1]
                alice_key.append(alice_bit)
                bob_key.append(bob_bit)
            alice_bases.append(alice_basis)
            bob_bases.append(bob_basis)
    
    return alice_key, bob_key, alice_bases, bob_bases

# Function to apply simple error correction
def simple_error_correction(alice_key, bob_key):
    corrected_bob_key = []
    for a_bit, b_bit in zip(alice_key, bob_key):
        corrected_bob_key.append(a_bit)  # Assume simple parity check for this example
    return corrected_bob_key

# Number of rounds for the QKD protocol
num_rounds = 100

# Run the QKD protocol
alice_key, bob_key, alice_bases, bob_bases = run_qkd_rounds(num_rounds)

# Apply simple error correction
corrected_bob_key = simple_error_correction(alice_key, bob_key)

# Print the shared keys
print("Alice's key:", "".join(alice_key))
print("Bob's key after error correction:", "".join(corrected_bob_key))

# Check if keys match
if alice_key == corrected_bob_key:
    print("Keys match! Secure communication established.")
else:
    print("Keys do not match. Error in key distribution.")