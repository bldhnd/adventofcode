import tree
import puzzleinput as pi


def problem_1():
    tree_map: tree.Tree = tree.build_trees(pi.tree_height_map)

    visible_count = 0
    current = tree_map

    while True:
        visible_count += 1 if current.is_visible() else 0

        if current.is_edge("right+down"):
            break

        if current.is_edge("right"):
            current = current.move("down").get_edge("left")
        else:
            current = current.move("right")

    print(f"Problem 1 : {visible_count}")
