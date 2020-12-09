import copy
from dataclasses import dataclass


@dataclass
class Instruction:
    ins_type: str
    argument: int
    visited: bool

    def action(self, acc):
        if self.ins_type == 'acc':
            return acc + self.argument
        else:
            return acc

    def get_next(self, index):
        if self.ins_type == 'jmp':
            return index + self.argument
        else:
            return index + 1

    def switch(self):
        if self.ins_type == 'nop':
            self.ins_type = 'jmp'

        if self.ins_type == 'jmp':
            self.ins_type = 'nop'


def run(instructions):
    acc = 0
    ind = 0

    while True:
        ins = instructions[ind]
        if ins.visited:
            break

        ins.visited = True
        acc = ins.action(acc)

        ind = ins.get_next(ind)

        # termination req
        if ind == len(instructions):
            print('terminated normally')
            print(acc)
            return True

    return False


def main():
    with open('input', 'r') as f:
        instructions = [Instruction(l.split()[0], int(l.split()[1]), False) for l in f.readlines()]

    for i in range(len(instructions)):
        if instructions[i].ins_type != 'acc':
            instructions_changed = copy.deepcopy(instructions)
            instructions_changed[i].switch()
            if run(instructions_changed):
                break


if __name__ == '__main__':
    main()
