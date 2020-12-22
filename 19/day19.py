from __future__ import annotations  # scheduled for python 3.10
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple


class Rule(ABC):

    @abstractmethod
    def eval(self, word: str) -> bool:
        pass

    @staticmethod
    def parse_rule(raw: str, all_rules: Dict[int, Rule]) -> Rule:
        raw = raw.strip().replace('"', '')

        if raw in ['a', 'b']:
            return LiteralRule(raw)

        if '|' in raw:
            left, right = raw.split('|')[0], raw.split('|')[1]
            return OrRule([Rule.parse_rule(left, all_rules), Rule.parse_rule(right, all_rules)])

        if raw.isdigit():
            return LookupRule(int(raw), all_rules)

        raws = raw.split()
        return ConcatRule((Rule.parse_rule(raws[0], all_rules), Rule.parse_rule(' '.join(raws[1:]), all_rules)))


class LiteralRule(Rule):
    literal: str

    def __init__(self, literal: str):
        self.literal = literal

    def __repr__(self):
        return f'literal: {self.literal}'

    def eval(self, word: str) -> bool:
        return word == self.literal


class ConcatRule(Rule):
    rules: Tuple[Rule, Rule]
    seen_words: Dict[str, bool]

    def __init__(self, rules: Tuple[Rule, Rule]):
        self.rules = rules
        self.seen_words = {}

    def __repr__(self):
        return f'concat: {self.rules}'

    def eval(self, word):

        if word in self.seen_words.keys():
            return self.seen_words[word]

        for i in range(len(word) + 1):
            first, second = word[0:i], word[i:]

            if self.rules[0].eval(first) and self.rules[1].eval(second):
                self.seen_words[word] = True
                return True

        self.seen_words[word] = False
        return False


class OrRule(Rule):
    rules: List[Rule]
    seen_words: Dict[str, bool]

    def __init__(self, rules):
        self.rules = rules
        self.seen_words = {}

    def __repr__(self):
        return f'or: {self.rules}'

    def eval(self, word: str) -> bool:

        if word in self.seen_words.keys():
            return self.seen_words[word]

        valid = self.rules[0].eval(word) or self.rules[1].eval(word)
        self.seen_words[word] = valid
        return valid


class LookupRule(Rule):
    all_rules: Dict[int, Rule]
    index: int

    def __init__(self, index, all_rules):
        self.index = index
        self.all_rules = all_rules

    def __repr__(self):
        return f'{self.index}'

    def eval(self, word: str) -> bool:
        return self.all_rules[self.index].eval(word)


def main():
    with open('input', 'r') as f:
        data = (l.strip() for l in f.readlines())

    rules = {}
    for line in data:
        if line == '':
            break

        number, raw = int(line.split(':')[0]), line.split(':')[1]
        rules[number] = Rule.parse_rule(raw, rules)

    rules[8] = Rule.parse_rule('42 | 42 8', rules)
    rules[11] = Rule.parse_rule('42 31 | 42 11 31', rules)

    print(sum(1 if rules[0].eval(line.strip()) else 0 for line in data))


def concat_test():
    b = LiteralRule('b')
    a = LiteralRule('a')
    conc = ConcatRule((a, b))
    print(conc.eval('ab'))
    print(not conc.eval('ba'))

    conc2 = ConcatRule((conc, conc))
    print(conc2.eval('abab'))


def or_test():
    b = LiteralRule('b')
    a = LiteralRule('a')
    orr = OrRule([a, b])
    print(orr.eval('a'))
    print(orr.eval('b'))


def concat_or_test():
    b = LiteralRule('b')
    a = LiteralRule('a')
    conc1 = ConcatRule((a, b))
    conc2 = ConcatRule((b, a))
    orr = OrRule([conc1, conc2])
    print(orr.eval('ab'))
    print(orr.eval('ba'))


if __name__ == '__main__':
    concat_test()
    or_test()
    concat_or_test()
    main()
