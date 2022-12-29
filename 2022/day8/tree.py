from typing import Self
from termcolor import colored


class Tree(object):
    def __init__(self, height: int, index: int) -> None:
        self.height: int = height
        self.index: int = index
        self.up: Tree = None
        self.left: Tree = None
        self.down: Tree = None
        self.right: Tree = None

    def get_edge(self, direction: str) -> Self:
        current: Tree = self

        for direct in direction.split("+"):
            while not current.is_edge(direct):
                current = current.move(direct)

        return current

    def move(self, direction: str, step: int = 1) -> Self:
        current: Tree = self

        for direct in direction.split("+"):
            if direct == "down":
                for _ in range(step):
                    if current.is_edge(direct):
                        break
                    if current.down:
                        current = current.down
            elif direct == "right":
                for _ in range(step):
                    if current.is_edge(direct):
                        break
                    if current.right:
                        current = current.right
            elif direct == "left":
                for _ in range(step):
                    if current.is_edge(direct):
                        break
                    if current.left:
                        current = current.left
            elif direct == "up":
                for _ in range(step):
                    if current.is_edge(direct):
                        break
                    if current.up:
                        current = current.up

        return current

    def is_edge(self, direction: str) -> bool:
        result = False

        for direct in direction.split("+"):
            if direct == "left":
                result = not self.left
            elif direct == "up":
                result = not self.up
            elif direct == "right":
                result = not self.right
            elif direct == "down":
                result = not self.down

            if not result:
                return False

        return result

    def is_visible(self) -> bool:
        return self.is_visible_for_direction("left") \
            or self.is_visible_for_direction("up") \
            or self.is_visible_for_direction("right") \
            or self.is_visible_for_direction("down")

    def is_visible_for_direction(self, direction: str) -> bool:
        if self.is_edge(direction):
            return True

        current = self.move(direction)

        while not current.is_edge(direction):
            if self.height <= current.height:
                return False
            current = current.move(direction)

        return self.height > current.height

    def scenic_score(self) -> int:
        left = self.scenic_score_for_direction("left")
        up = self.scenic_score_for_direction("up")
        right = self.scenic_score_for_direction("right")
        down = self.scenic_score_for_direction("down")

        return left * up * right * down

    def scenic_score_for_direction(self, direction: str) -> int:
        count = 0
        current = self

        while not current.is_edge(direction):
            count += 1
            current = current.move(direction)

            if self.height <= current.height:
                break

        return count

    def __repr__(self) -> str:
        return str(self.height)


def print_trees(nav: Tree, bool_map: bool):

    def get_display(nav: Tree, bool_map: bool) -> str:
        if bool_map:
            return colored("1", "green") if nav.is_visible() else "0"
        else:
            return repr(nav)

    while True:
        display = get_display(nav, bool_map)

        print(display, end="")

        if nav.is_edge("right+down"):
            break

        last = nav
        nav = nav.move("right")

        if last == nav:
            nav = nav.move("down").get_edge("left")
            print()

    print("\n")


def print_scenic_trees(nav: Tree, index: int) -> None:
    while True:
        display = colored("X", "green") if nav.index == index else "0"

        print(display, end="")

        if nav.is_edge("right+down"):
            break

        last = nav
        nav = nav.move("right")

        if last == nav:
            nav = nav.move("down").get_edge("left")
            print()

    print("\n")


def build_trees(tree_height_map: str) -> Tree:
    last: Tree = None
    last_row: Tree = None
    index = 0

    for row in tree_height_map.split("\n"):
        for height in row:
            current = Tree(int(height), index)

            if last:
                last.right = current
                current.left = last

            if last_row:
                current.up = last_row
                last_row.down = current
                last_row = last_row.move("right")

            last = current
            index += 1

        last_row = last.get_edge("left")
        last = None

    return last_row.get_edge("left+up")
