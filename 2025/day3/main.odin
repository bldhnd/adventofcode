package aoc

import "core:fmt"


ASCII_ZERO :: 48

main :: proc() {
  // day_one(PUZZLE_INPUT)
  day_two(SAMPLE_INPUT)
}

day_one :: proc(input: string) {
  // Answer: 17430
  answer := 0
  current_bank, ok := read_bank(input, 0)

  for ok {
    for i := 0; i < len(current_bank.bank) - 1; i += 1 {
      ch := current_bank.bank[i]

      num := int((ch - ASCII_ZERO) * 10)

      if num > current_bank.tens {
        current_bank.tens = num
        current_bank.tens_index = i
      }
    }

    for i := current_bank.tens_index + 1; i < len(current_bank.bank); i += 1 {
      ch := current_bank.bank[i]

      num := int(ch - ASCII_ZERO)

      if num > current_bank.ones {
        current_bank.ones = num
      }
    }

    answer += current_bank.tens + current_bank.ones

    current_bank, ok = read_bank(input, current_bank.row + 1)
  }

  fmt.println("Day three part one answer", answer)
}

day_two :: proc(input: string) {
  answer := 0
  current_bank, ok := read_bank_v2(input, 0)

  for ok {
    // TODO: impl

    current_bank, ok = read_bank_v2(input, current_bank.row + 1)
  }

  fmt.println("Day three part two answer", answer)
}

read_bank :: proc(input: string, row: int) -> (Battery_Bank, bool) {
  bank, ok := parse_bank(input, row)

  if !ok {
    return {}, false
  }

  return {bank = bank, row = row}, true
}

read_bank_v2 :: proc(input: string, row: int) -> (Battery_Bank_V2, bool) {
  bank, ok := parse_bank(input, row)

  if !ok {
    return {}, false
  }

  return {bank = bank, row = row}, true
}

parse_bank :: proc(input: string, row: int) -> (string, bool) {
  length := 0

  for i := 0;; i += 1 {
    if input[i] == '\n' {
      length = i + 1
      break
    }
  }

  start := row * length

  if start >= len(input) {
    return "", false
  }

  bank := input[start:start + length - 1]

  return bank, true
}

Battery_Bank :: struct {
  bank:  string,
  row:   int,
  tens:  int,
  tens_index: int,
  ones:  int,
  index: int,
}

// 000,000,000,000
Battery_Bank_V2 :: struct {
  bank:      string,
  row:       int,
  nums:      [12]int,
  num_index: int,
}