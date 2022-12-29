import re
import puzzleinput as pi


def problem_2() -> None:
    crate_stacks = []

    for stack_line in pi.crate_stack_init.split("\n"):
        if stack_line == "":
            continue

        container_index = 0
        size = 3
        stack_count = len(stack_line) // 4 + 1

        for pos in range(0, stack_count):
            if pos == len(crate_stacks):
                crate_stacks.append("")

            container = stack_line[container_index:container_index + size]

            if container[0] == "[":
                crate_stacks[pos] = container[1] + crate_stacks[pos]

            container_index += size + 1

    for instruction in pi.crate_stack_instructions.split("\n"):
        result = re.match("move (\d+) from (\d+) to (\d+)", instruction)

        count = int(result.group(1))
        source = int(result.group(2))
        dest = int(result.group(3))

        from_stack: str = crate_stacks[source - 1]
        to_stack: str = crate_stacks[dest - 1]

        to_stack += from_stack[-count:]
        from_stack = from_stack[:-count]

        crate_stacks[source - 1] = from_stack
        crate_stacks[dest - 1] = to_stack

    tops = [container[-1:] for container in crate_stacks]

    answer_message = "Problem 2 : " + "".join(tops)

    print(answer_message)
