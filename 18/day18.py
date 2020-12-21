from __future__ import annotations  # scheduled for python 3.10

tests = [
    ('1 + 2 * 3 + 4 * 5 + 6', 71),
    ('2 * 3 + (4 * 5)', 26),
    ('5 + (8 * 3 + 9 + 3 * 4 * 3)', 437),
    ('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 12240),
    ('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 13632)
]


class Node:
    value: object
    left: Node
    right: Node

    def __init__(self, value, left, right):
        self.value = int(value) if value.isdigit() else value
        self.left = left
        self.right = right

    def set_children(self, left, right):
        self.left = left
        self.right = right

    def get_value(self):
        #print(self.value)

        if isinstance(self.value, int):
            return self.value

        if self.value == '+':
            return self.left.get_value() + self.right.get_value()

        if self.value == '*':
            return self.left.get_value() * self.right.get_value()


def test1():
    for task, solution in tests:
        input = (c for c in task.replace(' ', ''))
        node = parse(input)
        print(node.get_value() == solution)


def main():
    with open('input', 'r') as f:
        data = [(c for c in l.strip().replace(' ', '')) for l in f.readlines()]

    print(sum(parse(d).get_value() for d in data))


def parse(parsing_input):
    left = None
    right = None
    op = None

    while (c := next(parsing_input, None)) is not None:

        current_node = Node(c, None, None)

        if c == '(':
            current_node = parse(parsing_input)
        if c == ')':
            return left

        if left is None:
            left = current_node
            continue

        if op is None:
            op = current_node
            continue

        if right is None:
            right = current_node
            op.set_children(left, current_node)
            left = op
            right, op = None, None

    return left


if __name__ == '__main__':
    test1()
    main()
