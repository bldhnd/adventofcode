import puzzleinput as pi


def problem_1():
    row = 0
    col = 0

    for pos, height in enumerate(pi.sample_heightmap):
        if height == "S":
            col = pos
            break
        elif height == "\n":
            row += 1
