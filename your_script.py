import qutip as qt
import matplotlib.pyplot as plt

# Create a quantum state
psi = qt.basis(2, 0)

# Create a Hamiltonian
H = qt.sigmax()

# Evolve the state under the Hamiltonian
result = qt.mesolve(H, psi, tlist=[0, 1, 2, 3], e_ops=[qt.sigmax(), qt.sigmay(), qt.sigmaz()])

# Plot the results
times = result.times
expect_x = result.expect[0]
expect_y = result.expect[1]
expect_z = result.expect[2]

plt.figure()
plt.plot(times, expect_x, label="X")
plt.plot(times, expect_y, label="Y")
plt.plot(times, expect_z, label="Z")
plt.xlabel("Time")
plt.ylabel("Expectation values")
plt.legend()
plt.show()
