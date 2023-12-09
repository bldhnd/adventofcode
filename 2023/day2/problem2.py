import puzzleinput


def problem_2() -> None:
    total = 0

    for line in puzzleinput.PUZZLE_INPUT.split("\n"):
        pos = 0
        ch = ''

        while ch != ":":
            ch = line[pos]
            pos += 1

        blue = 0
        green = 0
        red = 0

        while pos < len(line):
            pos += 1
            ch = line[pos]
            number_str = ''

            while ch.isnumeric():
                number_str += ch
                pos += 1
                ch = line[pos]
            
            pos += 1
            ch = line[pos]
            color = ''

            while ch not in [",", ";", ""]:
                color += ch
                pos += 1
                ch = line[pos] if pos < len(line) else ""
            
            number = int(number_str)

            if color == "blue" and number > blue:
                blue = number
            elif color == "green" and number > green:
                green = number
            elif color == "red" and number > red:
                red = number
            
            if ch in [",", ";"]:
                pos += 1
                ch = line[pos]
        
        total += blue * green * red
    
    print(f"Problem 2 solution is {total}")
