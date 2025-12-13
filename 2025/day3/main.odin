package aoc

import "core:fmt"


ASCII_ZERO :: 48

main :: proc() {
  day_one(PUZZLE_INPUT)
}

day_one :: proc(input: string) {
  // Answer: 17430
  answer := 0
  current_bank, ok := read_bank(input, 0)

  for ok {
    // fmt.println("bank", current_bank.row)

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

    // fmt.printfln("row %v total %v", current_bank.row, current_bank.tens + current_bank.ones)

    answer += current_bank.tens + current_bank.ones

    current_bank, ok = read_bank(input, current_bank.row + 1)
  }

  fmt.println("Day three part one answer", answer)
}

day_two :: proc(input: string) {

}

read_bank :: proc(input: string, row: int) -> (Battery_Bank, bool) {
    length := 0

    for i := 0;; i += 1 {
      if input[i] == '\n' {
        length = i + 1
        break
      }
    }

    start := row * length

    if start >= len(input) {
      return {}, false
    }

    bank := input[start:start + length - 1]

    return {bank = bank, row = row}, true
}

Battery_Bank :: struct {
  bank:  string,
  row:   int,
  tens:  int,
  tens_index: int,
  ones:  int,
  index: int,
}
