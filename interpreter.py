import hunt_kill_maze_algo

def interpreter(trad: str):
    for i in trad:
        if (i in "02468ACE"):
            print("|  |", end="")
        elif (i in "13579BDF"):
            print("|--|", end="")
    print("")
    for i in trad:
        if (i in "0145"):
            print("    ", end="")
        elif (i in "ABEF"):
            print("|  |", end="")
        elif (i in "89CD"):
            print("|   ", end="")
        elif (i in "2367"):
            print("   |", end="")
    print("")
    for i in trad:
        if (i in "012389AB"):
            print("|  |", end="")
        elif (i in "4567CDEF"):
            print("|--|", end="")
    print("")


def main():
    a = hunt_kill_maze_algo.Maze(10, 10, (0,0), 140)
    a.hunt_kill_algo()
    for i in a.maze:
        print(i)
    for i in a.maze:
        interpreter(i)


if __name__ == "__main__":
    main()
