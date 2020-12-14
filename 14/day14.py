import copy
from math import sqrt, ceil


def main():
    mask_inst = []
    with open('input', 'r') as f:
        ind = 0
        for line in f.readlines():
            if line.startswith('mask'):
                mask_inst.append((line.strip()[7:43], []))
                ind = len(mask_inst) - 1

            if line.startswith('mem'):
                address = int(line[line.find('[') + 1:line.find(']')])
                value = int(line.strip()[line.find('=') + 2:])
                mask_inst[ind][1].append((address, value))

    memory = {}
    for mask, instructions in mask_inst:
        for address, value in instructions:
            memory[address] = to_decimal(apply_mask(mask, value))

    print(sum(memory.values()))

    # PART 2
    memory = {}
    for mask, instructions in mask_inst:
        for address, value in instructions:
            for final_address in expand_floating(decode_address(mask, address)):
                memory[final_address] = value

    print(sum(memory.values()))


def apply_mask(mask, value):
    binary = to_binary(value)
    return [b if m == 'X' else int(m) for b, m in zip(binary, mask)]


def to_binary(decimal, digits=36):
    return [(decimal // 2**b) % 2 for b in range(digits)][::-1]


def to_decimal(binary):
    return sum([2 ** pos for pos, b in enumerate(binary[::-1]) if b == 1])


def decode_address(mask, address):
    binary = to_binary(address)
    return [m if m == 'X' else int(m) if m == '1' else b for b, m in zip(binary, mask)]


def expand_floating(address):
    indices = [i for i, x in enumerate(address) if x == 'X']
    num_addresses = 2 ** len(indices)

    new_adresses = []

    for i in range(num_addresses):
        replacements = (to_binary(i, len(indices)))
        new_address = copy.deepcopy(address)

        for ind, rep in enumerate(replacements):
            new_address[indices[ind]] = rep
        new_adresses.append(to_decimal(new_address))

    return new_adresses


def test_apply_mask():
    tests = [('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 11, 73),
             ('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 101, 101),
             ('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 0, 64)]

    for mask, value, expected in tests:
        masked = apply_mask(mask, value)
        print(to_decimal(masked) == expected)


def test_decode_address():
    tests = [('000000000000000000000000000000X1001X', 42, '000000000000000000000000000000X1101X'),
             ('00000000000000000000000000000000X0XX', 26, '00000000000000000000000000000001X0XX')]

    for mask, address, expected in tests:
        masked = decode_address(mask, address)
        print(''.join(str(x) for x in masked) == expected)


def test_expand_floating():
    tests = [([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'X', 1, 1, 0, 1, 'X'],
             [26, 27, 58, 59]),
             ([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 'X', 0, 'X', 'X'],
             [16, 17, 18, 19, 24, 25, 26, 27])]

    for floating, expected in tests:
        print(expand_floating(floating) == expected)


if __name__ == '__main__':
    test_apply_mask()
    test_decode_address()
    test_expand_floating()
    main()
