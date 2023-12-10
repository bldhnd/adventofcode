import puzzleinput


def problem_2() -> None:
    pos = 0
    total = 0

    ROW_LEN = 141
    CURRENT_INPUT = puzzleinput.PUZZLE_INPUT
    GEAR_SYMBOL = "*"

    def read_number_at(pos: int, puzzle_input: str) -> int:
        number_str = ''

        if pos < len(puzzle_input) and puzzle_input[pos].isnumeric():
            start = pos
            ch = puzzle_input[start]

            while ch.isnumeric():
                start -= 1
                ch = puzzle_input[start]
            
            start += 1
            ch = puzzle_input[start]
            
            while ch.isnumeric():
                number_str += ch
                start += 1
                ch = puzzle_input[start]
        
        return int(number_str) if number_str.isnumeric() else 0

    while pos < len(CURRENT_INPUT):
        while pos < len(CURRENT_INPUT) and CURRENT_INPUT[pos] != GEAR_SYMBOL:
            pos += 1
        
        top = pos - ROW_LEN

        parts = []

        top_number = read_number_at(top, CURRENT_INPUT)

        if top_number > 0:
            parts.append(top_number)

        top_left = read_number_at(top - 1, CURRENT_INPUT)

        if top_left > 0 and top_left != top_number:
            parts.append(top_left)

        top_right = read_number_at(top + 1, CURRENT_INPUT)
        
        if top_right > 0 and top_right != top_number:
            parts.append(top_right)

        left = read_number_at(pos - 1, CURRENT_INPUT)

        if left > 0:
            parts.append(left)

        right = read_number_at(pos + 1, CURRENT_INPUT)

        if right > 0:
            parts.append(right)

        bottom = pos + ROW_LEN

        bottom_number = read_number_at(bottom, CURRENT_INPUT)

        if bottom_number > 0:
            parts.append(bottom_number)

        bottom_left = read_number_at(bottom - 1, CURRENT_INPUT)
        
        if bottom_left > 0 and bottom_left != bottom_number:
            parts.append(bottom_left)

        bottom_right = read_number_at(bottom + 1, CURRENT_INPUT)
        
        if bottom_right > 0 and bottom_right != bottom_number:
            parts.append(bottom_right)

        if len(parts) == 2:
            # print(f"Gear found at {pos} with parts {repr(parts)}")
            total += parts[0] * parts[1]

        # print(f"pos {pos}: tl: {top_left}, t {top_number}, tr {top_right}, l {left}, r {right}, bl {bottom_left}, b {bottom_number}, br {bottom_right}")
        # print()

        pos += 1

    print(f"Problem 1 is {total}")
