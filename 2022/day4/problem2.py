import puzzleinput as pi


def problem_2() -> None:
    total_overlap = 0

    for assignment_pair in pi.assignment_pairs.split("\n"):
        pair = assignment_pair.split(",")

        first_sections = [int(section) for section in pair[0].split("-")]
        second_sections = [int(section) for section in pair[1].split("-")]

        first_lower = first_sections[0]
        first_upper = first_sections[1]

        second_lower = second_sections[0]
        second_upper = second_sections[1]

        if first_lower >= second_lower and first_upper <= second_upper:
            total_overlap += 1
        elif second_lower >= first_lower and second_upper <= first_upper:
            total_overlap += 1
        elif first_lower <= second_upper and first_lower >= second_lower:
            total_overlap += 1
        elif second_lower <= first_upper and second_lower >= first_lower:
            total_overlap += 1

    print(f"Problem 2 : Total Overlap {total_overlap}")
