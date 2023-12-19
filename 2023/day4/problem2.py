import puzzleinput


def problem_2() -> None:
    CURRENT_INPUT: str = puzzleinput.PUZZLE_INPUT

    total = 0
    won_games: dict = {}

    for line in CURRENT_INPUT.split('\n'):
        pos = 0
        ch = ''
        current_game = ''

        ch = line[pos]

        while ch != ':':
            pos += 1
            ch = line[pos]
            current_game += ch if ch.isnumeric() else ''

        game_number = int(current_game)

        if game_number not in won_games:
            won_games[game_number] = 0

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
        games_won = 0

        while pos < len(line):
            pos += 1
            ch = line[pos] if pos < len(line) else ' '
            
            if ch == ' ' and current_number.isnumeric():
                if current_number in winning_numbers:
                    games_won += 1

                current_number = ''
            elif ch.isnumeric():
                current_number += ch

        won_games[game_number] += 1

        total_copies = won_games[game_number]
        
        for x in range(1, games_won + 1):
            key = game_number + x

            if key not in won_games:
                won_games[key] = 0
            
            won_games[key] += total_copies
    
    total = sum([won_games[key] for key in won_games])

    print(f"Problem 2 total is {total}")