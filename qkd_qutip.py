import numpy as np
from qutip import *

# Function to create a Bell state
def create_bell_state():
    # Create basis states |00> and |11>
    zero_zero = tensor(basis(2, 0), basis(2, 0))
    one_one = tensor(basis(2, 1), basis(2, 1))
    
    # Create the Bell state |Ψ+> = (|00> + |11>) / sqrt(2)
    bell_state = (zero_zero + one_one).unit()
    return bell_state

# Function to measure in the standard basis
def measure_standard_basis(state):
    P0 = tensor(basis(2, 0), basis(2, 0)).proj()  # Projector for |00>
    P1 = tensor(basis(2, 0), basis(2, 1)).proj()  # Projector for |01>
    P2 = tensor(basis(2, 1), basis(2, 0)).proj()  # Projector for |10>
    P3 = tensor(basis(2, 1), basis(2, 1)).proj()  # Projector for |11>
    
    probabilities = [expect(P0, state), expect(P1, state), expect(P2, state), expect(P3, state)]
    outcomes = ["00", "01", "10", "11"]
    
    return np.random.choice(outcomes, p=probabilities)

# Create the Bell state
bell_state = create_bell_state()

# Print the Bell state
print("Bell state |Ψ+> =")
print(bell_state)

# Measure the Bell state in the standard basis
outcome = measure_standard_basis(bell_state)

# Print the measurement outcome
print("Measurement outcome:", outcome)
