package aoc

import "core:fmt"
import "core:strconv"
import "core:strings"
import "core:unicode/utf8"


main :: proc() {
  puzzle := make_puzzle(PUZZLE_INPUT)

  part_one(&puzzle)
  part_two(&puzzle)
}

part_one :: proc(puzzle: ^Puzzle_Data) {
  // Attempt 1: 5212839837770 .. is too low
  // Answer: 5782351442566
  answer := 0
  symbols := parse_puzzle_into_symbols_v3(puzzle)

  #reverse for sym in symbols {
    total := 0

    if sym.data == .Multiply {
      total = 1
      for expr in sym.expressions {
        total *= expr.data.(int)
      }
    } else {
      for expr in sym.expressions {
        total += expr.data.(int)
      }
    }

    answer += total
  }

  fmt.printfln("Day 6 part one answer: %v", answer)
}

part_two :: proc(puzzle: ^Puzzle_Data) {
  // Answer: 10194584711842
  answer := 0
  symbols := parse_puzzle_into_symbols_v3(puzzle)

 for sym in symbols {
   total := 0 if sym.data == .Add else 1

   new_num: [dynamic]rune
   defer delete(new_num)

   for i := 0; i < sym.length; i += 1 {
     #reverse for expr in sym.expressions {
       append(&new_num, rune(expr.raw_data[i]))
     }

     str := utf8.runes_to_string(new_num[:])

     num, _ := strconv.parse_int(strings.trim(str, " "))

     if sym.data == .Multiply {
       total *= num
     } else {
       total += num
     }

     clear(&new_num)
   }

   answer += total
 }

  fmt.printfln("Day 6 part two answer: %v", answer)
}

parse_puzzle_into_symbols_v3 :: proc(puzzle: ^Puzzle_Data) -> []Symbol {
  symbols: [dynamic]Symbol

  read_operators: for i := len(puzzle.data) - 1; i > 0; {
    ch := puzzle.data[i]

    switch ch {
    case ASCII_SPACE:
      end := i

      for puzzle.data[i] == ASCII_SPACE {
        i -= 1
      }

      sym := Symbol {
        index = i,
        length = end - i + 1,
        raw_data = puzzle.data[i:end + 1],
      }

      ch = puzzle.data[i]

      if ch == ASCII_STAR {
        sym.data = .Multiply
      } else if ch == ASCII_PLUS {
        sym.data = .Add
      }

      append(&symbols, sym)

      i -= 1

      if puzzle.data[i] == ASCII_SPACE {
        i -= 1
      }
    case '\n':
      break read_operators
    case:
      i -= 1
    }
  }

  for &op_sym in symbols {
    expressions: [dynamic]Symbol

    for row in 1 ..= puzzle.row_count {
      // work out the index for the start of the column above the current row
      index := op_sym.index - puzzle.row_length * row - row

      sym := Symbol {
        index  = index,
        length = op_sym.length,
        raw_data = puzzle.data[index:index + op_sym.length],
      }

      num, _ := strconv.parse_int(strings.trim(sym.raw_data, " "))

      sym.data = num

      append(&expressions, sym)
    }

    op_sym.expressions = expressions[:]
  }

  return symbols[:]
}

total_rows :: proc(input: string) -> int {
  row_count := 0

  for ch in input {
    (ch == '\n') or_continue

    row_count += 1
  }

  return row_count
}

line_length :: proc(input: string) -> int {
  for ch, i in input {
    (ch == '\n') or_continue

    return i
  }

  return 0
}

make_puzzle :: proc(input: string) -> Puzzle_Data {
  return {
    data       = input,
    row_length = line_length(input),
    row_count  = total_rows(input),
  }
}

Symbol_Op :: enum {
  Add      = 0,
  Multiply = 1,
}

Symbol :: struct {
  index:       int,
  length:      int,
  raw_data:    string,
  expressions: []Symbol,
  data: union {
    int,
    Symbol_Op,
  } 
}

Puzzle_Data :: struct {
  data:       string,
  row_length: int,
  row_count:  int,
}

ASCII_SPACE :: 32
ASCII_STAR :: 42
ASCII_PLUS :: 43
