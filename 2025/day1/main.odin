package puzzle

import "core:fmt"
import "core:strconv"
import "core:unicode"


main :: proc() {
	//day_one(PUZZLE_INPUT)
	day_two(PUZZLE_INPUT)
}

day_one :: proc(input: string) {
  // Answer: 1152
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

			if dial >= 100 {
				dial = dial % 100
			}
		}

    /*
		fmt.printfln(
			"move %v %v..dial was at %v now is at %v",
			direction,
			turn_count,
			old_spot,
			dial,
		)
    */

		if dial == 0 do answer += 1

		direction, turn_count, ok = parse_movement(&parser_state)
	}

	fmt.printfln("Day one part one answer: %v", answer)
}

day_two :: proc(input: string) {
  // Attempt 1: 2519 is too low
  // Attempt 2: 6767 is too high
  // Attempt 3: 6560 is too low
  // Attempt 4: 6594 is wrong
  // Answer: 6671

  answer := 0
	dial := 50

	parser_state := Puzzle_State {
		text  = input,
		index = 0,
	}

	direction, turn_count, ok := parse_movement(&parser_state)

	for ok {
		old_spot := dial
    past_zero := 0

    if turn_count >= 100 {
      past_zero = turn_count / 100
      answer += past_zero
      turn_count = turn_count % 100
    }

		switch direction {
		case 'L':
      dial -= turn_count

      if dial <= -100 {
        past_zero += abs(dial) / 100
        dial = abs(dial) % 100
        answer += past_zero
      } else if old_spot != 0 && dial <= 0 {
        past_zero = 1
        answer += past_zero
      }

      if dial <= 0 {
        dial += 100
      }
		case 'R':
      dial += turn_count

			if dial >= 100 {
        past_zero = dial / 100
        answer += past_zero
        dial = dial % 100
			}
		}

    if dial == 100 {
      dial = 0
    }

    /*
		fmt.printfln(
			"dial at %v, move %v %v. now at %v. past 0 %v (%v) times",
      old_spot,
			direction,
			turn_count,
			dial,
      answer,
      past_zero,
		)
    */

		direction, turn_count, ok = parse_movement(&parser_state)
	}

	fmt.printfln("Day one part two answer: %v", answer)

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
