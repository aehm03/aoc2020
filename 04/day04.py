import re


def main():
    with open('input', 'r') as f:
        passports_raw = f.read()

    passports = [{split_key_value(pp_entry)[0]: split_key_value(pp_entry)[1]
                 for pp_entry in passport.split()}
                 for passport in passports_raw.split('\n\n')]

    passports_with_fields = [p for p in passports if is_valid(p)]
    print(len(passports_with_fields))
    print(sum(is_valid2(p) for p in passports_with_fields))


def split_key_value(pp_entry):
    sep = pp_entry.find(':')
    return pp_entry[0:sep], pp_entry[sep+1:]


def is_valid(passport):
    return min(field in passport.keys() for field in ['eyr', 'hcl', 'hgt', 'byr', 'iyr', 'pid', 'ecl'])


def is_valid2(passport):
    return min(field_to_validation(key)(value) for key, value in passport.items())


def field_to_validation(key):
    mapping = {
        'eyr': lambda eyr: 2020 <= int(eyr) <= 2030 if eyr.isdigit() else False,
        'hcl': lambda hcl: bool(re.match(r'^#(\d|[a-f]){6}$', hcl)),
        'hgt': validate_height,
        'byr': lambda byr: 1920 <= int(byr) <= 2002 if byr.isdigit() else False,
        'iyr': lambda iyr: 2010 <= int(iyr) <= 2020 if iyr.isdigit() else False,
        'pid': lambda pid: (len(pid) == 9) and pid.isdigit(),
        'ecl': lambda ecl: ecl in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
        'cid': lambda cid: True
    }
    return mapping[key]


def validate_height(height_str):
    """
    hgt (Height) - a number followed by either cm or in:
    If cm, the number must be at least 150 and at most 193.
    If in, the number must be at least 59 and at most 76.
    """
    res = re.search(r'(\d+)(\w+)', height_str)

    if not res:
        return False

    digit = res.groups()[0]
    unit = res.groups()[1]

    if not digit.isdigit():
        return False
    digit = int(digit)

    if unit == 'in' and 59 <= digit <= 76:
        return True

    if unit == 'cm' and 150 <= digit <= 193:
        return True

    return False


if __name__ == '__main__':
    main()
