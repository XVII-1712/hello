import qutip as qt
import matplotlib.pyplot as plt

# Create a two-qubit system
psi = qt.tensor(qt.basis(2, 0), qt.basis(2, 1))

# Define a Hamiltonian for the two-qubit system
H = qt.tensor(qt.sigmax(), qt.sigmax()) + qt.tensor(qt.sigmaz(), qt.sigmaz())

# Time evolution
tlist = [0, 1, 2, 3, 4, 5]
result = qt.mesolve(H, psi, tlist=tlist, e_ops=[qt.tensor(qt.sigmax(), qt.sigmax()), qt.tensor(qt.sigmaz(), qt.sigmaz())])

# Plot the results
expect_xx = result.expect[0]
expect_zz = result.expect[1]

plt.figure()
plt.plot(tlist, expect_xx, label="XX")
plt.plot(tlist, expect_zz, label="ZZ")
plt.xlabel("Time")
plt.ylabel("Expectation values")
plt.legend()
plt.show()
