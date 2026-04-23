import hunt_kill_maze_algo


# 0 =  ┘    └
#        ██  
#      ┐    ┌

# 1 =  ┴────┴ ou ──────
#        ██        ██
#      ┐    ┌    ┐    ┌

# 2 = ┘    ├ ou ┘    │
#       ██ │      ██ │
#     ┐    ├    ┐    │

# 3 = ┴────┼ ou ─────┐
#       ██ │      ██ │
#     ┐    ├    ┐    │   

# 4 = ┘    └ ou ┘    └
#       ██        ██
#     ┬────┬    ──────

# 5 = ┴────┴ ou ──────
#       ██        ██
#     ┬────┬    ──────

# 6 = ┘    ├ ou ┘    │
#       ██ │      ██ │
#     ┬────┼    ─────┘

# 7 = ┴────┼ ou ─────┐
#       ██ │      ██ │
#     ┬────┼    ─────┘

# 8 = ┤    └ ou │    └
#     │ ██      │ ██  
#     ┤    ┌    │    ┌

# 9 = ┼────┴ ou ┌─────
#     │ ██      │ ██ 
#     ┤    ┌    │    ┌

# 10/A = ┤    ├ ou │    │
#        │ ██ │    │ ██ │
#        ┤    ├    │    │

# 11/B = ┼────┼ ou ┌────┐
#        │ ██ │    │ ██ │
#        ┤    ├    │    │

# 12/C = ┤    └ ou │    └
#        │ ██      │ ██ 
#        ┼────┬    └─────

# 13/D = ┼────┴ ou ┌─────
#        │ ██      │ ██ 
#        ┼────┬    └─────

# 14/E = ┤    ├ ou │    │
#        │ ██ │    │ ██ │
#        ┼────┼    └────┘

# 15/F = ┼────┼ ou ┌────┐
#        │ ██ │    │ ██ │
#        ┼────┼    └────┘


def interpreter(trad: list[str]):
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


def interpreter2(maze : list[list], start: int, exit: int):
    count = 0
    couleur = "\033[0m"
    for i in maze:
        for j in i:
            if (j in "04"):
                print("┘    └", end="")
            if (j in "15"):
                print(f"{couleur}──────\033[0m", end="")
            if (j in "26"):
                print("┘    │", end="")
            if (j in "37"):
                print("─────┐", end="")
            if (j in "8C"):
                print("│    └", end="")
            if (j in "9D"):
                print("┌─────", end="")
            if (j in "AE"):
                print("│    │", end="")
            if (j in "BF"):
                print("┌────┐", end="")
        print("")
        for j in i:
            count += 1
            if (count == start):
                couleur = "\033[0;34m"
            elif (count == exit):
                couleur = "\033[0;31m"
            else:
                couleur = "\033[0m"
            if (j in "0145"):
                print(f"  {couleur}██\033[0m  ", end="")
            if (j in "2367"):
                print(f"  {couleur}██\033[0m │", end="")
            if (j in "89CD"):
                print(f"│ {couleur}██\033[0m  ", end="")
            if (j in "ABEF"):
                print(f"│ {couleur}██\033[0m │", end="")
        print("")
        for j in i:
            if (j in "01"):
                print("┐    ┌", end="")
            if (j in "23"):
                print("┐    │", end="")
            if (j in "45"):
                print("──────", end="")
            if (j in "67"):
                print("─────┘", end="")
            if (j in "89"):
                print("│    ┌", end="")
            if (j in "AB"):
                print("│    │", end="")
            if (j in "CD"):
                print("└─────", end="")
            if (j in "EF"):
                print("└────┘", end="")
        print("")


def main():
    a = hunt_kill_maze_algo.Maze(15, 15, (0,0), 140)
    a.hunt_kill_algo()
    for i in a.maze:
        print(i)
    for i in a.maze:
        interpreter(i)
    interpreter2(a.maze, 1, 224)


if __name__ == "__main__":
    main()
