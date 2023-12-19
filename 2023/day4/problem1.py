import puzzleinput


def problem_1() -> None:
    CURRENT_INPUT = puzzleinput.PUZZLE_INPUT

    total = 0

    for line in CURRENT_INPUT.split('\n'):
        pos = 0
        ch = ''

        ch = line[pos]

        while ch != ':':
            pos += 1
            ch = line[pos]

        winning_numbers = []
        current_number = ''

        pos += 1
        ch = line[pos]

        while ch != '|':
            pos += 1
            ch = line[pos]

            if ch == ' ' and current_number.isnumeric():
                winning_numbers.append(current_number)
                current_number = ''
            elif ch.isnumeric():
                current_number += ch

        pos += 1
        ch = line[pos]

        current_number = ''
        game_points = 0

        while pos < len(line):
            pos += 1
            ch = line[pos] if pos < len(line) else ' '
            
            if ch == ' ' and current_number.isnumeric():
                if current_number in winning_numbers:
                    game_points = 1 if game_points == 0 else game_points * 2
                
                current_number = ''
            elif ch.isnumeric():
                current_number += ch
        
        total += game_points
    
    print(f"Problem 1 total is {total}")
