import numpy as np
from qutip import *

# Function to create a Bell state
def create_bell_state():
    zero_zero = tensor(basis(2, 0), basis(2, 0))
    one_one = tensor(basis(2, 1), basis(2, 1))
    bell_state = (zero_zero + one_one).unit()
    return bell_state

# Function to measure in the standard basis
def measure_standard_basis(state):
    P0 = tensor(basis(2, 0), basis(2, 0)).proj()
    P1 = tensor(basis(2, 0), basis(2, 1)).proj()
    P2 = tensor(basis(2, 1), basis(2, 0)).proj()
    P3 = tensor(basis(2, 1), basis(2, 1)).proj()
    
    probabilities = [expect(P0, state), expect(P1, state), expect(P2, state), expect(P3, state)]
    outcomes = ["00", "01", "10", "11"]
    
    return np.random.choice(outcomes, p=probabilities)

# Function to run multiple rounds of QKD
def run_qkd_rounds(rounds):
    alice_key = []
    bob_key = []
    
    for _ in range(rounds):
        bell_state = create_bell_state()
        outcome = measure_standard_basis(bell_state)
        
        if outcome == "00" or outcome == "11":
            alice_bit = outcome[0]
            bob_bit = outcome[1]
            alice_key.append(alice_bit)
            bob_key.append(bob_bit)
    
    return alice_key, bob_key

# Number of rounds for the QKD protocol
num_rounds = 10

# Run the QKD protocol
alice_key, bob_key = run_qkd_rounds(num_rounds)

# Print the shared keys
print("Alice's key:", "".join(alice_key))
print("Bob's key:", "".join(bob_key))

# Check if keys match
if alice_key == bob_key:
    print("Keys match! Secure communication established.")
else:
    print("Keys do not match. Error in key distribution.")
