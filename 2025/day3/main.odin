package aoc

import "core:fmt"
import "core:math"


ASCII_ZERO :: 48

main :: proc() {
  //day_one(PUZZLE_INPUT)
  day_two(SAMPLE_INPUT)
}

day_one :: proc(input: string) {
  // Answer: 17430
  answer := 0
  current_bank, ok := read_bank(input, 0)

  for ok {
    tens_index := 0
    for i := 0; i < len(current_bank.bank) - 1; i += 1 {
      ch := current_bank.bank[i]

      num := int((ch - ASCII_ZERO) * 10)

      if num > current_bank.nums[0] {
        current_bank.nums[0] = num
        tens_index = i
      }
    }

    for i := tens_index + 1; i < len(current_bank.bank); i += 1 {
      ch := current_bank.bank[i]

      num := int(ch - ASCII_ZERO)

      if num > current_bank.nums[1] {
        current_bank.nums[1] = num
      }
    }

    answer += current_bank.nums[0] + current_bank.nums[1]

    current_bank, ok = read_bank(input, current_bank.row + 1)
  }

  fmt.println("Day three part one answer", answer)
}

day_two :: proc(input: string) {
  // Attempt 1: 97873208283880 is too low
  answer := 0
  current_bank, ok := read_bank(input, 0)

  for ok {
    pop_count := 0

    for i := 0; i < len(current_bank.bank); i += 1 {
      num := int(current_bank.bank[i] - ASCII_ZERO)

      stack_index := current_bank.num_index

      if stack_index == 0 {
        current_bank.nums[stack_index] = num
        current_bank.num_index += 1
      } else if stack_index < 12 && current_bank.nums[stack_index - 1] > num {
        current_bank.nums[stack_index] = num
        current_bank.num_index += 1
      } else if pop_count < len(current_bank.bank) - 12 && current_bank.nums[stack_index - 1] < num {
        for si := stack_index - 1;
            si >= 0 && si < len(current_bank.bank) - 12 && current_bank.nums[si] < num;
            si -= 1 {
          current_bank.nums[si] = num
          pop_count += 1
        }
      } else if stack_index < len(current_bank.nums) {
        current_bank.nums[stack_index] = num
        current_bank.num_index += 1
      }
    }

    num := 0
    exponent := 0.0
    #reverse for n in current_bank.nums {
      num += n * int(math.pow10(exponent))
      exponent += 1
    }

    //ok = false

    fmt.printfln("row %v is %v.", current_bank.row, num)

    answer += num

    current_bank, ok = read_bank(input, current_bank.row + 1)
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

// 000,000,000,000
Battery_Bank :: struct {
  bank:      string,
  row:       int,
  nums:      [12]int,
  num_index: int,
}
