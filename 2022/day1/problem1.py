import re
import puzzleinput as pi


def problem_1() -> None:
    elf_calories = re.split("\n\n", pi.calories)

    elf_num = 0
    current_elf_num = 0
    largest_calorie_count = 0

    for elf_calories in elf_calories:
        current = sum([int(calorie)
                      for calorie in elf_calories.split("\n")])

        if current > largest_calorie_count:
            largest_calorie_count = current
            elf_num = current_elf_num

        current_elf_num += 1

    print(f"problem 1 : elf {elf_num} -> {largest_calorie_count}")
