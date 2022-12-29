from termcolor import colored


class Knot(object):
    def __init__(self, symbol: str, x_start: int = 1, y_start: int = 1) -> None:
        self.symbol: str = symbol
        self.x_pos: int = x_start
        self.y_pos: int = y_start
        self.where: list[tuple[int, int]] = []
        self.where_unique: dict = dict()

        self.update_where()

    def move_to(self, pos: tuple[int, int]) -> None:
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.update_where()

    def move_x_pos(self, pos: int) -> tuple[int, int]:
        self.x_pos += pos
        self.update_where()
        return self.position()

    def move_y_pos(self, pos: int) -> tuple[int, int]:
        self.y_pos += pos
        self.update_where()
        return self.position()

    def update_where(self) -> None:
        pos = (self.x_pos, self.y_pos)

        self.where.append(pos)

        entry: list = self.where_unique.get(self.x_pos) or []

        if self.y_pos not in entry:
            entry.append(self.y_pos)

        self.where_unique[self.x_pos] = entry

    def has_been_to(self, pos: tuple[int, int]) -> bool:
        x, y = pos

        entry: list = self.where_unique.get(x)

        if not entry:
            return False

        return y in entry

    def close_enough(self, other: tuple[int, int]) -> bool:
        other_x, other_y = other

        if abs(other_x - self.x_pos) >= 2 or abs(other_y - self.y_pos) >= 2:
            return False

        return True

    def position(self) -> tuple[int, int]:
        return (self.x_pos, self.y_pos)

    def __repr__(self) -> str:
        return repr(self.position())


class Rope(object):
    def __init__(self, trailing_knots_count: int) -> None:
        self.head = Knot(0)
        self.trailing_knots: list[Knot] = [
            Knot(str(index + 1)) for index in range(trailing_knots_count)]
        self.tail = self.trailing_knots[-1:][0]

    def move(self, direction: str, steps: int) -> None:
        for _ in range(steps):
            if direction == "left":
                prev_pos = self.head.move_x_pos(-1)
            elif direction == "right":
                prev_pos = self.head.move_x_pos(1)
            elif direction == "up":
                prev_pos = self.head.move_y_pos(1)
            elif direction == "down":
                prev_pos = self.head.move_y_pos(-1)

            for knot in self.trailing_knots:
                if not knot.close_enough(prev_pos):
                    last_x, last_y = prev_pos
                    x, y = knot.position()

                    if x != last_x and y != last_y:
                        x = x + 1 if x < last_x else x - 1
                        y = y + 1 if y < last_y else y - 1
                    elif last_x - x >= 2:
                        x = last_x - 1
                    elif x - last_x >= 2:
                        x = last_x + 1
                    elif last_y - y >= 2:
                        y = last_y - 1
                    elif y - last_y >= 2:
                        y = last_y + 1

                    knot.move_to((x, y))

                prev_pos = knot.position()


def execute_directions(directions: str, trailing_knots_count: int, tail_symbol: str = "") -> Rope:
    planck_rope = Rope(trailing_knots_count)

    if tail_symbol:
        planck_rope.tail.symbol = tail_symbol

    for direction_steps in directions.split("\n"):
        direction, steps = direction_steps.split(" ")
        steps = int(steps)

        if direction == "R":
            planck_rope.move("right", steps)
        elif direction == "U":
            planck_rope.move("up", steps)
        elif direction == "D":
            planck_rope.move("down", steps)
        elif direction == "L":
            planck_rope.move("left", steps)

    return planck_rope


def build_tail_map(rope: Rope) -> str:
    max_up = max([y for _, y in rope.head.where])
    min_down = min([y for _, y in rope.head.where])

    max_right = max([x for x, _ in rope.head.where])
    min_left = min([x for x, _ in rope.head.where])

    tail_map = ""

    for y in range(min_down - 1, max_up):
        axis = ""

        for x in range(min_left - 1, max_right):
            coord = (x + 1, y + 1)

            if coord == (1, 1):
                axis += colored("s", "green")
            elif rope.tail.has_been_to(coord):
                axis += colored("#", "cyan")
            else:
                axis += "."

        tail_map = axis + "\n" + tail_map

    return tail_map


def build_rope_map(rope: Rope) -> str:
    max_up = max([y for _, y in rope.head.where])
    min_down = min([y for _, y in rope.head.where])

    max_right = max([x for x, _ in rope.head.where])
    min_left = min([x for x, _ in rope.head.where])

    rope_map = ""

    for y in range(min_down - 1, max_up):
        axis = ""

        for x in range(min_left - 1, max_right):
            coord = (x + 1, y + 1)

            if rope.head.position() == coord:
                axis += colored("H", "yellow")
            else:
                tail_has_visited = False
                for knot in rope.trailing_knots:
                    if (tail_has_visited := knot.position() == coord):
                        axis += colored(knot.symbol, "cyan")
                        break

                if not tail_has_visited:
                    if coord == (1, 1):
                        axis += colored("s", "green")
                    else:
                        axis += "."

        rope_map = axis + "\n" + rope_map

    return rope_map
