from typing import Optional, Union

import puzzleinput


def problem_1() -> None:
    CURRENT_INPUT = puzzleinput.PUZZLE_INPUT
    
    parser = PuzzleParser(CURRENT_INPUT)
    
    # read seeds
    seeds = parser.read_seeds()

    parser.next()

    while not parser.eof():
        parser.read_map_name()
        parser.next() # skip :
        parser.next() # skip \n

        status_map = [False for _ in seeds]

        while parser.last() != '\n' and not parser.eof():
            if all(status_map):
                break
            
            map_entry = parser.read_map_entry()

            for seed_idx, seed in enumerate(seeds):
                if status_map[seed_idx]:
                    continue

                dst, src, rng = map_entry

                src_end = src + rng - 1

                if seed >= src and seed <= src_end:
                    idx = abs(src - seed)
                    
                    seeds[seed_idx] = dst + idx
                    status_map[seed_idx] = True
    
    print(f"Problem 1 location is {min(seeds)}")


class PuzzleParser:
    def __init__(self, input: str) -> None:
        self.pos: int = -1
        self.current: str = ''
        self.length: int = len(input)
        self.input: str = input
    
    def eof(self) -> bool:
        return self.pos == self.length

    def last(self) -> str:
        return self.input[self.pos] if not self.eof() else ''
    
    def next(self) -> str:
        if self.pos < self.length:
            self.pos += 1
            return self.last()
        
        return ''

    def read_seeds(self) -> list[int]:
        seeds = []

        while self.next() != ' ':
            pass

        while self.next() != '\n':
            seed = self.read_int()
            seeds.append(seed)

        return seeds

    def read_int(self) -> Optional[Union[int, None]]:
        number = ''

        while self.last().isnumeric():
            number += self.last()
            self.next()
        
        return int(number) if number != '' else ''

    def read_map_name(self) -> str:
        map_name = ''

        while self.last() != ':':
            map_name += self.last()
            self.next()

        return map_name

    def read_map_entry(self) -> tuple[int, int, int]:
        dest = self.read_int()
        self.next()
        src = self.read_int()
        self.next()
        range = self.read_int()
        self.next()

        return (dest, src, range)