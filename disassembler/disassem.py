from typing import Optional, Iterable

import pyevmasm


class EVMDisassemble:
    class EVMInst(pyevmasm.Instruction):
        def __init__(self, opcode: int, name: str, operand_size: int, pops: int, pushes: int, fee: int, description: str, operand: Optional[int] = None, pc: Optional[int] = 0, offset: Optional[int] = 0):
            super().__init__(opcode, name, operand_size,
                             pops, pushes, fee, description, operand, pc)
            self._offset = offset

    @staticmethod
    def convert_to_evm_inst(offset, inst):
        return EVMDisassemble.EVMInst(inst._opcode, inst._name, inst._operand_size,
                                      inst._pops, inst._pushes, inst._fee, inst._description, inst._operand, inst._pc, offset)

    @staticmethod
    def convert_to_evm_insts(insts):
        for offset, inst in enumerate(insts):
            yield EVMDisassemble.convert_to_evm_inst(offset, inst)

    @staticmethod
    def disassem_evm(bytecode: Iterable, pc: int = 0, fork=pyevmasm.DEFAULT_FORK):
        instructions = pyevmasm.disassemble_all(bytecode, pc, fork)
        return EVMDisassemble.convert_to_evm_insts(instructions)
