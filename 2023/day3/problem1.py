import puzzleinput


def problem_1() -> None:
    pos = 0
    total = 0

    ROW_LEN = 141
    CURRENT_INPUT = puzzleinput.PUZZLE_INPUT

    non_special_chars = ['.', '\n', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '']

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
        while pos < len(CURRENT_INPUT) and CURRENT_INPUT[pos] in non_special_chars:
            pos += 1
        
        top = pos - ROW_LEN

        top_number = read_number_at(top, CURRENT_INPUT)

        total += top_number

        top_left = read_number_at(top - 1, CURRENT_INPUT)

        if top_left != top_number:
            total += top_left
        
        top_right = read_number_at(top + 1, CURRENT_INPUT)

        if top_right != top_number:
            total += top_right
        
        left = read_number_at(pos - 1, CURRENT_INPUT)

        total += left

        right = read_number_at(pos + 1, CURRENT_INPUT)

        total += right

        bottom = pos + ROW_LEN

        bottom_number = read_number_at(bottom, CURRENT_INPUT)

        total += bottom_number

        bottom_left = read_number_at(bottom - 1, CURRENT_INPUT)

        if bottom_left != bottom_number:
            total += bottom_left
        
        bottom_right = read_number_at(bottom + 1, CURRENT_INPUT)

        if bottom_right != bottom_number:
            total += bottom_right
        
        # if pos < len(CURRENT_INPUT):
        #     print(f"found {CURRENT_INPUT[pos]} at {pos}")
        #     print(f"tl: {top_left}, t {top_number}, tr {top_right}, l {left}, r {right}, bl {bottom_left}, b {bottom_number}, br {bottom_right}")
        #     print()

        pos += 1

    print(f"Problem 1 is {total}")
