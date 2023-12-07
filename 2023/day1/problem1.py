import puzzleinput


def problem_1() -> None:
    current_input = puzzleinput.puzzle_input

    inputs = current_input.split('\n')

    total = 0
    for line in inputs:
        numstr = ""

        for ch in line:
            if ch.isnumeric():
                numstr = ch
                break
        
        for idx in range(len(line) - 1, -1, -1):
            ch = line[idx]

            if ch.isnumeric():
                numstr += ch
                break
        
        total += int(numstr)

    print(f"problem 1 solution: {total}")
