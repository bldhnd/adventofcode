import strategy

def problem_1() -> None:
    op_rock = "A"
    op_paper = "B"
    op_scissors = "C"

    me_rock = "X"
    me_paper = "Y"
    me_scissors = "Z"

    rock_point = 1
    paper_point = 2
    scissor_point = 3

    win = 6
    draw = 3
    lose = 0

    score = 0

    for play in strategy.rps_guide.split("\n"):
        opponent = play[0]
        me = play[2]

        if me == me_rock:
            play_point = rock_point
        elif me == me_paper:
            play_point = paper_point
        elif me == me_scissors:
            play_point = scissor_point

        if opponent == op_rock:
            if me == me_rock:
                score += play_point + draw
            elif me == me_paper:
                score += play_point + win
            elif me == me_scissors:
                score += play_point + lose
        elif opponent == op_paper:
            if me == me_rock:
                score += play_point + lose
            elif me == me_paper:
                score += play_point + draw
            else:
                score += play_point + win
        elif opponent == op_scissors:
            if me == me_rock:
                score += play_point + win
            elif me == me_paper:
                score += play_point + lose
            elif me == me_scissors:
                score += play_point + draw
        
    print(f"Score: {score}")