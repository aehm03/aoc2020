from typing import NamedTuple, Dict, List


def main():
    space = {}
    with open('input', 'r') as f:
        for x, line in enumerate(f.readlines()):
            for y, char in enumerate(line.strip()):
                space[Coord(x, y, 0, 0)] = 1 if char == '#' else 0

    print(run(space, 6, 3))
    print(run(space, 6, 4))


def run(space, steps, dims):
    for i in range(steps):
        new_space = {}
        for coord, value in space.items():
            neighbors = coord.get_neighbors(dims)
            count = count_cells(space, neighbors)

            if (value == 1 and 2 <= count <= 3) or (value == 0 and count == 3):
                new_space[coord] = 1
            else:
                new_space[coord] = 0

            for new_coord in neighbors:
                if new_coord not in space.keys() and new_coord not in new_space.keys():
                    new_neighbors = new_coord.get_neighbors(dims)

                    if count_cells(space, new_neighbors) == 3:
                        new_space[new_coord] = 1
                    else:
                        new_space[new_coord] = 0
        space = new_space

    return sum(space.values())


class Coord(NamedTuple):
    x: int
    y: int
    z: int
    w: int

    def get_neighbors(self, dims=3):
        if dims == 3:
            return self.get_neighbors3()
        if dims == 4:
            return self.get_neighbors4()

    def get_neighbors4(self):
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    for dw in [-1, 0, 1]:
                        if sum([abs(dx), abs(dy), abs(dz), abs(dw)]) > 0:
                            neighbors.append(Coord(self.x + dx, self.y + dy, self.z + dz, self.w + dw))
        return neighbors

    def get_neighbors3(self):
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    if sum([abs(dx), abs(dy), abs(dz)]) > 0:
                        neighbors.append(Coord(self.x + dx, self.y + dy, self.z + dz, 0))
        return neighbors


def count_cells(space: Dict[Coord, int], cells: List[Coord]):
    return sum(space[n] for n in cells if n in space.keys())


if __name__ == '__main__':
    main()
