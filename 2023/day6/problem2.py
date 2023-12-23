import puzzleinput
from math import floor


def problem_2() -> None:
    CURRENT_INPUT = puzzleinput.PUZZLE_INPUT

    def parser(line: str) -> int:
        pos = 0
        ch = ""
        
        current = ''

        while pos < len(line):
            if ch.isnumeric():
                current += ch
            pos += 1
            ch = line[pos] if pos < len(line) else ''
        else:
            return int(current)

    lines = CURRENT_INPUT.split("\n")
    
    time = parser(lines[0])
    distance = parser(lines[1])

    start = 0

    half_way = floor(time / 2)

    for press_len in range(1, half_way):
        candidate = press_len * (time - press_len)

        if candidate > distance:
            start = press_len
            break        

    total = (half_way - start) * 2 + 1
    
    # answer 28545089
    print(f"Problem 2 total ways to win is {total}")