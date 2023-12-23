import puzzleinput


def problem_1() -> None:
    CURRENT_INPUT = puzzleinput.PUZZLE_INPUT

    def parser(line: str) -> list[int]:
        pos = 0
        ch = ""
        
        results = []
        current = ''

        while pos < len(line):
            if not ch.isnumeric() and current.isnumeric():
                results.append(int(current))
                current = ''
            elif ch.isnumeric():
                current += ch
            
            pos += 1
            ch = line[pos] if pos < len(line) else ''
        else:
            results.append(int(current))

        return results

    lines = CURRENT_INPUT.split("\n")
    
    times = parser(lines[0])
    distances = parser(lines[1])

    total = 1

    for idx, time in enumerate(times):
        distance = distances[idx]

        num_of_ways_to_win = 0

        for press_len in range(1, time):
            candidate = press_len * (time - press_len)

            num_of_ways_to_win += 1 if candidate > distance else 0

        total *= num_of_ways_to_win 
    
    print(f"Problem 1 total ways to win is {total}")
