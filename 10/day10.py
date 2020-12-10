from collections import Counter


def main():
    with open('input', 'r') as f:
        data = sorted(int(line) for line in f.readlines())

    data = [0] + data + [max(data) + 3]
    differences = Counter([j-i for i, j in zip(data[:-1], data[1:])])
    print(differences[1] * differences[3])

    # how many ways are there to reach each adapter?
    ways = {x: len([y for y in data if x - 3 <= y < x]) for x in data}

    # sum up the ways to get to each adapter
    for adapter in ways.keys():
        ways[adapter] = max(1, sum(ways[o] for o in ways.keys() if adapter > o >= adapter-3))
    print(ways[adapter])


if __name__ == '__main__':
    main()
