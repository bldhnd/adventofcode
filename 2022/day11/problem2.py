import puzzleinput as pi
import monkeys


def problem_2():
    # never solved this
    total_inspections = monkeys.run_simulation(pi.sample_monkies, 20, 3)

    print(f"Problem 2 : {total_inspections}")
