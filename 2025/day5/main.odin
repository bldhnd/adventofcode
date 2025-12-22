package aoc

import "core:fmt"
import "core:sort"
import "core:strconv"


main :: proc() {
  puzzle := make_puzzle(SAMPLE_INPUT)

  //part_one(&puzzle)
  //part_two(&puzzle)
}

part_one :: proc(puzzle: ^Puzzle_Data) {
  // Answer: 681 .. first try and runs in ~0.3 secs
  answer := 0

  id, ok := next_id(puzzle)

  for ok {
    for range in puzzle.id_ranges {
      (range.start <= id && range.end >= id) or_continue

      answer += 1
      break
    }

    id, ok = next_id(puzzle)
  }

  fmt.printfln("Day 5 part one answer: %v", answer)
}

part_two :: proc(puzzle: ^Puzzle_Data) {
  // Attempt 1: 354966828391732 .. too damn high
  // Attempt 2: 351974077086541 .. still too damn high
  // Attempt 3: 351974077086445 .. wow, still high
  answer := 0

  for id_range in puzzle.id_ranges {
    fmt.printfln("%15d - %15d", id_range.start, id_range.end)
    answer += id_range.end - id_range.start + 1
  }

  fmt.printfln("Day 5 part two answer: %v", answer)
}

next_id :: proc(puzzle: ^Puzzle_Data) -> (int, bool) {
  start := puzzle.current_id_index
  data_length := len(puzzle.data)

  if start == data_length {
    return 0, false
  }

  for i := start; i < data_length; i += 1 {
    ch := rune(puzzle.data[i])

    if ch == '\n' {
      num, _ := strconv.parse_int(puzzle.data[start:i])

      puzzle.current_id_index = i + 1

      return num, true
    }
  }

  num, _ := strconv.parse_int(puzzle.data[start:data_length])

  puzzle.current_id_index = data_length

  return num, true
}

make_puzzle :: proc(data: string) -> Puzzle_Data {
  puzzle := Puzzle_Data {
    data = data,
  }

  id_ranges: [dynamic]Ingredient_ID_Range

  last_newline := 0
  start_id_index := 0
  range_ch_index := 0

  for ch, i in data {
    if ch == '\n' && last_newline == i {
      start_id_index = i + 1
      break
    }

    if ch == '\n' {
      first_num, _  := strconv.parse_int(data[last_newline:range_ch_index])
      last_num, _ := strconv.parse_int(data[range_ch_index + 1:i])

      append(&id_ranges, Ingredient_ID_Range {
          start = first_num,
          end = last_num,
      })
 
      last_newline = i + 1
    } else if ch == '-' {
      range_ch_index = i
    }
  }

  id_range_sort :: proc(lhs, rhs: Ingredient_ID_Range) -> int {
    return -1 if lhs.start < rhs.start else 1
  }

  sort.quick_sort_proc(id_ranges[:], id_range_sort)

  final_id_ranges := make([dynamic]Ingredient_ID_Range)

  current_id := &id_ranges[0]

  for &id_range, index in id_ranges[1:] {
    if current_id.start >= id_range.start && current_id.start <= id_range.start ||
      current_id.end >= id_range.end && current_id.end <= id_range.end {
        current_id.start = min(current_id.start, id_range.start)
        current_id.end = max(current_id.end, id_range.end)
      } else {
        append(&final_id_ranges, current_id^)
        current_id = &id_range
      }
  }

  for r in final_id_ranges {
    fmt.println(r.start, r.end)
  }

  return {
    data = data,
    id_ranges = id_ranges[:],
    current_id_index = start_id_index,
  }
}

Puzzle_Data :: struct {
  data:             string,
  id_ranges:        []Ingredient_ID_Range,
  current_id_index: int,
}

Ingredient_ID_Range :: struct {
  start: int,
  end:   int,
}
