import math
from itertools import count


def main():
    with open('input_mini', 'r') as f:
        data = [l.strip() for l in f.readlines()]

    departure = int(data[0])
    busses = [int(b) for b in data[1].split(',') if b.isdigit()]
    waiting_time = ([(b, b - (departure % b)) for b in busses])
    waiting_time.sort(key=lambda x: x[1])
    print(waiting_time[0][0] * waiting_time[0][1])


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1

    if b == 1:
        return 1

    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0

    if x1 < 0:
        x1 += b0

    return x1


def chinese_remainder(mod_remain):
    product = math.prod([m for m, r in mod_remain])
    sum = 0
    for mod, remain in mod_remain:
        p = product // mod
        sum += remain * mul_inv(p, mod) * p
    return sum % product


def main2():
    with open('input', 'r') as f:
        data = [l.strip() for l in f.readlines()]

    bus_offset = [(int(m), i) for i, m in enumerate(data[1].split(',')) if m.isdigit()]

    n = bus_offset[0][0]
    step = 1
    for b, offset in bus_offset:
        n = next(c for c in count(n, step) if (c + offset) % b == 0)
        step *= b

    print(n)


if __name__ == '__main__':
    main()
    main2()
