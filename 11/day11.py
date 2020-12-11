import copy
from itertools import chain


def main():
    with open('input', 'r') as f:
        seats = [[c for c in l.strip()] for l in f.readlines()]

    changed = True
    while changed:
        seats, changed = apply_rules(seats)

    occupied = len([s for s in chain.from_iterable(seats) if s == '#'])
    print(occupied)


def main2():
    with open('input', 'r') as f:
        seats = [[c for c in l.strip()] for l in f.readlines()]

    changed = True
    while changed:
        seats, changed = apply_rules(seats, transforms2)

    occupied = len([s for s in chain.from_iterable(seats) if s == '#'])
    print(occupied)


def test_count():
    with open('round_1', 'r') as f:
        seats = [[c for c in l.strip()] for l in f.readlines()]

    assert (count_adjacent(0, 0, seats) == 2)
    assert (count_adjacent(1, 2, seats) == 5)
    assert (count_adjacent(0, 9, seats) == 3)


def test_transform():
    with open('round_1', 'r') as f:
        seats = [[c for c in l.strip()] for l in f.readlines()]

    assert (transforms[seats[0][9]](0, 9, seats) == '#')


def test_count_directions():
    seats = [['.', 'L', '.', 'L', '.', '#', '.', '#', '.', '#', '.', '#', '.']]
    assert (count_directions(0, 6, seats) == 2)
    assert (count_directions(0, 1, seats) == 0)
    assert (count_directions(0, 3, seats) == 1)


def count_adjacent(current_y, current_x, seats):
    count = 0
    for y in range(max(0, current_y - 1), min(current_y + 2, len(seats))):
        for x in range(max(0, current_x - 1), min(current_x + 2, len(seats[current_y]))):
            if (x != current_x) or (y != current_y):
                count = count + 1 if seats[y][x] == '#' else count
    return count


def count_directions(current_y, current_x, seats):
    count = 0

    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:

            # skip self
            if dy == 0 and dx == 0:
                continue

            y, x = current_y + dy, current_x + dx
            while 0 <= y < len(seats) and 0 <= x < len(seats[y]):
                if seats[y][x] != '.':
                    count = count + 1 if seats[y][x] == '#' else count
                    break
                y, x = y + dy, x + dx
    return count


def transform_empty(y, x, seats, count=count_adjacent):
    adjacent = count(y, x, seats)
    return '#' if adjacent == 0 else 'L'


def transform_occupied(y, x, seats, count=count_adjacent, thresh=4):
    adjacent = count(y, x, seats)
    return 'L' if adjacent >= thresh else '#'


transforms = {'.': lambda _, __, ___: '.',
              'L': transform_empty,
              '#': transform_occupied
              }

transforms2 = {'.': lambda _, __, ___: '.',
               'L': lambda  y, x, seats: transform_empty(y, x, seats, count_directions),
               '#': lambda y, x, seats: transform_occupied(y, x, seats, count_directions, 5)
               }


def apply_rules(seats, transforms=None):
    if transforms is None:
        transforms = transforms
    changed = False
    new_seats = copy.deepcopy(seats)
    for y, _ in enumerate(seats):
        for x, _ in enumerate(seats[y]):
            new_seat = transforms[seats[y][x]](y, x, seats)
            new_seats[y][x] = new_seat
            if new_seat != seats[y][x]:
                changed = True

    return new_seats, changed


if __name__ == '__main__':
    test_count()
    test_transform()
    test_count_directions()
    main()
    main2()
