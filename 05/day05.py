def main():
    with open('05/input.txt', 'r') as f:
        data = [line for line in f]

    seats = [partition(range(128), seats[0:7], 'F', 'B') * 8 +
             partition(range(8), seats[7:], 'L', 'R') for seats in data]
    print(max(seats))

    my_seat = [seat for seat in range(max(seats)) if (seat - 1 in seats)
               and (seat + 1 in seats)
               and seat not in seats]
    print(my_seat)


def partition(space, actions, lower, upper):
    for action in actions:
        if action == lower:
            space = space[0:int(len(space)/2)]
        elif action == upper:
            space = space[int(len(space)/2):]
    return space[0]


if __name__ == '__main__':
    main()
