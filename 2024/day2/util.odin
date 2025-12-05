package main

import "core:strconv"
import "core:unicode"
import "core:unicode/utf8"


parse_input :: proc(input: string) -> [][]int {
	defer {
		free_all(context.temp_allocator)
	}

	result: [dynamic][]int
	current: [dynamic]int

	current_digit: [dynamic]rune
	defer delete(current_digit)

	for ch in input {
		if unicode.is_digit(ch) {
			append(&current_digit, ch)
		} else if ch == ' ' {
			number := parse_rune_to_int(current_digit[:], context.temp_allocator)

			append(&current, number)
			clear(&current_digit)
		} else if unicode.is_control(ch) {
			number := parse_rune_to_int(current_digit[:], context.temp_allocator)

			append(&current, number)
			clear(&current_digit)

			append(&result, current[:])
			current = make([dynamic]int)
		}
	}

	return result[:]
}

parse_rune_to_int :: proc(ch: []rune, allocator := context.allocator) -> int {
	str := utf8.runes_to_string(ch, allocator)

	result, _ := strconv.parse_int(str)

	return result
}
