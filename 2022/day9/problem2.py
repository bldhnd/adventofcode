import puzzleinput as pi
import rope


def problem_2():
    movements = pi.movements

    planck_rope = rope.execute_directions(movements, 9)

    tail_visit_count = len(set(planck_rope.tail.where))

    rope_map = rope.build_rope_map(planck_rope)
    tail_map = rope.build_tail_map(planck_rope)

    print(rope_map)
    print(tail_map)

    print(f"Problem 2 : {tail_visit_count}")


def map_every_step():

    # sample_movements = pi.sample_larger_movements
    sample_movements = "R 5\nU 8\nL 8\nD 3\nR 17\nD 10\nL 25\nU 20"

    next_movements = ""
    for movement in sample_movements.split("\n"):
        direction, steps = movement.split(" ")

        for _ in range(int(steps)):
            next_movements += direction + " 1\n"

            # print(next_movements.split("\n"))

            planck_rope = rope.execute_directions(next_movements[:-1], 9)

            rope_map = rope.build_rope_map(planck_rope)

            print(rope_map)
