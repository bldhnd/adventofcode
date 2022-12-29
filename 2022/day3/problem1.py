import puzzleinput as pi


def problem_1() -> None:
    priority_total = 0
    
    for rucksack in pi.rucksacks.split("\n"):
        divider = int(len(rucksack) / 2)

        first = rucksack[:divider]
        second = rucksack[-divider:]

        found = set()

        for first_type in first:
            if first_type in second and first_type not in found:
                found.add(first_type)
                type_code = ord(first_type)

                if type_code >= pi.lowercase_priority_a:
                    priority = type_code - pi.lowercase_priority_a + 1
                else:
                    priority = type_code - pi.uppercase_priority_A + 27

                priority_total += priority

    print(f"problem 1 : priority total {priority_total}")