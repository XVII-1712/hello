import numpy as np
from qutip import *
import matplotlib.pyplot as plt
import hashlib
from pyldpc import make_ldpc, encode, decode, get_message

# Function to create a Bell state
def create_bell_state():
    zero_zero = tensor(basis(2, 0), basis(2, 0))
    one_one = tensor(basis(2, 1), basis(2, 1))
    bell_state = (zero_zero + one_one).unit()
    return bell_state

# Function to apply depolarizing noise to the state
def apply_depolarizing_noise(state, noise_level):
    depolarizing_channel = (1 - noise_level) * state.proj() + (noise_level / 4) * tensor(qeye(2), qeye(2))
    return depolarizing_channel.unit()

# Function to simulate eavesdropping
def eavesdrop(state, eavesdropping_level):
    if np.random.rand() < eavesdropping_level:
        eve_basis = np.random.choice(['Z', 'X'])
        outcome = measure_basis(state, eve_basis)
        if eve_basis == 'Z':
            if outcome == "00" or outcome == "11":
                return tensor(basis(2, 0), basis(2, 0)) if outcome == "00" else tensor(basis(2, 1), basis(2, 1))
            else:
                return tensor(basis(2, 0), basis(2, 1)) if outcome == "01" else tensor(basis(2, 1), basis(2, 0))
        else:
            plus = (basis(2, 0) + basis(2, 1)).unit()
            minus = (basis(2, 0) - basis(2, 1)).unit()
            return tensor(plus, plus) if outcome == "00" else tensor(plus, minus) if outcome == "01" else tensor(minus, plus) if outcome == "10" else tensor(minus, minus)
    else:
        return state

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

# Function to run multiple rounds of QKD with dynamic noise and eavesdropping
def run_qkd_rounds(rounds, noise_levels, eavesdropping_levels):
    alice_key = []
    bob_key = []
    alice_bases = []
    bob_bases = []
    qber_values = []

    for i in range(rounds):
        noise_level = noise_levels[i % len(noise_levels)]
        eavesdropping_level = eavesdropping_levels[i % len(eavesdropping_levels)]
        bell_state = create_bell_state()
        noisy_state = apply_depolarizing_noise(bell_state, noise_level)
        intercepted_state = eavesdrop(noisy_state, eavesdropping_level)
        alice_basis = np.random.choice(['Z', 'X'])
        bob_basis = np.random.choice(['Z', 'X'])
        outcome = measure_basis(intercepted_state, alice_basis)
        
        if alice_basis == bob_basis:
            if outcome == "00" or outcome == "11":
                alice_bit = outcome[0]
                bob_bit = outcome[1]
                alice_key.append(alice_bit)
                bob_key.append(bob_bit)
            alice_bases.append(alice_basis)
            bob_bases.append(bob_basis)
        
        if alice_basis == bob_basis:
            if outcome == "01" or outcome == "10":
                qber_values.append(1)
            else:
                qber_values.append(0)
    
    qber = sum(qber_values) / len(qber_values) if qber_values else 0
    return alice_key, bob_key, alice_bases, bob_bases, qber

# Function to find a valid n for LDPC
def find_valid_n(starting_length, d_c):
    while starting_length % d_c != 0:
        starting_length += 1
    return starting_length

# Function to apply LDPC error correction
def ldpc_error_correction(alice_key, bob_key):
    # Convert keys to binary arrays
    alice_key_bin = np.array([int(bit) for bit in alice_key], dtype=np.uint8)
    bob_key_bin = np.array([int(bit) for bit in bob_key], dtype=np.uint8)
    
    # Ensure the key length matches the LDPC code parameters
    key_length = len(alice_key_bin)
    d_v, d_c = 2, 4  # Adjusted parameters
    n = find_valid_n(key_length, d_c)  # Ensure d_c divides n
    
    # Adjust key lengths to match n
    alice_key_bin = np.pad(alice_key_bin, (0, n - key_length), 'constant', constant_values=0)
    bob_key_bin = np.pad(bob_key_bin, (0, n - key_length), 'constant', constant_values=0)
    
    # Create LDPC code
    H, G = make_ldpc(n, d_v, d_c, systematic=True, sparse=True)
    
    # Encode Alice's key
    encoded_alice_key = encode(G, alice_key_bin, snr=10)
    
    # Introduce errors to simulate transmission errors
    received_bob_key = decode(H, encoded_alice_key, snr=10)
    
    # Extract the message
    corrected_bob_key = get_message(G, received_bob_key)
    
    # Convert back to string keys
    corrected_bob_key_str = ''.join(map(str, corrected_bob_key[:key_length]))  # Truncate to original length
    
    return corrected_bob_key_str

# Function to apply privacy amplification
def privacy_amplification(key, length):
    hash_function = hashlib.sha256()
    hash_function.update("".join(key).encode())
    hashed_key = hash_function.hexdigest()[:length]
    return hashed_key

# Number of rounds for the QKD protocol
num_rounds = 100
noise_levels = [0.1, 0.2, 0.3]  # Dynamic noise levels
eavesdropping_levels = [0.1, 0.2, 0.3]  # Dynamic eavesdropping levels
final_key_length = 64  # Length of the final key after privacy amplification

# Run the QKD protocol and measure QBER
alice_key, bob_key, alice_bases, bob_bases, qber = run_qkd_rounds(num_rounds, noise_levels, eavesdropping_levels)

# Apply LDPC error correction
corrected_bob_key = ldpc_error_correction(alice_key, bob_key)

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
plt.title('Quantum Bit Error Rate over Rounds with Dynamic Conditions and LDPC')
plt.legend()
plt.show()
