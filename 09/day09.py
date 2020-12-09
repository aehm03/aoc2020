def main():
    with open('input', 'r') as f:
        data = [int(l) for l in f.readlines()]

    first_invalid = find_first_invalid(data, 25)
    print(first_invalid)

    cont_summands = find_cont_summands(data, first_invalid)
    print(min(cont_summands) + max(cont_summands))


def test_small():
    with open('input_mini', 'r') as f:
        data = [int(l) for l in f.readlines()]

    first_invalid = find_first_invalid(data, 5)
    assert (first_invalid == 127)

    cont_summands = find_cont_summands(data, first_invalid)
    assert(cont_summands == [15, 25, 47, 40])

    assert(min(cont_summands) + max(cont_summands) == 62)


def find_cont_summands(codes, invalid):
    for ind, code in enumerate(codes):
        if code < invalid:
            res = [code]
            rest = iter(codes[ind+1:])
            while (nxt := next(rest)) + sum(res) <= invalid:
                res += [nxt]
                if sum(res) == invalid:
                    return res


def find_first_invalid(codes, offset):
    valid = (is_valid(codes[i], codes[i - offset:i]) for i in range(offset, len(codes)))
    first = next(ind for ind, x in enumerate(valid) if not x)
    return codes[first + offset]


def is_valid(code, previous):
    valid = [p for p in previous if (complement := code - p) in previous and complement != p]
    return len(valid) > 0


if __name__ == '__main__':
    test_small()
    main()
