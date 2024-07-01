from qiskit import QuantumCircuit, transpile, assemble, Aer, IBMQ, execute
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import os

# Load IBM Q account
api_token = os.getenv("QISKIT_IBMQ_API_TOKEN")
if api_token is None:
    raise ValueError("IBM Q API token is not set as an environment variable.")
IBMQ.save_account(api_token, overwrite=True)
IBMQ.load_account()

# Get the backend
provider = IBMQ.get_provider('ibm-q')
backend = provider.get_backend('ibmq_qasm_simulator')

# Create a quantum circuit for QKD
qc = QuantumCircuit(2, 2)

# QKD protocol steps
qc.h(0)  # Apply Hadamard gate to qubit 0
qc.cx(0, 1)  # Apply CNOT gate
qc.measure([0, 1], [0, 1])  # Measure both qubits

# Transpile the circuit
qc = transpile(qc, backend)

# Assemble the circuit
qobj = assemble(qc)

# Execute the circuit
job = execute(qc, backend)
result = job.result()

# Get the counts (measurement results)
counts = result.get_counts()

# Plot the results
plot_histogram(counts)
plt.show()
