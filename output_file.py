import hunt_kill_maze_algo

def main():
    a = hunt_kill_maze_algo.Maze(15, 15, (0,0), 140)
    a.hunt_kill_algo()
    to_write = ""
    for i in a.maze:
        trad = str(i).replace("[", "")
        trad = trad.replace("]", "")
        trad = trad.replace("'", "")
        trad = trad.replace(",", "")
        trad = trad.replace(" ", "")
        to_write += trad +"\n"

    # need to insert the real start, end and path later
    start = (0,0)
    end = (12, 8)
    start_txt = f"\n{start[0]},{start[1]}"
    end_txt = f"{end[0]},{end[1]}"
    path = "addkd"
    to_write += start_txt + "\n" + end_txt + "\n" + path + "\n"
    with open("./output_maze.txt", "w") as fd:
        fd.write(to_write)
    with open("./output_maze.txt", "r") as fd:
        print(fd.read())


if __name__ == "__main__":
    main()