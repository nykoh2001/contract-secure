class CheckedBlock:
    def __init__(self, block, state=None, constraints=[]):
        self.block = block
        self.state = state
        self.constraints = constraints
