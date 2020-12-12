from math import radians, sin, cos


class Ship:
    x: float
    y: float
    w_x: float
    w_y: float
    rotation: float

    def __init__(self, x=0, y=0, rotation=90):
        self.x = x
        self.y = y
        self.rotation = rotation

    def get_position(self):
        return self.x, self.y

    def change_x(self, value):
        self.x += value

    def change_y(self, value):
        self.y += value

    def move(self, raw):
        action = raw[0]
        value = int(raw[1:])

        if action in ['N', 'E', 'S', 'W']:
            self.move_absolute(action, value)

        if action in ['R', 'L']:
            self.rotate(action, value)

        if action == 'F':
            self.move_forward(value)

    def move_absolute(self, direction, value):
        sign = 1 if direction in ['N', 'E'] else -1
        change = self.change_x if direction in ['E', 'W'] else self.change_y
        change(sign * value)

    def rotate(self, direction, value):
        sign = 1 if direction == 'R' else -1
        self.rotation += sign * value

    def move_forward(self, value):
        self.change_x(round(sin(radians(self.rotation)) * value))
        self.change_y(round(cos(radians(self.rotation)) * value))


class WPShip(Ship):
    w_x: float
    w_y: float

    def __init__(self, x=0, y=0, w_x=10, w_y=1, rotation=0):
        super().__init__(x, y, rotation)
        self.w_x = w_x
        self.w_y = w_y

    def change_x(self, value):
        self.w_x += value

    def change_y(self, value):
        self.w_y += value

    def get_waypoint(self):
        return self.w_x, self.w_y

    def move_forward(self, value):
        self.x += self.w_x * value
        self.y += self.w_y * value

    def rotate(self, direction, value):
        steps = value / 90
        for step in range(int(steps)):
            self.rotate_90(direction)

    def rotate_90(self, direction):
        self.w_x, self.w_y = self.w_y, self.w_x
        if direction == 'R':
            self.w_y = self.w_y * -1
        else:
            self.w_x = self.w_x * -1


def main():
    with open('input', 'r') as f:
        directions = [line.strip() for line in f.readlines()]

    ship = Ship()
    [ship.move(d) for d in directions]

    print(abs(ship.get_position()[0]) + abs(ship.get_position()[1]))


def main2():
    with open('input', 'r') as f:
        directions = [line.strip() for line in f.readlines()]

    ship = WPShip()

    [ship.move(d) for d in directions]
    print(abs(ship.get_position()[0]) + abs(ship.get_position()[1]))


def test_forward():
    ship = Ship()
    ship.move_forward(1)
    ship.rotate('R', 90)
    ship.move_forward(1)
    assert(almost_qual(ship.get_position()[0], 1, 3))
    assert(almost_qual(ship.get_position()[1], -1, 3))


def test_wp_rotation():
    with open('input_debug', 'r') as f:
        directions = [line.strip() for line in f.readlines()]

    ship = WPShip()
    [ship.move(d) for d in directions]
    assert(ship.get_position() == (0, 0))

    with open('input_mini', 'r') as f:
        directions = [line.strip() for line in f.readlines()]

    ship = WPShip()
    [ship.move(d) for d in directions]
    assert(ship.get_position() == (214, -72))


def almost_qual(a, b, digits):
    epsilon = 10 ** -digits
    return abs(a/b - 1) < epsilon


if __name__ == '__main__':
    test_forward()
    main()
    test_wp_rotation()
    main2()
