from typing import Self
from pprint import pprint
import puzzleinput as pi


class HeightStep(object):
    def __init__(self, position: tuple, counter: int) -> None:
        self.position = position
        self.counter = counter

    def change(self, x: int, y: int) -> None:
        self.position = (x, y)

    def get_x(self) -> int:
        return self.position[0]

    def get_y(self) -> int:
        return self.position[1]

    def surrounding(self) -> list[Self]:
        up = (self.get_x(), self.get_y() - 1)
        down = (self.get_x(), self.get_y() + 1)
        left = (self.get_x() - 1, self.get_y())
        right = (self.get_x() + 1, self.get_y())

        counter = self.counter + 1

        return [HeightStep(left, counter), HeightStep(up, counter), HeightStep(right, counter), HeightStep(down, counter)]

    def __eq__(self, __o: object) -> bool:
        if type(__o) is tuple:
            return self.position == __o
        return self.position == __o.position

    def __repr__(self) -> str:
        x = self.get_x()
        y = self.get_y()
        counter = self.counter

        return f"({x}, {y}, {counter})"


def problem_1():
    height_map = pi.heightmap

    height = height_map.count("\n") + 1
    width = height_map.find("\n") + 1

    start = find_height("S", height_map)
    goal = find_height("E", height_map)

    done = False
    main = [goal]

    while not done:
        changes = []

        for coord in main:
            to_check = coord.surrounding()

            for check_coord in to_check:
                if check_coord in main or check_coord in changes:
                    continue

                if check_coord.get_y() < 0 or check_coord.get_y() == height:
                    continue

                if check_coord.get_x() < 0 or check_coord.get_x() >= width - 1:
                    continue

                check_index = check_coord.get_x() + check_coord.get_y() * width
                coord_index = coord.get_x() + coord.get_y() * width

                check_step = height_map[check_index]
                coord_step = height_map[coord_index]

                if check_coord == start:
                    changes.append(check_coord)
                    done = True
                    break
                elif (coord_step == "E" and check_step == "z") or abs(ord(check_step) - ord(coord_step)) <= 1:
                    changes.append(check_coord)

            if done:
                break

        main += changes

    last = main[-1:][0]
    print(f"Problem 1 : {last.counter}")

    # print_map_results(main, width - 1, height)
    # pprint(main)


def print_map_results(steps: list[HeightStep], width: int, height: int):
    last = steps[-1:][0]
    path = [last]

    for step in reversed(steps[:-1]):
        if step.counter == last.counter:
            continue

        if abs(step.get_x() - last.get_x()) <= 1 and abs(step.get_y() - last.get_y()) <= 1:
            path.append(step)
            last = step

    pprint(path)

    for y in range(height):
        for x in range(width):
            candidate = (x, y)

            if candidate in path:
                print("#", end="")
            else:
                print(".", end="")

        print()


def find_height(height_to_find: str, height_map: str) -> HeightStep:
    target = HeightStep((0, 0), 0)
    row_length = height_map.find("\n") + 1

    for pos, height in enumerate(height_map):
        if height == height_to_find:
            x = pos - row_length * target.get_y()
            y = target.get_y()

            target.change(x, y)
            return target
        elif height == "\n":
            x = 0
            y = target.get_y() + 1

            target.change(x, y)

    raise ValueError(f"Could not find {height_to_find}")
