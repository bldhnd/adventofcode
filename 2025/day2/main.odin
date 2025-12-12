package aoc

import "core:fmt"
import "core:strings"
import "core:strconv"


main :: proc() {
  //day_one(PUZZLE_INPUT)
  day_two(PUZZLE_INPUT)
}

day_one :: proc(input: string) {
  // Attempt 1: 865 is too low..attemped to just take up the the current sub string index and search until end of string for that pattern
  // Attempt 2: 1212627 is too low..change here was to use strings.contains to find current candidate string. tested afterwards on sample and got wrong answer
  // Attempt 3: 31000881061 is the answer. I'm retarded and didn't read close enough. I was counting the errors not summing the product ids. lol
  answer := 0
  product_ranges := parse_product_ranges(input)

  for product_range in product_ranges {
    for current in product_range.start ..= product_range.end {
      s := fmt.tprintf("%v", current)
      middle := len(s) / 2


      for middle != 0 {
        candidate := s[:middle]
        da_rest := s[middle:]

        if candidate == da_rest {
          answer += current
          break
        }

        middle = len(candidate) / 2
      }
    }

    free_all(context.temp_allocator)
  }

  fmt.println("Day one part one answer:", answer)
}

day_two :: proc(input: string) {
  // Attempt 1: 46769308530 is too high
  // Answer: 46769308485
  answer := 0
  product_ranges := parse_product_ranges(input)

  for product_range in product_ranges {
    for current in product_range.start ..= product_range.end {
       (current > 10) or_continue

       s := fmt.tprintf("%v", current)

       middle := len(s) / 2 + len(s) % 2

       for middle != 0 {
         candidate := s[:middle]
         da_rest := s[middle:]

         found := len(da_rest) % len(candidate) == 0
         for i := middle; i < len(s) && found; i += len(candidate) {
           next := s[i: i + len(candidate)]

           if candidate != next {
             found = false
           }
         }

         if found {
           answer += current
           break
         }

         middle = len(candidate) / 2

         if len(candidate) > 1 {
           middle += len(candidate) % 2
         }
       }
    }

    free_all(context.temp_allocator)
  }

  fmt.println("Day two part two answer:", answer)
}

parse_product_ranges :: proc(input: string) -> []Product_Range {
  res, err := strings.split(input, ",", context.temp_allocator)

  if err != .None {
    panic(fmt.aprintf("could not split string! %v\n", err))
  }

  ranges: [dynamic]Product_Range

  for id_range in res {
    id_res := strings.split(id_range, "-", context.temp_allocator)

    start, _ := strconv.parse_int(id_res[0])
    end, _ := strconv.parse_int(id_res[1])

    append(&ranges, Product_Range {
      start = start,
      end = end,
    })
  }

  free_all(context.temp_allocator)

  return ranges[:]
}

Product_Range :: struct {
  start: int,
  end:   int,
}
