package main

import "core:fmt"


main :: proc() {
    problem_one()
}

problem_one :: proc() {
    answer := 0

    puzzle := create_puzzle(SAMPLE_INPUT)

    

    fmt.println("Problem one answer is", answer)
}

problem_two :: proc() {
    answer := 0

    fmt.println("Problem two answer is", answer)
}

create_puzzle :: proc(input: string) -> Puzzle {
    return Puzzle {
        input = input,
        length = len(input)
    }
}

Puzzle :: struct {
    input: string,
    length: int,
}