import re
from functools import reduce
from typing import NamedTuple, Tuple


class Field(NamedTuple):
    name: str
    valid: Tuple[Tuple[int, int], Tuple[int, int]]

    def is_valid(self, value):
        return (self.valid[0][0] <= value <= self.valid[0][1]) or \
               (self.valid[1][0] <= value <= self.valid[1][1])


def parse_field(raw):
    name = raw[:raw.find(':')]
    res = re.findall(r'(\d+)', raw)
    return Field(name, ((int(res[0]), int(res[1])), (int(res[2]), int(res[3]))))


def main():
    with open('input', 'r') as f:
        data = (l.strip() for l in f.readlines() if l != '\n')

    fields = []
    other_tickets = []

    for line in data:
        if line == 'your ticket:':
            break
        parse_field(line)
        fields.append(parse_field(line))

    my_ticket = [int(i) for i in next(data).split(',')]

    next(data)
    for line in data:
        other_tickets.append([int(n) for n in line.split(',')])

    sum_invalid = 0
    valid_tickets = []

    for ticket in other_tickets:
        valid = True
        for value in ticket:
            if not max([field.is_valid(value) for field in fields]):
                sum_invalid += value
                valid = False
        if valid:
            valid_tickets.append(ticket)
    print(sum_invalid)

    # Create Candidates
    positions = len(valid_tickets[0])
    pos_fields = {}
    removed = []
    for position in range(positions):
        pos_fields[position] = [field for field in fields
                                if min([field.is_valid(ticket[position])
                                        for ticket in valid_tickets])]
        # Delete possibilties on the fly
        if len(pos_fields[position]) == 1:
            removed.append(pos_fields[position][0])
            fields.remove(pos_fields[position][0])
            for pos in range(position):
                pos_fields[pos].remove(pos_fields[position][0])

    # fiend positions with only one candidate and remove this field from all others
    while sum([len(fields) for fields in pos_fields.values()]) > len(pos_fields.values()):
        remove_me = [fields for fields in pos_fields.values() if len(fields) == 1 and fields[0] not in removed][0][0]
        [values.remove(remove_me) for values in pos_fields.values() if len(values) > 1 and remove_me in values]
        removed.append(remove_me)

    pos_fields_final = [field[0].name for field in pos_fields.values()]
    print(reduce(lambda x, y: x * y , [my_ticket[ind] for ind, field in enumerate(pos_fields_final) if field.startswith('departure')]))


if __name__ == '__main__':
    main()
