import math


def get_years():
    years = []
    with open('input', 'r') as f:
        for line in f:
            years.append(int(line))
    return years


def find_rec(current_sum, current_indices, searched_sum, n_parts, alist):

    if len(current_indices) == 0:
        start_index = 0
    else:
        start_index = current_indices[-1]

    for i in range(start_index + 1, len(alist)):

        if (current_sum + alist[i] == searched_sum) and (len(current_indices) + 1 == n_parts):
            current_indices.append(i)
            return current_indices

        if (current_sum + alist[i] <= searched_sum) and (len(current_indices) < n_parts):
            solution = find_rec(current_sum + alist[i], current_indices + [i], searched_sum, n_parts, alist)
            if solution:
                return solution


def main():
    years = get_years()
    solution1 = find_rec(0, [], 2020, 2, years)
    print(f'solution 1: {math.prod([years[i] for i in solution1])}')

    solution2 = find_rec(0, [], 2020, 3, years)
    print(f'solution 2: {math.prod([years[i] for i in solution2])}')


if __name__ == '__main__':
    main()
