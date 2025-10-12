def dfs_water_jug(max_x, max_y, target):
    stack = []
    visited = set()
    stack.append((0, 0, []))

    while stack:
        x, y, path = stack.pop()

        if (x, y) in visited:
            continue
        visited.add((x, y))

        if x == target or y == target:
            print("Goal reached!")
            for step, rule in path:
                print(f"{step} -> {rule}")
            print(f"Final state: ({x}, {y})")
            return True

        next_moves = [
            ((max_x, y), "Fill Jug X"),
            ((x, max_y), "Fill Jug Y"),
            ((0, y), "Empty Jug X"),
            ((x, 0), "Empty Jug Y"),
            ((x - min(x, max_y - y), y + min(x, max_y - y)), "Pour Jug X → Jug Y"),
            ((x + min(y, max_x - x), y - min(y, max_x - x)), "Pour Jug Y → Jug X")
        ]

        for (new_x, new_y), rule in next_moves:
            if (new_x, new_y) not in visited:
                stack.append((new_x, new_y, path + [((x, y), rule)]))

    print("No solution found.")
    return False


dfs_water_jug(4, 3, 2)
