package aoc

import "core:fmt"
import "core:strconv"
import "core:math"


main :: proc() {
  puzzle := make_puzzle(SAMPLE_INPUT)

  part_one(puzzle)
  //part_two(puzzle)
}

part_one :: proc(puzzle: Puzzle_Data) {
  // not gonna lie, I understand calc distance but im not sure how to do this part at all
  for i := 0; i < len(puzzle.circuits); i += 1 {
    current := puzzle.circuits[i]

    for j := i + 1; j < len(puzzle.circuits); j += 1 {
      next := puzzle.circuits[j]

      
    }
  }
  for i in 1 ..< len(puzzle.circuits) {
    circuit := puzzle.circuits[i]

    fmt.printfln("distance for %v is %v", circuit.box, distance(first.box, circuit.box))
  }
}

part_two :: proc(puzzle: Puzzle_Data) {

}

distance :: proc(p: Vec3, q: Vec3) -> f32 {
  x := (p.x - q.x) * (p.x - q.x)
  y := (p.y - q.y) * (p.y - q.y)
  z := (p.z - q.z) * (p.z - q.z)

  return math.sqrt(x + y + z)
}

make_puzzle :: proc(input: string) -> Puzzle_Data {
  circuits: [dynamic]Circuit

  current: Vec3
  pos := 0
  index := 0
  ch: u8

  parser: for {
    ch = input[index] if index < len(input) else ASCII_EOF

    switch {
    case ch >= ASCII_ZERO && ch <= ASCII_NINE:
      start := index
      for index < len(input) && input[index] != ASCII_COMMA && input[index] != '\n' { 
        index += 1
      }

      num, _ := strconv.parse_int(input[start:index])
      current[pos] = f32(num)

      continue parser
    case ch == ASCII_COMMA:
      pos += 1
    case ch == '\n' || ch == ASCII_EOF:
      pos = 0
      append(&circuits, Circuit {box = current})

      if ch == ASCII_EOF {
        break parser
      }
    }

    index += 1
  }

  return {
    data = input,
    circuits = circuits[:]
  }
}

Puzzle_Data :: struct {
  data:     string,
  circuits: []Circuit,
}

Circuit :: struct {
  box:  Vec3,
  next: ^Circuit,
}

Vec3 :: [3]f32

ASCII_COMMA :: 44
ASCII_ZERO  :: 48
ASCII_NINE  :: 57
ASCII_EOF   :: 0
