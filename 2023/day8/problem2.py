import math
import puzzleinput


class Node:
    def __init__(self, label: str) -> None:
        self.label: str = label
        self.left: 'Node' = None
        self.right: 'Node' = None
        self.is_start: bool = label.endswith("A")
        self.is_finish: bool = label.endswith("Z")
        self.last_step: str = ""
        self.step_count: int = 0
        self.step_index: int = 0
    
    def step(self, direction: str, step_index: int) -> None:
        self.step_count += 1
        self.step_index = step_index
        self.last_step = direction

    def __repr__(self) -> str:
        repr = self.label

        if self.last_step:
            repr += f" (last: {self.last_step}, step index: {self.step_index}, stepped {self.step_count})"
        
        return repr

def problem_2() -> None:
    def get_node_name(node_line: str) -> str:
        return node_line[0:3]

    def get_left_node(node_line: str) -> str:
        return node_line[7:10]

    def get_right_node(node_line: str) -> str:
        return node_line[12:15]

    def make_nodes(node_lines: list[str]) -> list[Node]:
        nodes_map = dict()
        start_nodes = []
        
        for node_line in node_lines:
            node_name = get_node_name(node_line)

            if node_name not in nodes_map:
                nodes_map[node_name] = Node(node_name)
                        
            node: Node = nodes_map.get(node_name)

            left_node_name = get_left_node(node_line)
            
            if left_node_name not in nodes_map:
                nodes_map[left_node_name] = Node(left_node_name)

            node.left = nodes_map[left_node_name]

            right_node_name = get_right_node(node_line)

            if right_node_name not in nodes_map:
                nodes_map[right_node_name] = Node(right_node_name)

            node.right = nodes_map[right_node_name]

            if node.is_start:
                start_nodes.append(node)
        
        return start_nodes

    data = puzzleinput.PUZZLE_INPUT.split("\n")

    instructions = data[0]
    inst_len = len(instructions)

    total = 0
    inst_index = 0
    steps_taken = 0

    nodes = make_nodes(data[2:])

    all_steps_taken = []

    for node in nodes:
        current: Node = node
        inst_index = 0

        while not current.is_finish:
            direction = instructions[inst_index]

            current = current.left if direction == "L" else current.right

            current.step(direction, inst_index)
            
            inst_index += 1

            if inst_index == inst_len:
                inst_index = 0
            
            steps_taken += 1
        
        all_steps_taken.append(steps_taken)
        steps_taken = 0

    def lcm(a, b) -> int:
        return (a * b) // math.gcd(a, b)

    while len(all_steps_taken) != 0:
        current = all_steps_taken.pop()
        
        if len(all_steps_taken) == 0:
            total = current
        else:
            next = all_steps_taken.pop()
            all_steps_taken.append(lcm(current, next))
    
    # 13524038372771
    print(f"Problem 2 steps taken is {total}")
