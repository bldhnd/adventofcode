import puzzleinput


class NodeRunner:
    def __init__(self, instructions: str, nodes: dict) -> None:
        self._steps_taken: int = 0
        self._instructions: str = instructions
        self._current_step: int = 0
        self._nodes: dict = nodes
    
    def run_to(self, destination: str) -> int:
        current_node = self._nodes["START"]

        while current_node != destination:
            direction = self.__get_next_direction()

            current_node = self._nodes[current_node][direction]

            self._steps_taken += 1
        
        return self._steps_taken

    def __get_next_direction(self) -> int:
        step = self._instructions[self._current_step]
        
        self._current_step += 1 
        
        if self._current_step >= len(self._instructions):
            self._current_step = 0

        return 0 if step == "L" else 1

    def __repr__(self) -> str:
        return f"{{ steps taken: {self._steps_taken}, current step: {self._instructions[self._current_step]} ({self._current_step}), inst: {self._instructions}\nnodes: {repr(self._nodes)} }}"


def problem_1() -> None:
    def parser(puzzle_input: str) -> NodeRunner:
        pos = 0
        ch = puzzle_input[pos]

        instructions = ""

        while ch != "\n":
            instructions += ch
            pos += 1
            ch = puzzle_input[pos]
        else:
            pos += 2
            ch = puzzle_input[pos]

        nodes = dict()

        while pos < len(puzzle_input):
            node = ""

            while ch != " ":
                node += ch
                pos += 1
                ch = puzzle_input[pos]
            else:
                pos += 4
                ch = puzzle_input[pos]
            
            if "START" not in nodes:
                nodes["START"] = node

            left = right = ""

            while ch != ",":
                left += ch
                pos += 1
                ch = puzzle_input[pos]
            else:
                pos += 2
                ch = puzzle_input[pos]
            
            while ch != ")":
                right += ch
                pos += 1
                ch = puzzle_input[pos]
            
            while ch != "\n" and ch != "":
                pos += 1
                ch = puzzle_input[pos] if pos < len(puzzle_input) else ""
            
            if ch == "\n":
                pos += 1
                ch = puzzle_input[pos]
            
            nodes[node] = (left, right)

        return NodeRunner(instructions, nodes)

    node_runner = parser(puzzleinput.PUZZLE_INPUT)

    steps_taken = node_runner.run_to("ZZZ")

    # 13019
    print(f"Problem 1 steps taken is {steps_taken}")
