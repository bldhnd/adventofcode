import puzzleinput as pi
import rope


def problem_1():
    planck_rope = rope.execute_directions(pi.movements, 1, "T")

    tail_visit_count = len(set(planck_rope.tail.where))

    rope_map = rope.build_rope_map(planck_rope)
    tail_map = rope.build_tail_map(planck_rope)
    print(rope_map)
    print(tail_map)

    print(f"Problem 1 : {tail_visit_count}")


def map_every_step():

    # sample_movements = pi.sample_movements.split("\n")
    sample_movements = "R 1\nR 1\nR 1\nU 1\nU 1\nU 1\nL 1\nL 1\nD 1\nD 1\nD 1"

    next_movements = ""
    for movement in sample_movements.split("\n"):
        direction, steps = movement.split(" ")

        for _ in range(int(steps)):
            next_movements += direction + " 1\n"

            print(next_movements.split("\n"))

            planck_rope = rope.execute_directions(next_movements[:-1], 1, "T")

            rope_map = rope.build_rope_map(planck_rope)

            print(rope_map)
