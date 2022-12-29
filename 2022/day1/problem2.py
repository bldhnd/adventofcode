import re
import puzzleinput as pi


def problem_2() -> None:
    elf_calories = re.split("\n\n", pi.calories)

    calorie_totals = []

    for elf_calorie in elf_calories:
        total = sum([int(calorie) for calorie in elf_calorie.split("\n")])

        calorie_totals.append(total)
    else:
        calorie_totals = sorted(calorie_totals, reverse=True)

    top_3_total = sum(calorie_totals[:3])

    print(f"problem 2 : {top_3_total}")
