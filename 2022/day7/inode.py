import enum


class INodeType(enum.Enum):
    Directory = 1
    File = 2


class INode(object):
    def __init__(self, name: str, type: INodeType) -> None:
        self.name: str = name
        self.type: INodeType = type
        self.size: int = 0
        self.parent: INode = None
        self.children: list[INode] = []

    def __repr__(self) -> str:
        if self.type == INodeType.Directory:
            return f"{self.name} (dir)"
        else:
            return f"{self.name} (file, size={self.size})"


class INodePrintTreeVisitor(object):
    def __init__(self) -> None:
        self.__depth = 0

    def visit(self, node: INode) -> None:
        print("".rjust(self.__depth) + "- " + repr(node))

        self.__depth += 2

        for child in node.children:
            self.visit(child)

        self.__depth -= 2


class INodeDirSizeVisitor(object):

    def get_all_dir_sizes(self, node: INode) -> list[tuple[INode, int]]:
        result = []

        size = self.dir_size(node)

        result.append(size)

        for child in node.children:
            if child.type == INodeType.Directory:
                result += self.get_all_dir_sizes(child)

        return result

    def dir_size(self, node: INode) -> tuple[INode, int]:
        size = sum(
            [file.size for file in node.children if file.type == INodeType.File])

        sub_dir_size = sum([self.dir_size(dir)[1]
                           for dir in node.children if dir.type == INodeType.Directory])

        return (node, size + sub_dir_size)


class INodePrintDirSizeVisitor(INodeDirSizeVisitor):
    def visit(self, node: INode) -> None:
        size = self.dir_size(node)

        print(f"{repr(node)} ({size})")

        for child in node.children:
            if child.type == INodeType.Directory:
                self.visit(child)


def build_inode_from_io(command_io: str) -> INode:
    current: INode = None

    for in_out in command_io.split("\n"):
        if in_out.startswith("$ "):
            # command
            input = in_out[2:].split(" ")
            command = input[0]

            if command == "cd":
                # cd
                name = input[1]

                if name == "..":
                    current = current.parent
                elif name == "/":
                    current = INode(name, INodeType.Directory)
                else:
                    found_dir = [
                        dir for dir in current.children if dir.name == name]

                    directory = INode(
                        name, INodeType.Directory) if not found_dir else found_dir[0]

                    directory.parent = current
                    current = directory
            elif command == "ls":
                # ls
                pass
        else:
            # output
            output = in_out.split(" ")

            if output[0] == "dir":
                # directory name
                name = output[1]

                directory = INode(name, INodeType.Directory)

                current.children.append(directory)
            elif output[0].isdigit():
                # byte size file name
                name = output[1]
                size = int(output[0])

                file = INode(name, INodeType.File)
                file.size = size

                current.children.append(file)

    while current.parent:
        current = current.parent

    return current
