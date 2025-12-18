package aoc

import "core:fmt"


main :: proc() {
	//part_one(PUZZLE_INPUT)
  part_two(SAMPLE_INPUT)
}

part_one :: proc(input: string) {
  // Answer: 1540
  answer := 0
  puzzle := make_puzzle(input)

  for vec_to_index(&puzzle, puzzle.pos) < len(puzzle.rolls_of_paper) {
    found := 0

    if _, ok := look(&puzzle, puzzle.pos); !ok {
      move_forward(&puzzle)
      continue
    }

    // upper left
    if _, ok := look(&puzzle, puzzle.pos + {-1, -1}); ok do found += 1
    // up
    if _, ok := look(&puzzle, puzzle.pos + {0, -1}); ok do found += 1
    // upper right
    if _, ok := look(&puzzle, puzzle.pos + {1, -1}); ok do found += 1
    // right
    if _, ok := look(&puzzle, puzzle.pos + {1, 0}); ok do found += 1
    // down right
    if _, ok := look(&puzzle, puzzle.pos + {1, 1}); ok do found += 1
    // down
    if _, ok := look(&puzzle, puzzle.pos + {0, 1}); ok do found += 1
    // down left
    if _, ok := look(&puzzle, puzzle.pos + {-1, 1}); ok do found += 1
    // left
    if _, ok := look(&puzzle, puzzle.pos + {-1, 0}); ok do found += 1

    answer += 1 if found < 4 else 0

    //index := vec_to_index(&puzzle, puzzle.pos)
    //fmt.printfln("%v = %v %v", index, rune(puzzle.rolls_of_paper[index]), found < 4)

    move_forward(&puzzle)
  }

  fmt.println("day 4 part one answer:", answer)
}

part_two :: proc(input: string) {

}

make_puzzle :: proc(data: string) -> Puzzle_Data {
  return {
    rolls_of_paper = data,
    pos            = {0, 0},
    row_length     = index_of_newline(data),
  }
}

look :: proc(puzzle: ^Puzzle_Data, pos: Vec2i) -> (rune, bool) #optional_ok {
  index := vec_to_index(puzzle, pos)

  if index < 0 {
    return 0, false
  }

  if index >= len(puzzle.rolls_of_paper) {
    return 0, false
  }

  ch := puzzle.rolls_of_paper[index]

  return rune(ch), ch == '@'
}

vec_to_index :: proc(puzzle: ^Puzzle_Data, vec: Vec2i) -> int {
  index := vec.x + vec.y * puzzle.row_length + vec.y

  return index
}

move_forward :: proc(puzzle: ^Puzzle_Data) {
  puzzle.pos.x += 1

  if puzzle.pos.x > puzzle.row_length - 1 {
    puzzle.pos.x = 0
    puzzle.pos.y += 1
  }
}

index_of_newline :: proc(input: string) -> int {
  for i := 0; i < len(input); i += 1 {
    (input[i] == '\n') or_continue

    return i
  }

  return 0
}

Puzzle_Data :: struct {
  rolls_of_paper: string,
  pos:            Vec2i,
  row_length:     int,
}

Vec2i :: [2]int
