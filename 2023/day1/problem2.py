import puzzleinput


NUMBER_WORDS_START = ['o', 't', 'f', 's', 'e', 'n']
NUMBER_WORDS_END = ['e', 'o', 'r', 'x', 'n', 't']
NUMBER_WORDS = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
NUMBER_MAP = ['1', '2', '3', '4', '5', '6', '7', '8', '9']


def problem_2_alternative() -> None:
    current_input = puzzleinput.puzzle_input

    total = 0

    number_symbols = NUMBER_WORDS + NUMBER_MAP

    for line in current_input.split('\n'):
        first = -1
        last = -1
        first_digit = ''
        last_digit = ''

        for symbol in number_symbols:
            current = line.find(symbol)

            if current != -1 and current < first or first == -1:
                first = current
                first_digit = symbol
            
            current = line.rfind(symbol)

            if current != -1 and current > last or last == -1:
                last = current
                last_digit = symbol
        
        first_digit = first_digit if \
                        first_digit.isnumeric() else \
                        NUMBER_MAP[NUMBER_WORDS.index(first_digit)]
    
        second_digit = last_digit if \
                        last_digit.isnumeric() else \
                        NUMBER_MAP[NUMBER_WORDS.index(last_digit)]
        
        digit = int(first_digit + second_digit)

        total += digit
    
    print(f"problem 2 total is {total}")

def problem_2() -> None:
    current_input = puzzleinput.puzzle_input

    total = 0

    for line in current_input.split('\n'):
        pos = 0
        numbers = []

        while pos < len(line):
            ch = line[pos]

            if ch.isnumeric():
                numbers.append(ch)
                break
            elif ch in NUMBER_WORDS_START:
                word = ch
                is_match = False
                start_pos = pos

                while pos < len(line) and not is_match:
                    pos += 1

                    word += line[pos]

                    if not any([x for x in NUMBER_WORDS if x.startswith(word)]):
                        break

                    is_match = len([x for x in NUMBER_WORDS if x == word]) == 1
                
                if is_match:
                    numbers.append(NUMBER_MAP[NUMBER_WORDS.index(word)])
                    break
                else:
                    pos = start_pos + 1
            else:
                pos += 1
        
        pos = len(line) - 1

        while pos > 0:
            ch = line[pos]

            if ch.isnumeric():
                numbers.append(ch)
                break
            elif ch in NUMBER_WORDS_END:
                word = ch
                is_match = False
                start_pos = pos

                while pos > 0 and not is_match:
                    pos -= 1

                    ch = line[pos]

                    word = ch + word

                    if not any([x for x in NUMBER_WORDS if x.endswith(word)]):
                        break

                    is_match = len([x for x in NUMBER_WORDS if x == word]) == 1
                
                if is_match:
                    numbers.append(NUMBER_MAP[NUMBER_WORDS.index(word)])
                    break
                else:
                    pos = start_pos - 1
            else:
                pos -= 1

        if len(numbers) == 1:
            numbers += numbers

        next_number = int("".join(numbers))

        total += next_number
    
    print(f"problem 2 is {total}")
