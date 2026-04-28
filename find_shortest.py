import interpreter


def check_ways(maze: list[list], coords: tuple[int, int], previous_coords: list[tuple[int, int]]) -> str:
    NESW = [0,0,0,0]

    if (coords[1] != 0):
        if (maze[coords[1] - 1][coords[0]] in "012389AB" and (coords[0], coords[1] - 1) not in previous_coords):
            NESW[0] = 1
    if (coords[0] != len(maze[coords[1]]) - 1):
        if (maze[coords[1]][coords[0] + 1] in "01234567" and (coords[0] + 1, coords[1]) not in previous_coords):
            NESW[1] = 1
    if (coords[1] != len(maze) - 1):
        if (maze[coords[1] + 1][coords[0]] in "02468ACE") and (coords[0], coords[1] + 1) not in previous_coords:
            NESW[2] = 1
    if (coords[0] != 0):
        if (maze[coords[1]][coords[0] - 1] in "014589CD") and (coords[0] - 1, coords[1]) not in previous_coords:
            NESW[3] = 1
    return NESW


def walk_indiv_path(maze: int, current_coords: tuple[int, int], previous_coords: list[tuple[int, int]]) -> list[tuple[int,int]]:
    NESW = check_ways(maze, current_coords, previous_coords)
    paths = []
    if (NESW[0] == 1):
        paths += [(current_coords[0], current_coords[1] - 1)]
    if (NESW[1] == 1):
        paths += [(current_coords[0] + 1, current_coords[1])]
    if (NESW[2] == 1):
        paths += [(current_coords[0], current_coords[1] + 1)]
    if (NESW[3] == 1):
        paths += [(current_coords[0] - 1, current_coords[1])]
    # print("#######", paths)
    return paths


def find_shortest(maze: list[list], entry: tuple[int,int], exit: tuple[int,int]) -> list[tuple[int, int]]:
    maze_paths = []
    current_coords_mul = [entry]
    new_coords = []
    passing = 0
    test = 0
    previous_coords = []
    while (exit not in current_coords_mul):
    # for x in range(21):
        num_new_path = 0
        num_suppr = -1
        for i in range(len(current_coords_mul)):
            if (walk_indiv_path(maze, current_coords_mul[i], previous_coords) != []):
                # num_suppr = -1
                new_coords += walk_indiv_path(maze, current_coords_mul[i], previous_coords)
                # if (x == 13):
                #     print("\n\n", i+num_new_path, current_coords_mul, "\n\n")
                # print("#######", num_new_path)
                if (maze_paths != []):
                    current_maze_path = maze_paths[i+num_new_path]
                else:
                    test = 1
                new_maze_path = []
                for j in range(passing, len(new_coords)):
                    if (test == 1):
                        new_maze_path += [[new_coords[j]]]
                    else:
                        # print(current_maze_path)
                        new_maze_path += [current_maze_path + [new_coords[j]]]
                if (new_maze_path != []):
                    maze_paths = maze_paths[:i+num_new_path] + new_maze_path + maze_paths[i+num_new_path+1:]
                num_new_path += len(new_coords) - 1 - passing
                for j in range(passing, len(new_coords)):
                    passing += 1
            else:
                # print("@@@-----------------------------------------------------------------------------------------------")
                num_new_path -= 1
                num_suppr += 1
                # print(i, len(maze_paths), len(current_coords_mul), num_suppr)
                maze_paths.pop(i - num_suppr)
        passing = 0
        previous_coords = current_coords_mul
        current_coords_mul = new_coords
        new_coords = []
        test = 0
        # for i in maze_paths:
        #     print("!!!", i)
        # print("!!!!!", current_coords_mul)
        # print("\n")
    # print("\n\n\n", current_coords_mul, "\n", maze_paths)
    for i in maze_paths:
        if exit in i:
            return i
