import puzzleinput as pi
import inode


def problem_1() -> None:
    root: inode.INode = inode.build_inode_from_io(pi.command_io)

    visitor = inode.INodePrintDirSizeVisitor()

    at_most = 100000

    all_dir_sizes = visitor.get_all_dir_sizes(root)
    total_size = sum([
        dir_size[1] for dir_size in all_dir_sizes if dir_size[1] <= at_most])

    print(f"Problem 1 : {total_size}")
