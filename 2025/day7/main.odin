package aoc

import "core:fmt"
import q "core:container/queue"


main :: proc() {
  puzzle := make_puzzle(PUZZLE_INPUT)

  //part_one(&puzzle)
  part_two(&puzzle)
}

part_one :: proc(puzzle: ^Puzzle_Data) {
  // Answer: 1560
  answer := follow_beam_path(&puzzle.start, puzzle)

  fmt.printfln("Day 7 part one answer is %v", answer)
}

part_two :: proc(puzzle: ^Puzzle_Data) {
  pos := Vec2i {0, 130}

  print_out: for i := 0; i < 20; i += 1 {
    index := vec2_to_index(pos, puzzle.row_length)

    if index >= len(puzzle.data) do break print_out

    fmt.print(pos.y)

    for _ in 0 ..< puzzle.row_length {
      index := vec2_to_index(pos, puzzle.row_length)

      ch := rune(puzzle.data[index])

      if pos.x == 13 && pos.y >= 132 {
        fmt.print("[")
      }

      fmt.print(ch)

      if pos.x == 13 && pos.y >= 132 {
        fmt.print("]")
      }

      pos.x += 1
    }

    fmt.println()

    pos.x = 0
    pos.y += 1
  }

  //answer := follow_particle_many_worlds_path(puzzle)

  //fmt.printfln("Day 7 part two answer is %v", answer)
}

count_unique_splitters :: proc(beam: ^Tachyon_Beam, splitters: ^[dynamic]Vec2i) {
  found := false
  for splitter in splitters {
    (splitter == beam.split_at) or_continue

    found = true
    break
  }

  if !found {
    append(splitters, beam.split_at)
  }

  if beam.left_beam != nil {
    count_unique_splitters(beam.left_beam, splitters)
  }

  if beam.right_beam != nil {
    count_unique_splitters(beam.right_beam, splitters)
  }
}

print_beam :: proc(beam: ^Tachyon_Beam) {
  fmt.printfln("%p %v", beam, beam)

  if beam.left_beam != nil {
    print_beam(beam.left_beam)
  }

  if beam.right_beam != nil {
    print_beam(beam.right_beam)
  }
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
        beam.left_beam.split_at = current_pos
        beam.left_beam.start    = pos
      }

      pos = current_pos + {1, 0}

      if !beam_intersects_another_beam_at(pos, &puzzle.start, puzzle) {
        beam.right_beam = new(Tachyon_Beam)
        beam.right_beam.split_at = current_pos
        beam.right_beam.start    = pos
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

follow_particle_many_worlds_path :: proc(puzzle: ^Puzzle_Data) -> int {
  path_count := 0

  stack: q.Queue(^Splitter)

  q.init(&stack)
  defer q.destroy(&stack)

  make_splitter :: proc(pos: Vec2i) -> ^Splitter {
    s := new(Splitter)
    s.pos = pos

    return s
  }

  q.push_front(&stack, make_splitter(puzzle.start.split_at))

  current := q.back_ptr(&stack)^
  current_pos := current.pos

  //fmt.println("start", current)

  dump_stack :: proc(stack: ^q.Queue(^Splitter)) {
    fmt.printf("STACK::")
    for i := 0; i < q.len(stack^); i += 1 {
      item := q.get(stack, i)
      fmt.printfln("  %v", item)
    }
    fmt.println()
  }

  traverse: for q.len(stack) > 0 {

    next := q.front_ptr(&stack)^

    if next != current {
      current = next
      current_pos = current.pos

      //fmt.println("current", current)

      if current.left != nil {
        //fmt.println("  current.left", current.left)
      }
 
      if current.right != nil {
        //fmt.println("  current.right", current.right)
      }
   }

    if current.left != nil && current.left.done && current.right != nil && current.right.done {
      q.pop_front(&stack)

      free(current.left)
      free(current.right)

      current.left = nil
      current.right = nil

      current.done = true

      //fmt.println("current done", current)

      dump_stack(&stack)
      continue traverse
    }

    index := vec2_to_index(current_pos, puzzle.row_length)

    if index > len(puzzle.data) {
      last := q.pop_front(&stack)
      last.done = true

      //fmt.println("popped", last)

      path_count += 1

      dump_stack(&stack)
      continue traverse
    }

    ch := rune(puzzle.data[index])

    if ch == '^' {
      current.left = make_splitter(current_pos + {-1, 0})
      current.right = make_splitter(current_pos + {1, 0})

      //fmt.println("  splitting left at", current.left)
      //fmt.println("  splitting right at", current.right)

      q.push_front(&stack, current.right)
      q.push_front(&stack, current.left)

      dump_stack(&stack)
      continue traverse
    }

    current_pos += {0, 1}
  }

  return path_count
}

Splitter :: struct {
  pos:   Vec2i,
  done:  bool,
  left:  ^Splitter,
  right: ^Splitter,
}

make_puzzle :: proc(input: string) -> Puzzle_Data {
  pos := find_start(input)

  return {
    data       = input,
    row_length = get_row_length(input),
    start      = {
      split_at = pos,
      start    = pos,
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
  split_at:   Vec2i,
  start:      Vec2i,
  left_beam:  ^Tachyon_Beam,
  right_beam: ^Tachyon_Beam,
}

Vec2i :: [2]int

ASCII_S :: 83
