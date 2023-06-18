from z3 import Extract
from instructions.check_concrete_val import ceil32, is_concrete, is_symbolic


class Memory:
    def __init__(self, memory=None, size=0):
        self.memory = memory
        self.size = size
        if memory == None:
            self.memory = {}

    def extend(self, start_index, size):
        if size > 0:
            new_size = ceil32(start_index + size)
            self.size = new_size

    def store(self, start_index, value, size=0):
        if size > 0:
            if is_concrete(value):
                value = value & ((2 ** (size * 8)) - 1)
                value_bytes = value.to_bytes(size)
            else:
                bv_size = value.size()
                assert (bv_size // 8) >= size

                value_bytes = []
                end = bv_size - (size * 8) - 1
                for i in range(bv_size - 1, end, -8):
                    value_bytes.append(Extract(i, i - 7, value))
            if is_symbolic(start_index):
                for i in range(size):
                    self.memory[start_index + size].append(value_bytes[i])
