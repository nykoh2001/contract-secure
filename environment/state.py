from environment.memory import Memory
from environment.register import Register


class State:
    def __init__(self, registers=Register(), memory=Memory(), contract=None):
        self.registers = registers
        self.memory = memory
        self.index = 0
        self.environment = contract
