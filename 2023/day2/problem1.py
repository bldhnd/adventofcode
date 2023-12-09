import puzzleinput


def problem_1() -> None:
    RED_LIMIT = 12
    GREEN_LIMIT = 13
    BLUE_LIMIT = 14

    total_games = 0
    
    for line in puzzleinput.PUZZLE_INPUT.split('\n'):
        blue_cubes = 0
        red_cubes = 0
        green_cubes = 0
        game_number = 0

        def get_game_number(line) -> int:
            pos = 0
            ch = ''
            result = ''

            while ch != ':':
                ch = line[pos]

                if ch.isnumeric():
                    result += ch
                
                pos += 1
        
            return int(result)

        def sum_cube_by_color(line: str, color: str) -> list[int]:
            pos = len(line) - 1
            ch = ''
            current_color = ''
            num_of_colors_sets = []
            

            while ch != ":":
                ch = line[pos]

                if ch == ";" or ch == ',':
                    current_color = ''
                elif color == current_color:
                    current_color = ''
                    number = ''
                    pos -= 1
                    ch = line[pos]

                    while ch != ' ':
                        number = ch + number
                        pos -= 1
                        ch = line[pos]
                    
                    num_of_colors_sets.append(int(number))
                else:
                    current_color = ch + current_color
                
                pos -= 1
            
            return num_of_colors_sets

        game_number = get_game_number(line)
        blue_cubes = sum_cube_by_color(line, "blue")
        green_cubes = sum_cube_by_color(line, "green")
        red_cubes = sum_cube_by_color(line, "red")

        blue_qualifies = all([x <= BLUE_LIMIT for x in blue_cubes])
        green_qualifies = all([x <= GREEN_LIMIT for x in green_cubes])
        red_qualifies = all([x <= RED_LIMIT for x in red_cubes])

        if blue_qualifies and green_qualifies and red_qualifies: 
            total_games += game_number
        
        # print(line)
        # print(f"game {game_number} produced {blue_cubes} blue, {green_cubes} green, {red_cubes} red: total is now {total_games}")
        # print()
    
    print(f"Problem 1 solution is {total_games}")
