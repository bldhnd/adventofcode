from typing import Self
import re


class Monkey(object):
    def __init__(self, id: int, items: list[int], worry_op: str, test: int, monkey_true: int, monkey_false: int) -> None:
        self._id = id
        self._items = items
        self._worry_op = worry_op
        self._test = test
        self._monkey_true = monkey_true
        self._monkey_false = monkey_false
        self.inspections = 0

    def inspect_and_throw(self, worry_level_per_item: int, other_monkeys: list[Self]) -> None:
        throw_tos: dict[int: list] = dict()

        self.inspections += len(self._items)

        for item in self._items:
            worry_level = self._get_worry_level(item)

            worry_level //= worry_level_per_item

            if worry_level % self._test == 0:
                throw_to_monkey_id = self._monkey_true
            else:
                throw_to_monkey_id = self._monkey_false

            if throw_to_monkey_id not in throw_tos:
                throw_tos[throw_to_monkey_id] = []

            to_monkey_items = throw_tos.get(throw_to_monkey_id)

            to_monkey_items.append(worry_level)

        for to_monkey_id in throw_tos:
            to_monkey = other_monkeys[to_monkey_id]
            items = throw_tos.get(to_monkey_id)

            self.throw(items, to_monkey)

    def throw(self, items: list[int], to: Self) -> None:
        for item in items:
            to.catch(item)

        self._items.clear()

    def catch(self, item: int) -> None:
        self._items.append(item)

    def _get_worry_level(self, item: int) -> int:
        worry_op_match = re.match("(old|\d+) ([+*]) (old|\d+)", self._worry_op)

        loperand = worry_op_match.groups(0)[0]
        operator = worry_op_match.groups(0)[1]
        roperand = worry_op_match.groups(0)[2]

        if loperand == "old":
            loperand = item
        else:
            loperand = int(loperand)

        if roperand == "old":
            roperand = item
        else:
            roperand = int(roperand)

        if operator == "+":
            return loperand + roperand
        elif operator == "*":
            return loperand * roperand

        raise ValueError(f"Unrecognized worry operator {operator}")

    def __repr__(self) -> str:
        # return f"Monkey {self._id} inspected items {self.inspections} times."
        return f"Monkey {self._id} inspected items {self.inspections} times. ({self._items})"


class MonkeySim(object):
    def __init__(self, monkies: list[Monkey]) -> None:
        self._monkies = monkies

    def play(self, rounds: int, worry_level_per_item: int) -> int:
        current_worry_level = worry_level_per_item

        for round in range(rounds):
            for monkey in self._monkies:
                monkey.inspect_and_throw(current_worry_level, self._monkies)

            if (round + 1) % 20 == 0:
                current_worry_level *= 3

            if round == 0 or round == 19 or (round + 1) % 100 == 0:
                print(f"After round {round + 1}")
                print("\n".join([repr(monkey)
                                 for monkey in self._monkies]), end="\n\n")

        ordered_inspections = sorted(
            self._monkies, key=lambda monkey: monkey.inspections, reverse=True)

        highest = ordered_inspections[0].inspections
        second_highest = ordered_inspections[1].inspections

        return highest * second_highest


def run_simulation(monkies_info: str, rounds: int, worry_level: int) -> int:
    sim = build_simulation(monkies_info)

    return sim.play(rounds, worry_level)


def build_simulation(monkies_info: str) -> MonkeySim:
    monkies: list[Monkey] = []

    for monkey_info in re.split("\n\n", monkies_info):
        info = monkey_info.split("\n")

        monkey_id = info[0].split(" ")[1][:-1]
        starting_items = [int(item) for item in re.findall("\d+", info[1])]
        worry_algo = info[2].split("=")[1]
        test = re.findall("\d+", info[3])[0]
        moneky_true = re.findall("\d+", info[4])[0]
        monkey_false = re.findall("\d+", info[5])[0]

        monkey = Monkey(int(monkey_id), starting_items, worry_algo.strip(),
                        int(test), int(moneky_true), int(monkey_false))
        monkies.append(monkey)

    return MonkeySim(monkies)
