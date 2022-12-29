import puzzleinput as pi


def problem_2() -> None:
    three_rucksacks = []
    priority_total = 0
    
    rucksacks = pi.rucksacks.split("\n")
    pos = 0
    size = len(rucksacks)

    while pos < size:
        three_rucksacks.append(rucksacks[pos])

        if len(three_rucksacks) == 3:
            for item in three_rucksacks[0]:
                if item in three_rucksacks[1] and item in three_rucksacks[2]:
                    code_type = ord(item)

                    if code_type >= pi.lowercase_priority_a:
                        priority_total += code_type - pi.lowercase_priority_a + 1
                    else:
                        priority_total += code_type - pi.uppercase_priority_A + 27
                    
                    break

            three_rucksacks.clear()
        
        pos += 1
    
    print(f"problem 2 : priority total {priority_total}")