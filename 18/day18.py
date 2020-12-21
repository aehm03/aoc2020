from __future__ import annotations  # scheduled for python 3.10

tests = [
    ('1 + 2 * 3 + 4 * 5 + 6', 71),
    ('2 * 3 + (4 * 5)', 26),
    ('5 + (8 * 3 + 9 + 3 * 4 * 3)', 437),
    ('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 12240),
    ('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 13632)
]

tests2 = [
    ('1 + 2 * 3 + 4 * 5 + 6', 231),
    ('1 + (2 * 3) + (4 * (5 + 6))', 51),
    ('2 * 3 + (4 * 5)', 46),
    ('5 + (8 * 3 + 9 + 3 * 4 * 3)', 1445),
    ('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 669060),
    ('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 23340)
]


class Node:
    value: object
    left: Node
    right: Node

    def __init__(self, value, left=None, right=None):
        self.value = int(value) if isinstance(value, str) and value.isdigit() else value
        self.left = left
        self.right = right

    def set_children(self, left, right):
        self.left = left
        self.right = right

    def get_value(self):
        if isinstance(self.value, int):
            return self.value

        if self.value == '+':
            return self.left.get_value() + self.right.get_value()

        if self.value == '*':
            return self.left.get_value() * self.right.get_value()

    def get_optype(self):
        return self.value if self.value in ['+', '*'] else None


def test1():
    for task, solution in tests:
        input = (c for c in task.replace(' ', ''))
        node = parse(input)
        print(node.get_value() == solution)


def test2():
    for task, solution in tests2:
        input = (c for c in task.replace(' ', ''))
        node = parse(input, plus_prec=True)
        print(f'{node.get_value() == solution}')


def main():
    with open('input', 'r') as f:
        data = [(c for c in l.strip().replace(' ', '')) for l in f.readlines()]

    print(sum(parse(d, plus_prec=True).get_value() for d in data))


def parse(parsing_input, plus_prec=False):
    left = None
    op = None

    while (c := next(parsing_input, None)) is not None:

        current_node = Node(c)

        if c == '(':
            current_node = Node(parse(parsing_input, plus_prec).get_value())
        if c == ')':
            return left

        if left is None:
            left = current_node
            continue

        elif op is None:
            op = current_node
            continue

        else:
            if plus_prec and left.get_optype() == "*" and op.get_optype() == '+':
                op.set_children(left.right, current_node)
                left.set_children(left.left, op)
            else:
                op.set_children(left, current_node)
                left = op
            op = None

    return left


if __name__ == '__main__':
    test1()
    test2()
    main()
