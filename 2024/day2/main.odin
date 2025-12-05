package main

import "core:fmt"
import "core:mem"


main :: proc() {
	when ODIN_DEBUG {
		track: mem.Tracking_Allocator
		mem.tracking_allocator_init(&track, context.allocator)
		context.allocator = mem.tracking_allocator(&track)

		defer {
			if len(track.allocation_map) > 0 {
				fmt.eprintf("=== %v allocations not freed: ===\n", len(track.allocation_map))
				for _, entry in track.allocation_map {
					fmt.eprintf("- %v bytes @ %v\n", entry.size, entry.location)
				}
			}
			if len(track.bad_free_array) > 0 {
				fmt.eprintf("=== %v incorrect frees: ===\n", len(track.bad_free_array))
				for entry in track.bad_free_array {
					fmt.eprintf("- %p @ %v\n", entry.memory, entry.location)
				}
			}
			mem.tracking_allocator_destroy(&track)
		}
	}

	problem_two()
}

problem_one :: proc() {
	data := parse_input(PUZZLE_INPUT)
	defer {
		for lst in data do delete(lst)
		delete(data)
	}

	safe_count := 0

	for list in data {
		is_safe := true
		is_decreasing := list[0] > list[1]

		for index in 0 ..< len(list) - 1 {
			current := list[index]
			next := list[index + 1]

			if is_decreasing && current < next {
				is_safe = false
				break
			} else if !is_decreasing && next < current {
				is_safe = false
				break
			}

			diff := abs(current - next)

			if diff <= 0 || diff > 3 {
				is_safe = false
				break
			}
		}

		if is_safe {
			safe_count += 1
		}
	}

	fmt.println("Problem one answer is", safe_count)
}

// First attemp is too low
problem_two :: proc() {
	data := parse_input(SAMPLE_INPUT)
	defer {
		for lst in data do delete(lst)
		delete(data)
	}

	safe_count := 0

	for list in data {
		skip_count := 0
		is_safe := true
		is_decreasing := list[0] > list[1]

		for index in 0 ..< len(list) - 1 {
			current := list[index]
			next := list[index + 1]

			if is_decreasing && current < next {
				is_safe = false
				break
			} else if !is_decreasing && next < current {
				is_safe = false
				break
			}

			diff := abs(current - next)

			if diff <= 0 || diff > 3 {
				skip_count += 1
			} else {
				continue
			}

			if skip_count > 1 {
				is_safe = false
				break
			}

			next = list[index + 2]

			diff = abs(current - next)

			if diff <= 0 || diff > 3 {
				is_safe = false
				break
			}
		}

		if is_safe {
			fmt.println("list", list)
			safe_count += 1
		}
	}

	fmt.println("Problem two answer is", safe_count)
}
