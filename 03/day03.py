from math import  prod

def main():
    landscape = []
    with open('input', 'r') as f:
        for line in f.readlines():
            landscape.append(line.rstrip('\n'))

    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    trees = [count_trees(landscape, slope) for slope in slopes]

    print(prod(trees))


def count_trees(landscape, slope, x=0, y=0) -> int:
    dx, dy = slope

    trees = 0
    while y < len(landscape):
        y_line = landscape[y]

        if y_line[x % len(y_line)] == '#':
            trees += 1
        y += dy
        x += dx
    return trees


if __name__ == '__main__':
    main()
