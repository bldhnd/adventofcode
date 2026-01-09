package aoc

import "core:fmt"
import "core:c"
import rl "vendor:raylib"
import q "core:container/queue"


main :: proc() {
  puzzle := make_puzzle(PUZZLE_INPUT)

  //part_one(&puzzle)
  //part_two(&puzzle)
  visualize_part_two(&puzzle)
}

part_one :: proc(puzzle: ^Puzzle_Data) {
  // Answer: 1560
  answer := follow_beam_path(&puzzle.start, puzzle)

  fmt.printfln("Day 7 part one answer is %v", answer)
}

part_two :: proc(puzzle: ^Puzzle_Data) {
  answer := follow_particle_many_worlds_path(puzzle)

  fmt.printfln("Day 7 part two answer is %v", answer)
}

visualize_part_two :: proc(puzzle: ^Puzzle_Data) {
  rl.SetConfigFlags({.WINDOW_RESIZABLE})
  rl.InitWindow(800, 800, "Visualize Part Two")
  defer rl.CloseWindow()

  the_shit: [dynamic]Puzzle_Piece

  FONT_SIZE :: 12
  SIZE :: rl.Vector2 {20, 20}
  pos: rl.Vector2

  dot_image := rl.GenImageColor(c.int(SIZE[0]), c.int(SIZE[1]), rl.BLANK)
  start_image := rl.GenImageColor(c.int(SIZE[0]), c.int(SIZE[1]), rl.BLANK)
  splitter_image := rl.GenImageColor(c.int(SIZE[0]), c.int(SIZE[1]), rl.BLANK)

  rl.ImageDrawText(&dot_image, ".", c.int(SIZE[0] / 2), 0, FONT_SIZE, rl.BLACK)
  rl.ImageDrawText(&start_image, "S", c.int(SIZE[0] / 2), 0, FONT_SIZE, rl.BLACK)
  rl.ImageDrawText(&splitter_image, "^", c.int(SIZE[0] / 2), 6, FONT_SIZE, rl.BLACK)

  dot_texture := rl.LoadTextureFromImage(dot_image)
  start_texture := rl.LoadTextureFromImage(start_image)
  splitter_texture := rl.LoadTextureFromImage(splitter_image)

  rl.UnloadImage(dot_image)
  rl.UnloadImage(start_image)
  rl.UnloadImage(splitter_image)

  for ch in puzzle.data {
    if ch == '\n' {
      pos.x = 0
      pos.y += 1
      continue
    }

    piece := Puzzle_Piece {
      pos = pos,
    }

    switch rune(ch) {
    case '.':
      piece.texture = dot_texture
    case 'S':
      piece.texture = start_texture
    case '^':
      piece.texture = splitter_texture
    }

    append(&the_shit, piece);

    pos.x += 1
  }

  camera := rl.Camera2D {
    zoom = 5,
    offset = {400, 400},
  }

  font := rl.GetFontDefault()
  SPACING :: 1

  for !rl.WindowShouldClose() {

    if rl.IsMouseButtonDown(.LEFT) {
      camera.target += -rl.GetMouseDelta()
    }

    wheel_move := rl.GetMouseWheelMove()

    camera.zoom = clamp(camera.zoom + wheel_move, 1, 10)

    rl.BeginDrawing()
    rl.ClearBackground(rl.RAYWHITE)
    rl.BeginMode2D(camera)

    for piece in the_shit {

      pos := rl.Vector2 {
        piece.pos.x * SIZE[0] + SIZE[0] / 2,
        piece.pos.y * SIZE[1],
      }

      rl.DrawTexturePro(piece.texture, {0, 0, SIZE[0], SIZE[1]}, {pos.x, pos.y, SIZE[0], SIZE[1]}, {}, 0, rl.WHITE)

    }

    // TODO: draw lines between nodes
 
    rl.EndMode2D()
    rl.EndDrawing()
  }
}

Puzzle_Piece :: struct {
  pos:  rl.Vector2,
  texture: rl.Texture,
}

count_unique_splitters :: proc(beam: ^Tachyon_Beam, splitters: ^[dynamic]Vec2i) {
  found := false
  for splitter in splitters {
    (splitter == beam.split_at) or_continue

    found = true
    break
  }

  if !found {
    append(splitters, beam.split_at)
  }

  if beam.left_beam != nil {
    count_unique_splitters(beam.left_beam, splitters)
  }

  if beam.right_beam != nil {
    count_unique_splitters(beam.right_beam, splitters)
  }
}

print_beam :: proc(beam: ^Tachyon_Beam) {
  fmt.printfln("%p %v", beam, beam)

  if beam.left_beam != nil {
    print_beam(beam.left_beam)
  }

  if beam.right_beam != nil {
    print_beam(beam.right_beam)
  }
}

count_beams :: proc(beam: ^Tachyon_Beam) -> int {
  count := 1 if beam.left_beam == nil && beam.right_beam == nil else 0

  if beam.left_beam != nil {
    count += count_beams(beam.left_beam)
  }

  if beam.right_beam != nil {
    count += count_beams(beam.right_beam)
  }

  return count
}

