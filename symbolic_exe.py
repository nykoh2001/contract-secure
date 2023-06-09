from rattle.analyze import SSABasicBlock
from instructions import instructions_functions
from environment.trace import Trace
from environment.checked_block import CheckedBlock
from copy import copy


class Symbolic(object):
    def __init__(self, recover):
        self.recover = recover
        self.env = self.recover.internal.filedata

        self.initial_trace = Trace(environment=self.env)
        self.initial_block = recover.functions[0].blocks[0]
        self.initial_trace.block = self.initial_block
        self.traces = []

    def run(self):
        traces = [self.initial_trace]
        while True:
            analyzed_traces = self.tracing(traces)
            print("analyzed trace:", analyzed_traces)
            self.traces.extend(traces)
            if not analyzed_traces:
                break
            traces = analyzed_traces
        return self.traces

    def execute_instuction(self, inst, state):
        print("insn:", inst.insn)
        if inst.insn.is_push:
            func = instructions_functions["PUSH"]
        else:
            func = instructions_functions[str(inst.insn)]
        return func(inst, state)

    def execute_block(self, block, state):
        blocks = []
        for inst in block.insns:
            executes_block = self.execute_instuction(inst, state)
            blocks.append(executes_block)
        return blocks

    def tracing(self, traces):
        analyzed_traces = []
        traces = [t for t in traces if t.block != None]
        print("traces:", traces)
        for t in traces:
            print("t.block:", t.block)
            if t.block == None:
                continue
            current_block = t.block
            executed_block = self.execute_block(
                current_block, t.state)
            executed_block = [e for e in executed_block if e != None]

            print("executes block:", executed_block)
            t.add_checked_block(CheckedBlock(current_block))
            for b in executed_block[1:]:
                if b == None:
                    continue
                new_trace = copy(t)
                new_trace.block = b[0]
                try:
                    b[1]
                    pass
                except:
                    continue
                new_trace.current_contraint = b[1]
                analyzed_traces.append(new_trace)
            t.block = executed_block[0][0]
            # t.current_constraint = executed_block[0][1]
        return analyzed_traces
