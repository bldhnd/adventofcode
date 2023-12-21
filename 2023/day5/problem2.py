from typing import Optional, Union

import puzzleinput


def problem_2() -> None:
    CURRENT_INPUT = puzzleinput.PUZZLE_INPUT
    
    parser = PuzzleParser(CURRENT_INPUT)
    
    # read seeds
    initial_seeds = parser.read_seeds()

    seeds = [(initial_seeds[i], initial_seeds[i + 1]) for i in range(0, len(initial_seeds), 2)]

    parser.next() # skip \n

    while not parser.eof():
        parser.read_map_name()
        parser.next() # skip :
        parser.next() # skip \n

        # these seeds who matched and were updated to the next destination map
        updated_seeds = []

        while parser.last() != '\n' and not parser.eof():
            map_entry = parser.read_map_entry()

            # locations that didn't match yet and we need to check the remaining seed locations
            retry_seeds = []
            
            dst, src, rng = map_entry
            src_end = src + rng - 1

            for seed in seeds:
                seed_start = seed[0]
                seed_end = seed_start + seed[1] - 1

                #    I========I
                # RRR===========>>
                # capture those numbers that start before the start and extend into the source map
                if seed_start < src and seed_end >= src:
                    retry_seeds.append((seed_start, src - seed_start + 1))
                
                #    I========I
                #    S=========RRR*
                # capture those numbers that run past the end of the source map
                if seed_start >= src and seed_start < src_end and seed_end > src_end:
                    dst_idx = seed_start - src
                    new_rng = src_end - seed_start + 1
                    
                    updated_seeds.append((dst + dst_idx, new_rng))
                    retry_seeds.append((src_end + 1, seed_end - src_end))

                #    I========I
                #    S========S
                # capture those numbers that start and end in the source map
                if seed_start >= src and seed_end <= src_end:
                    dst_idx = seed_start - src
                    new_rng = seed_end - seed_start + 1

                    updated_seeds.append((dst + dst_idx, new_rng))
                
                #    I========I
                #  S=X========X=S
                # capture those numbers inside the source map when the seed starts before and ends after source map
                if seed_start <= src and seed_end > src_end:
                    updated_seeds.append((dst, rng))

                #    I========I
                #  S=X=======S
                # capture those numbers that are in the range of the seed start and end
                if seed_start < src and seed_end > src and seed_end < src_end:
                    new_rng = seed_end - src + 1

                    updated_seeds.append((dst, new_rng))

                # didnt fall into source map at all
                if seed_end < src or seed_start > src_end:
                    retry_seeds.append(seed)

            seeds = retry_seeds
        
        seeds += updated_seeds

        parser.next()
    
    print(f"Problem 2 location is {min([x[0] for x in seeds])}")


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
    

# if seed_start < src and seed_end >= src and seed_end <= src_end:
#                     # starting seed is less than map entry start but range extends into range of source map entry
#                     new_rng = rng - (rng - seed[1])
#                     org_seed_new_rng = src - seed_start

#                     updated_seeds.append((dst, new_rng))
#                     updated_seeds.append((seed_start, org_seed_new_rng))
#                 elif seed_start >= src and seed_start <= src_end and seed_end > src_end:
#                     # starting seed range matches but end goes past map entry source range
#                     dst_idx = abs(seed_start - src)
#                     dst_rng = rng - dst_idx
#                     org_seed_new_rng = seed_end - src_end

#                     updated_seeds.append((dst + dst_idx, dst_rng))
#                     updated_seeds.append((src_end, org_seed_new_rng))
#                 elif seed_start < src and seed_end > src_end:
#                     updated_seeds.append((seed_start, src - seed_start))
#                     updated_seeds.append((src_end, seed_end - src_end))
#                     updated_seeds.append((dst, rng))
#                 elif seed_start >= src and seed_end <= src_end:
#                     # every number matches
#                     dst_idx = seed_start - src
#                     updated_seeds.append((dst + dst_idx, seed[1]))
#                 else:
#                     updated_seeds.append(seed)