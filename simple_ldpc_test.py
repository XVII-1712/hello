import numpy as np
from pyldpc import make_ldpc, encode, decode, get_message

# Simplified example parameters
d_v, d_c = 3, 6
key_length = 50
n = key_length + d_c - (key_length % d_c)  # Ensure n is divisible by d_c

# Generate random key
alice_key_bin = np.random.randint(0, 2, key_length)
bob_key_bin = alice_key_bin.copy()

# Pad keys to match n
alice_key_bin = np.pad(alice_key_bin, (0, n - key_length), 'constant', constant_values=0)
bob_key_bin = np.pad(bob_key_bin, (0, n - key_length), 'constant', constant_values=0)

# Create LDPC code
H, G = make_ldpc(n, d_v, d_c, systematic=True, sparse=True)

# Encode Alice's key
encoded_alice_key = encode(G, alice_key_bin, snr=10)

# Simulate transmission errors by introducing noise
noisy_bob_key = encoded_alice_key + np.random.normal(0, 0.5, size=encoded_alice_key.shape)

# Decode Bob's received key
decoded_bob_key = decode(H, noisy_bob_key, snr=10)

# Extract the message
corrected_bob_key = get_message(G, decoded_bob_key)

# Debugging prints
print(f"Original Alice key: {alice_key_bin[:key_length]}")
print(f"Encoded Alice key: {encoded_alice_key}")
print(f"Noisy Bob key: {noisy_bob_key}")
print(f"Decoded Bob key: {decoded_bob_key}")
print(f"Corrected Bob key: {corrected_bob_key[:key_length]}")

# Check if keys match
if np.array_equal(alice_key_bin[:key_length], corrected_bob_key[:key_length]):
    print("Keys match! LDPC error correction successful.")
else:
    print("Keys do not match. Error in LDPC error correction.")
