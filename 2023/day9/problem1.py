import puzzleinput


def problem_1() -> None:
    data = puzzleinput.PUZZLE_INPUT.split("\n")

    def sequence_is_all_zeros(sequence: list[int]) -> bool:
        return len([x for x in sequence if x == 0]) == len(sequence)

    total = 0

    for line in data:
        next_sequence = [[int(x) for x in line.split(" ")]]
        
        while not sequence_is_all_zeros(next_sequence[-1]):
            current = next_sequence[-1]
            sequence = []

            for index in range(0, len(current) - 1):
                val = current[index]
                next_val = current[index + 1]

                sequence.append(next_val - val)

            next_sequence.append(sequence)

        last = 0
        for index in range(len(next_sequence) - 2, -1, -1):
            sequence = next_sequence[index]
            last = sequence[-1] + last
        else:
            total += last
    
    # 1884768153
    print(f"Problem 1 total is {total}")
