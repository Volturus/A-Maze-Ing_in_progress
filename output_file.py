def output_file(maze: list[list], entry: tuple[int, int], exit: tuple[int, int]):
    to_write = ""
    for i in maze.maze:
        trad = str(i).replace("[", "")
        trad = trad.replace("]", "")
        trad = trad.replace("'", "")
        trad = trad.replace(",", "")
        trad = trad.replace(" ", "")
        to_write += trad +"\n"

    # need to insert the real path later
    start_txt = f"\n{entry[0]},{entry[1]}"
    end_txt = f"{exit[0]},{exit[1]}"
    path = "addkd"
    to_write += start_txt + "\n" + end_txt + "\n" + path + "\n"
    with open("./output_maze.txt", "w") as fd:
        fd.write(to_write)


if __name__ == "__main__":
    output_file()