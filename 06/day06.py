import unittest


class Group:
    vocab: list[chr]
    answers: list[str]

    def __init__(self, raw):
        self.answers = raw.split()
        self.vocab = set(raw)

    def combined_yes(self, agg):
        return sum(1 for q in self.vocab if agg(q in answer for answer in self.answers))

    def combined_yes_any(self):
        return self.combined_yes(max)

    def combined_yes_every(self):
        return self.combined_yes(min)


class TestGroup(unittest.TestCase):
    def test_combined(self):
        data = [('abc', 3), ('a\nb\nc', 3), ('ab\nac', 3),
                ('a\na\na', 1), ('b', 1)]
        for pair in data:
            result = Group(pair[0]).combined_yes_any()
            self.assertEqual(result, pair[1])


def main():
    with open('input.txt', 'r') as f:
        data = f.read()

    groups_raw = data.split('\n\n')
    print(sum(Group(g).combined_yes_any() for g in groups_raw))
    print(sum(Group(g).combined_yes_every() for g in groups_raw))


if __name__ == '__main__':
    #unittest.main()
    main()
