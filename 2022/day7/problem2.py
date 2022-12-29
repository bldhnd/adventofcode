import puzzleinput as pi
import inode


def problem_2() -> None:
    root: inode.INode = inode.build_inode_from_io(pi.command_io)

    visitor = inode.INodePrintDirSizeVisitor()

    total_disk_space = 70000000
    free_up_at_least = 30000000

    _, total_used_space = visitor.dir_size(root)
    all_dir_sizes = visitor.get_all_dir_sizes(root)

    total_unused_space = total_disk_space - total_used_space
    # total_needed_space = free_up_at_least - total_unused_space

#     print(f"""
# total disk space: {total_disk_space}
# total used space: {total_used_space}
# total unused space: {total_unused_space}
# total needed space: {total_needed_space}
# """)

    total_size = 0
    dir_node: inode.INode = None

    for node, size in all_dir_sizes:
        new_total_unused_space = size + total_unused_space

        if new_total_unused_space >= free_up_at_least:
            if total_size > size or total_size == 0:
                dir_node = node
                total_size = size

    print(f"Problem 2 : {dir_node} {total_size}")
