import strategy

def problem_2() -> None:
    op_rock = "A"
    op_paper = "B"
    op_scissors = "C"
    
    me_lose = "X"
    me_draw = "Y"
    me_win = "Z"

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

        if opponent == op_rock:
            if me == me_lose:
                score += scissor_point + lose
            elif me == me_draw:
                score += rock_point + draw
            elif me == me_win:
                score += paper_point + win
        elif opponent == op_paper:
            if me == me_lose:
                score += rock_point + lose
            elif me == me_draw:
                score += paper_point + draw
            elif me == me_win:
                score += scissor_point + win
        elif opponent == op_scissors:
            if me == me_lose:
                score += paper_point + lose
            elif me == me_draw:
                score += scissor_point + draw
            elif me == me_win:
                score += rock_point + win
    
    print(f"Score: {score}")