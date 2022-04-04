import ctypes
import random

class XORShift:
    def __init__(self, seed=0):
        if seed == 0:
            seed = random.randint(1, 1 << 31)
        self.state = seed

    def next(self):
        self.state = ctypes.c_int32(self.state ^ self.state << 13).value
        self.state = ctypes.c_int32(self.state ^ self.state >> 17).value
        self.state = ctypes.c_int32(self.state ^ self.state << 5).value
        self.state = ctypes.c_int32(self.state).value

        if self.state < 0:
            self.state += 2147483647

        return self.state
