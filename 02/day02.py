import re
from dataclasses import dataclass


@dataclass
class PasswordValidation:
    min: int
    max: int
    character: chr
    password: str

    def validate(self) -> bool:
        n_char = self.password.count(self.character)
        return self.min <= n_char <= self.max

    def validate2(self) -> bool:
        return (self.password[self.min-1] == self.character) != (self.password[self.max-1] == self.character)


def main():
    with open('input', 'r') as f:
        validations = []
        for line in f:
            res = re.search(r'(\d+)-(\d+)\s(\w):\s(\w+)', line)
            validation = PasswordValidation(int(res.groups()[0]),
                                            int(res.groups()[1]),
                                            *res.groups()[2:])

            validations += [validation]
        print(sum([v.validate() for v in validations]))
        print(sum([v.validate2() for v in validations]))


if __name__ == '__main__':
    main()