follow_beam_path :: proc(beam: ^Tachyon_Beam, puzzle: ^Puzzle_Data) -> int {
  splits := 0

  current_pos := beam.start

  move_downward: for {
    index := vec2_to_index(current_pos, puzzle.row_length)

    if index >= len(puzzle.data) {
      break move_downward
    }

    ch := rune(puzzle.data[index])

    if ch == '^' {
      pos := current_pos + {-1, 0}

      if !beam_intersects_another_beam_at(pos, &puzzle.start, puzzle) {
        beam.left_beam = new(Tachyon_Beam)
        beam.left_beam.split_at = current_pos
        beam.left_beam.start    = pos
      }

      pos = current_pos + {1, 0}

      if !beam_intersects_another_beam_at(pos, &puzzle.start, puzzle) {
        beam.right_beam = new(Tachyon_Beam)
        beam.right_beam.split_at = current_pos
        beam.right_beam.start    = pos
      }

      splits = 1 if beam.left_beam != nil || beam.right_beam != nil else 0

      break move_downward
    }

    current_pos += {0, 1}
  }

  if beam.left_beam != nil {
    splits += follow_beam_path(beam.left_beam, puzzle)
  }
  if beam.right_beam != nil {
    splits += follow_beam_path(beam.right_beam, puzzle)
  }

  return splits
}

beam_intersects_another_beam_at :: proc(at: Vec2i, root: ^Tachyon_Beam, puzzle: ^Puzzle_Data) -> bool {
  if at == root.start {
    return true
  }

  if at.x == root.start.x && root.start.y < at.y {
    for y := at.y; y <= root.start.y; y -= 1 {
      up := at + {0, -1}

      index := vec2_to_index(up, puzzle.row_length)

      if index < 0 {
        return false
      }

      ch := rune(puzzle.data[index])

      if ch == '^' {
        return false
      }

      if at == up {
        return true
      }
    }
  }

  if root.left_beam != nil && beam_intersects_another_beam_at(at, root.left_beam, puzzle) {
    return true
  }

  if root.right_beam != nil {
    return beam_intersects_another_beam_at(at, root.right_beam, puzzle)
  }

  return false
}

follow_particle_many_worlds_path :: proc(puzzle: ^Puzzle_Data) -> int {
  path_count := 0

  stack: q.Queue(^Splitter)

  q.init(&stack)
  defer q.destroy(&stack)

  make_splitter :: proc(pos: Vec2i) -> ^Splitter {
    s := new(Splitter)
    s.pos = pos

    return s
  }

  q.push_front(&stack, make_splitter(puzzle.start.split_at))

  current := q.back_ptr(&stack)^
  current_pos := current.pos

  //fmt.println("start", current)

  dump_stack :: proc(stack: ^q.Queue(^Splitter)) {
    fmt.printf("STACK::")
    for i := 0; i < q.len(stack^); i += 1 {
      item := q.get(stack, i)
      fmt.printfln("  %v", item)
    }
    fmt.println()
  }

  traverse: for q.len(stack) > 0 {

    next := q.front_ptr(&stack)^

    if next != current {
      current = next
      current_pos = current.pos

      //fmt.println("current", current)

      if current.left != nil {
        //fmt.println("  current.left", current.left)
      }
 
      if current.right != nil {
        //fmt.println("  current.right", current.right)
      }
   }

    if current.left != nil && current.left.done && current.right != nil && current.right.done {
      q.pop_front(&stack)

      free(current.left)
      free(current.right)

      current.left = nil
      current.right = nil

      current.done = true

      //fmt.println("current done", current)

      dump_stack(&stack)
      continue traverse
    }

    index := vec2_to_index(current_pos, puzzle.row_length)

    if index > len(puzzle.data) {
      last := q.pop_front(&stack)
      last.done = true

      //fmt.println("popped", last)

      path_count += 1

      dump_stack(&stack)
      continue traverse
    }

    ch := rune(puzzle.data[index])

    if ch == '^' {
      current.left = make_splitter(current_pos + {-1, 0})
      current.right = make_splitter(current_pos + {1, 0})

      //fmt.println("  splitting left at", current.left)
      //fmt.println("  splitting right at", current.right)

      q.push_front(&stack, current.right)
      q.push_front(&stack, current.left)

      dump_stack(&stack)
      continue traverse
    }

    current_pos += {0, 1}
  }

  return path_count
}

Splitter :: struct {
  pos:   Vec2i,
  done:  bool,
  left:  ^Splitter,
  right: ^Splitter,
}

make_puzzle :: proc(input: string) -> Puzzle_Data {
  pos := find_start(input)

  return {
    data       = input,
    row_length = get_row_length(input),
    start      = {
      split_at = pos,
      start    = pos,
    }
  }
}

find_start :: proc(input: string) -> Vec2i {
  row_length := get_row_length(input)

  pos := Vec2i {0, 0}

  search: for ch, i in input {
    switch ch {
    case ASCII_S:
      pos.x = i
      break search
    case '\n':
      pos.x = 0
      pos.y += 1
    case:
      pos.x += 1
    }
  }

  return pos
}

vec2_to_index :: proc(vec: Vec2i, row_length: int) -> int {
  return vec.x + row_length * vec.y + vec.y
}

get_row_length :: proc(input: string) -> int {
  for ch, i in input {
    (ch == '\n') or_continue

    return i
  }

  return -1
}

Puzzle_Data :: struct {
  data:       string,
  row_length: int,
  start:      Tachyon_Beam,
}

Tachyon_Beam :: struct {
  split_at:   Vec2i,
  start:      Vec2i,
  left_beam:  ^Tachyon_Beam,
  right_beam: ^Tachyon_Beam,
}

Vec2i :: [2]int

ASCII_S :: 83
