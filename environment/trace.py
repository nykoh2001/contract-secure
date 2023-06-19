from environment.state import State


class Trace:
    def __init__(self, block=None, state=State(), environment=None, contraints=None, block_checked=[]):
        self.blocks_checked = block_checked
        self.state = state
        self.environment = environment
        self.current_constraint = None
        self.constraints = contraints
        self.block = block

    def add_checked_block(self, block):
        self.blocks_checked.append(block)
        self.block = None
