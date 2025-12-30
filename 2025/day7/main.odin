package aoc

import "core:fmt"


main :: proc() {
  puzzle := make_puzzle(PUZZLE_INPUT)

  //part_one(&puzzle)
  part_two(&puzzle)
}

part_one :: proc(puzzle: ^Puzzle_Data) {
  // Answer: 1560
  answer := follow_beam_path(&puzzle.start, puzzle)

  print_beam :: proc(beam: ^Tachyon_Beam) {
    fmt.printfln("%p %v", beam, beam)

    if beam.left_beam != nil {
      print_beam(beam.left_beam)
    }

    if beam.right_beam != nil {
      print_beam(beam.right_beam)
    }
  }

  fmt.printfln("Day 7 part one answer is %v", answer)
}

part_two :: proc(puzzle: ^Puzzle_Data) {
  answer := follow_particle_many_worlds_path(puzzle.start.start, puzzle)

  fmt.printfln("Day 7 part two answer is %v", answer)
}

count_beams :: proc(beam: ^Tachyon_Beam) -> int {
  count := 1 if beam.left_beam == nil && beam.right_beam == nil else 0

  if beam.left_beam != nil {
    count += count_beams(beam.left_beam)
  }

  if beam.right_beam != nil {
    count += count_beams(beam.right_beam)
  }

  return count
}

follow_beam_path :: proc(beam: ^Tachyon_Beam, puzzle: ^Puzzle_Data) -> int {
  splits := 0

  current_pos := beam.start

  move_downward: for {
    index := vec2_to_index(current_pos, puzzle.row_length)

    if index >= len(puzzle.data) {
      break move_downward
    }

    ch := rune(puzzle.data[index])

    if ch == '^' {
      pos := current_pos + {-1, 0}

      if !beam_intersects_another_beam_at(pos, &puzzle.start, puzzle) {
        beam.left_beam = new(Tachyon_Beam)
        beam.left_beam.start = pos
      }

      pos = current_pos + {1, 0}

      if !beam_intersects_another_beam_at(pos, &puzzle.start, puzzle) {
        beam.right_beam = new(Tachyon_Beam)
        beam.right_beam.start = pos
      }

      splits = 1 if beam.left_beam != nil || beam.right_beam != nil else 0

      break move_downward
    }

    current_pos += {0, 1}
  }

  if beam.left_beam != nil {
    splits += follow_beam_path(beam.left_beam, puzzle)
  }
  if beam.right_beam != nil {
    splits += follow_beam_path(beam.right_beam, puzzle)
  }

  return splits
}

beam_intersects_another_beam_at :: proc(at: Vec2i, root: ^Tachyon_Beam, puzzle: ^Puzzle_Data) -> bool {
  if at == root.start {
    return true
  }

  if at.x == root.start.x && root.start.y < at.y {
    for y := at.y; y <= root.start.y; y -= 1 {
      up := at + {0, -1}

      index := vec2_to_index(up, puzzle.row_length)

      if index < 0 {
        return false
      }

      ch := rune(puzzle.data[index])

      if ch == '^' {
        return false
      }

      if at == up {
        return true
      }
    }
  }

  if root.left_beam != nil && beam_intersects_another_beam_at(at, root.left_beam, puzzle) {
    return true
  }

  if root.right_beam != nil {
    return beam_intersects_another_beam_at(at, root.right_beam, puzzle)
  }

  return false
}

follow_particle_many_worlds_path :: proc(pos: Vec2i, puzzle: ^Puzzle_Data) -> int {
  // well ive eliminated the need for Tachyon_Beam allocation but still running forever with puzzle data
  // most likely because of deep nested recursion. I can probably eliminate that as well with a for
  // loop but cant think of how to acheive that atm
  path_count := 0

  current_pos := pos

  left: Vec2i
  right: Vec2i

  traverse: for {
    index := vec2_to_index(current_pos, puzzle.row_length)

    if index >= len(puzzle.data) {
      path_count = 1
      break traverse
    }

    ch := rune(puzzle.data[index])

    if ch == '^' {
      left = current_pos + {-1, 0}

      right = current_pos + {1, 0}

      break traverse
    }

    current_pos += {0, 1}
  }

  if left != {0, 0} {
    path_count += follow_particle_many_worlds_path(left, puzzle)
  }

  if right != {0, 0} {
    path_count += follow_particle_many_worlds_path(right, puzzle)
  }

  return path_count
}

make_puzzle :: proc(input: string) -> Puzzle_Data {
  pos := find_start(input)

  return {
    data       = input,
    row_length = get_row_length(input),
    start      = {
      start = pos,
    }
  }
}

find_start :: proc(input: string) -> Vec2i {
  row_length := get_row_length(input)

  pos := Vec2i {0, 0}

  search: for ch, i in input {
    switch ch {
    case ASCII_S:
      pos.x = i
      break search
    case '\n':
      pos.x = 0
      pos.y += 1
    case:
      pos.x += 1
    }
  }

  return pos
}

vec2_to_index :: proc(vec: Vec2i, row_length: int) -> int {
  return vec.x + row_length * vec.y + vec.y
}

get_row_length :: proc(input: string) -> int {
  for ch, i in input {
    (ch == '\n') or_continue

    return i
  }

  return -1
}

Puzzle_Data :: struct {
  data:       string,
  row_length: int,
  start:      Tachyon_Beam,
}

Tachyon_Beam :: struct {
  start:      Vec2i,
  left_beam:  ^Tachyon_Beam,
  right_beam: ^Tachyon_Beam,
}

Vec2i :: [2]int

ASCII_S :: 83
