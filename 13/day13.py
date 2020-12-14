from itertools import count


def main():
    with open('input_mini', 'r') as f:
        data = [l.strip() for l in f.readlines()]

    departure = int(data[0])
    buses = [int(b) for b in data[1].split(',') if b.isdigit()]
    waiting_time = ([(b, b - (departure % b)) for b in buses])
    waiting_time.sort(key=lambda x: x[1])
    print(waiting_time[0][0] * waiting_time[0][1])


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
