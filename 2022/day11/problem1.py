import puzzleinput as pi
import monkeys


def problem_1():
    total_inspection = monkeys.run_simulation(pi.sample_monkies, 20, 3)

    print(f"Problem 1 : {total_inspection}")
