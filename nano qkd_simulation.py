from qutip import basis, sigmax, sigmay, sigmaz, mesolve, expect
import matplotlib.pyplot as plt
import numpy as np

# Define initial state and Hamiltonian
psi0 = basis(2, 0)
H = 0.5 * sigmax()

# Time points
times = np.linspace(0.0, 10.0, 100)

# Solve the Schrödinger equation
result = mesolve(H, psi0, times, [], [sigmax(), sigmay(), sigmaz()])

# Extract expectation values
exp_x = np.array([expect(sigmax(), state) for state in result.states])
exp_y = np.array([expect(sigmay(), state) for state in result.states])
exp_z = np.array([expect(sigmaz(), state) for state in result.states])

# Plot results
plt.figure()
plt.plot(times, exp_x, label='X')
plt.plot(times, exp_y, label='Y')
plt.plot(times, exp_z, label='Z')
plt.xlabel('Time')
plt.ylabel('Expectation values')
plt.legend()
plt.savefig('qutip_simulation.png')

