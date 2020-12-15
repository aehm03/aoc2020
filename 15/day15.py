def main():
    print(get_nth([18, 11, 9, 0, 5, 1]))
    print(get_nth([18, 11, 9, 0, 5, 1], 30000000))


def next_number(numbers, last, round):
    if last not in numbers.keys():
        numbers[last] = (round, round)
        return numbers, 0, round + 1

    else:
        numbers[last] = (numbers[last][1], round)
        return numbers, numbers[last][1] - numbers[last][0], round + 1


def make_dict(numbers):
    return {n: (i + 1, i + 1) for i, n in enumerate(numbers)}


def tests_p1():
    tests = [([0, 3, 6], 436),
             ([1, 3, 2], 1),
             ([2, 1, 3], 10)]

    for numbers, expected in tests:
        print(get_nth(numbers) == expected)


def tests_p2():
    tests = [([0, 3, 6], 175594),
             ([1, 3, 2], 2578),
             ([2, 1, 3], 3544142)]

    for numbers, expected in tests:
        print(get_nth(numbers, max_rounds=30000000) == expected)


def get_nth(numbers, max_rounds=2020):
    round = len(numbers)
    last = numbers[-1]
    numbers = make_dict(numbers)

    while round < max_rounds:
        numbers, last, round = next_number(numbers, last, round)
    return last


if __name__ == '__main__':
    tests_p1()
    #tests_p2()
    main()
