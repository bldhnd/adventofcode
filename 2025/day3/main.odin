package aoc

import "core:fmt"


main :: proc() {
  day_one(SAMPLE_INPUT)
}

day_one :: proc(input: string) {

}

day_two :: proc(input: string) {

}

read_bank :: proc(input: string, row: int) -> (Battery_Bank, bool) {

  return {}, false
}

Battery_Bank :: struct {
  bank:       string,
  row:        int,
  tens_index: int,
  ones_index: int,
  index:      int,
}
