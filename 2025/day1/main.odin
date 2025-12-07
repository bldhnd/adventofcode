package puzzle

import "core:fmt"
import "core:strconv"
import "core:unicode"


main :: proc() {
	day_one(PUZZLE_INPUT)
}

day_one :: proc(input: string) {
	answer := 0
	dial := 50

	parser_state := Puzzle_State {
		text  = input,
		index = 0,
	}

	direction, turn_count, ok := parse_movement(&parser_state)

	for ok {
		old_spot := dial

		switch direction {
		case 'L':
			dial -= turn_count % 100

			if dial < 0 {
				dial += 100
			}
		case 'R':
			dial += turn_count % 100

			if dial == 100 {
				dial = 0
			} else if dial > 100 {
				dial = dial % 100
			}
		}

		fmt.printfln(
			"move %v %v..dial was at %v now is at %v",
			direction,
			turn_count,
			old_spot,
			dial,
		)

		if dial == 0 do answer += 1

		direction, turn_count, ok = parse_movement(&parser_state)
	}

	fmt.printfln("puzzle 1 answer: %v", answer)
}

parse_movement :: proc(parser: ^Puzzle_State) -> (rune, int, bool) {
	if len(parser.text) == parser.index {
		return 0, -1, false
	}

	direction := rune(parser.text[parser.index])

	parser.index += 1

	start_index := parser.index

	for parser.index < len(parser.text) && unicode.is_number(rune(parser.text[parser.index])) {
		parser.index += 1
	}

	count, ok := strconv.parse_int(parser.text[start_index:parser.index])

	if !ok {
		panic(
			fmt.aprintf("could not parse turn count! %v\n", parser.text[start_index:parser.index]),
		)
	}

	if parser.index < len(parser.text) {
		parser.index += 1
	}

	return direction, count, true
}

Puzzle_State :: struct {
	text:  string,
	index: int,
}
