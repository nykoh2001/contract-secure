from instructions.check_concrete_val import is_symbolic


class Register:
    def __init__(self, registers={}):
        self.registers = registers

    def set(self, index, value):
        self.registers[index] = value

    def get(self, index):
        if is_symbolic(self.registers[index]):
            return self.registers[index]
        else:
            return int.from_bytes(self.registers[index])
