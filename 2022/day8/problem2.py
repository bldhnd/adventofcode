import tree
import puzzleinput as pi


def problem_2():
    tree_map: tree.Tree = tree.build_trees(pi.tree_height_map)

    # most_scenic_tree: tree.Tree = None
    most_scenic_tree_score = 0

    current = tree_map

    while True:
        score = current.scenic_score()

        if score > most_scenic_tree_score:
            most_scenic_tree_score = score
            # most_scenic_tree = current

        if current.is_edge("right+down"):
            break

        if current.is_edge("right"):
            current = current.move("down").get_edge("left")
        else:
            current = current.move("right")

    print(f"Problem 2 : {most_scenic_tree_score}")

    # print()
    # tree.print_scenic_trees(tree_map, most_scenic_tree.index)
