package aoc

import "core:fmt"
import "core:strconv"


main :: proc() {
  //part_one(PUZZLE_INPUT)
  part_two(SAMPLE_INPUT)
}

part_one :: proc(input: string) {
  // Answer: 681 .. first try and runs in ~0.3 secs
  answer := 0
  puzzle := make_puzzle(input)

  id, ok := next_id(&puzzle)

  for ok {
    for range in puzzle.id_ranges {
      (range.start <= id && range.end >= id) or_continue

      answer += 1
      break
    }

    id, ok = next_id(&puzzle)
  }

  fmt.printfln("Day 5 part one answer: %v", answer)
}

part_two :: proc(input: string) {
  answer := 0
  puzzle := make_puzzle(input)

  final_id_ranges: [dynamic]Ingredient_ID_Range
  merged_indexes := make([dynamic]bool, len(puzzle.id_ranges))

  for index in 0 ..< len(puzzle.id_ranges) - 1 {
    (merged_indexes[index] == false) or_continue

    id_range := puzzle.id_ranges[index]

    for next_index in index + 1 ..< len(puzzle.id_ranges) {
      (merged_indexes[next_index] == false) or_continue

      next_id_range := puzzle.id_ranges[next_index]

      if id_range.start >= next_id_range.start && id_range.start <= next_id_range.end {
        merged_indexes[index] = true
        merged_indexes[next_index] = true
      } else if id_range.end >= next_id_range.start && id_range.end <= next_id_range.end {
        merged_indexes[index] = true
        merged_indexes[next_index] = true
      } else {
        continue
      }

      start := min(id_range.start, next_id_range.start)
      end := max(id_range.end, next_id_range.end)

      append(&final_id_ranges, Ingredient_ID_Range {
        start = start,
        end = end,
      })
    }

    if merged_indexes[index] == false {
      append(&final_id_ranges, id_range)
    }
  }

  fmt.println(final_id_ranges)
  fmt.printfln("merged %v", merged_indexes)

  for id_range in final_id_ranges {
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
