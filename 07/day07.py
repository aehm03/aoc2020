import re
from itertools import chain


def main():
    with open('input', 'r') as f:
        data = [line for line in f.readlines()]

    rules = {name: contains for name, contains in map(parse_bags, data)}

    shiny_gold_sum = 0
    for bag, contains in rules.items():

        contains = set([bags for n, bags in contains])

        while True:
            old = len(contains)
            new_rules = [rules[name] for name in contains if name in rules.keys()]
            new_contains = set([bags for n, bags in chain.from_iterable(new_rules)])
            contains.update(new_contains)
            if old == len(contains):
                break

        if 'shiny gold bag' in contains:
            shiny_gold_sum += 1

    print(shiny_gold_sum)
    print(count_rec('shiny gold bag', rules))


def count_rec(current_bag, rules):
    if len(rules[current_bag]) == 0:
        return 0
    else:
        return sum(count + (count * count_rec(bag, rules)) for count, bag in rules[current_bag])


def parse_bags(line: str):
    res = [r.strip(' \n.') for r in re.split(r'contain|,', line)]
    name = res[0][:-1]
    if 'no other' in line:
        return name, []

    contains = [(int(r[0]), ' '.join(r[1:]) if r[0] == '1' else ' '.join(r[1:])[:-1]) for r in map(lambda s: s.split(), res[1:])]
    return name, contains


if __name__ == '__main__':
    main()
