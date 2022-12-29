import puzzleinput as pi


def problem_2() -> None:
    for buffer in pi.data_buffer.split("\n"):
        pos = 0
        current = ""

        while pos < len(buffer):
            if len(current) == 14:
                is_valid = False

                for cur_pos in range(len(current)):
                    is_valid = current[cur_pos] not in current[cur_pos + 1:]

                    if not is_valid:
                        break

                if is_valid:
                    break

                current = current[1:]

            current += buffer[pos]

            pos += 1

        print(f"Problem 2 : start ({pos})\n\n{buffer}\n")
