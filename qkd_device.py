# qkd_device.py
import random
import string

class QKDDevice:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.initialized = False

    def initialize(self):
        # Simulate device initialization
        self.initialized = True
        print(f"QKD Device initialized at {self.address}:{self.port}")

    def generate_key(self):
        # Simulate quantum key generation
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        print("Quantum key generated.")
        return key
