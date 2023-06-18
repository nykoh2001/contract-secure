from z3 import Solver, ULT, sat
from z3.z3util import get_vars

from environment.trace import Trace
from instructions.check_concrete_val import get_argument_value, CEILING_256_VALUE, is_concrete, is_all_concrete


def check_add_overflow(instruction, block, constraints):
    args = instruction.arguments
    registers = block.state.registers
    a, b = get_argument_value(
        args, 0, registers), get_argument_value(args, 1, registers)
    c = (a + b) % CEILING_256_VALUE
    if is_concrete(c):
        if c < a or c < b:
            print("Vulnerability found: Add Integer Overflow")
            return
    else:
        s = Solver()
        s.add(constraints)
        s.add(ULT(c, a))
        if s.check() == sat:
            print("Vulnerability found: Add Integer Overflow")
            return

    print("No Add Integer Overflow Vul.")
