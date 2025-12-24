package aoc

import "core:fmt"
import "core:strconv"


main :: proc() {
  puzzle := make_puzzle(SAMPLE_INPUT)

  test(&puzzle)

  //part_one(&puzzle)
  //part_two(&puzzle)
}

test :: proc(puzzle: ^Puzzle_Data) {
  symbols := parse_puzzle_into_symbols(puzzle)
  defer delete(symbols)

  fmt.println(symbols)
}

part_one :: proc(puzzle: ^Puzzle_Data) {
  // Attempt 1: 5212839837770 .. is too low
  // Answer: 5782351442566
  answer := 0
  numbers: [dynamic]int
  defer delete(numbers)

  solve: for {
    sym := look(puzzle, vec2_to_index(puzzle.pos, puzzle.row_length))

    fmt.println(sym, puzzle.pos, vec2_to_index(puzzle.pos, puzzle.row_length))

    switch val in sym.data {
    case int:
      append(&numbers, val)
      puzzle.pos.y += 1
    case Symbol_Op:
      if val == .Add {
        answer += add(numbers[:])
      } else {
        answer += mul(numbers[:])
      }

      clear(&numbers)

      sym = look(puzzle, vec2_to_index({puzzle.pos.x, 0}, puzzle.row_length))

      fast_forward_to_next_number: for i := sym.index + sym.length; i <= puzzle.row_length; i += 1 {
        puzzle.pos.x = i

        ch := puzzle.data[i]

        if ch != ASCII_SPACE {
          break fast_forward_to_next_number
        }
      }

      puzzle.pos.y = 0

      if puzzle.pos.x >= puzzle.row_length {
        break solve
      }
    }
  } 

  fmt.printfln("Day 6 part one answer: %v", answer)
}

part_two :: proc(puzzle: ^Puzzle_Data) {
  answer := 0
  numbers: [dynamic]string
  defer delete(numbers)

  solve: for {
    sym := look(puzzle, vec2_to_index(puzzle.pos, puzzle.row_length))

    fmt.println(sym, puzzle.pos, vec2_to_index(puzzle.pos, puzzle.row_length))

    switch val in sym.data {
    case int:
      append(&numbers, puzzle.data[sym.index:sym.index + sym.length])
      puzzle.pos.y += 1
    case Symbol_Op:
      if val == .Add {
        fmt.printfln("add these %v", numbers)
        //answer += add(numbers[:])
      } else {
        fmt.printfln("mul these %v", numbers)
        //answer += mul(numbers[:])
      }

      clear(&numbers)

      sym = look(puzzle, vec2_to_index({puzzle.pos.x, 0}, puzzle.row_length))

      fast_forward_to_next_number: for i := sym.index + sym.length; i <= puzzle.row_length; i += 1 {
        puzzle.pos.x = i

        ch := puzzle.data[i]

        if ch != ASCII_SPACE {
          break fast_forward_to_next_number
        }
      }

      puzzle.pos.y = 0

      if puzzle.pos.x >= puzzle.row_length {
        break solve
      }
    }
  } 

  fmt.printfln("Day 6 part two answer: %v", answer)
}

add :: proc(numbers: []int) -> int {
  result := 0

  for num in numbers do result += num

  return result
}

mul :: proc(numbers: []int) -> int {
  result := 1

  for num in numbers do result *= num

  return result
}

look :: proc(puzzle: ^Puzzle_Data, start: int) -> Symbol {
  begin := start

  if begin > 0 {
    if puzzle.data[begin - 1] != ASCII_SPACE && puzzle.data[begin - 1] != '\n' {
      rewind: for i := begin - 1; i > 0; i -= 1 {
        ch := puzzle.data[i]

        if ch == ASCII_SPACE || ch == '\n' {
          begin = i
          break rewind
        }
      }
    } else if puzzle.data[begin] == ASCII_SPACE {
      for i := begin; i > 0; i -= 1 {
        ch := puzzle.data[i]

        if ch == ASCII_PLUS || ch == ASCII_STAR {
          begin = i
          break
        }
      }
    }
  }

  trim_leading_space: for i in begin ..< len(puzzle.data) {
    ch := puzzle.data[i]

    if ch != ASCII_SPACE {
      break trim_leading_space
    }

    begin += 1
  }

  ch := puzzle.data[begin]

  if ch == ASCII_STAR {
    return {
      index  = begin,
      length = 1,
      data   = .Multiply,
    }
  }

  if ch == ASCII_PLUS {
    return {
      index  = begin,
      length = 1,
      data   = .Add,
    }
  }

  end := begin
  read_number: for i in begin ..< len(puzzle.data) {
    ch := puzzle.data[i]

    if ch == '\n' || ch == ASCII_SPACE {
      break read_number
    }

    end += 1
  }

  num, _ := strconv.parse_int(puzzle.data[begin:end])

  return {
    index  = begin,
    length = end - begin,
    data   = num,
  }
}

parse_puzzle_into_symbols :: proc(puzzle: ^Puzzle_Data) -> []Symbol {
  symbols: [dynamic]Symbol

  current_pos := 0

  //TODO: break into lines and maybe I can process that better

  return symbols[:]
}

line_length :: proc(input: string) -> int {
  for ch, i in input {
    (ch == '\n') or_continue

    return i
  }

  return 0
}

vec2_to_index :: proc(vec2: Vec2i, line_length: int) -> int {
  return vec2.x + vec2.y * line_length + vec2.y
}

make_puzzle :: proc(input: string) -> Puzzle_Data {
  return {
    data       = input,
    row_length = line_length(input),
    pos        = {0,0},
  }
}

Symbol_Op :: enum {
  Add      = 0,
  Multiply = 1,
}

Symbol :: struct {
  index:    int,
  length:   int,
  raw_data: string,
  data: union {
    int,
    Symbol_Op,
  } 
}

Puzzle_Data :: struct {
  data:       string,
  row_length: int,
  pos:        Vec2i,
}

Vec2i :: [2]int

ASCII_SPACE :: 32
ASCII_ZERO :: 48
ASCII_NINE :: 57
ASCII_STAR :: 42
ASCII_PLUS :: 43
