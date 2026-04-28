from mazegen.maze import Maze
import interpreter
import output_file
import parser
import sys
from typing import Optional


def make_choice():
    print("\n=== A-Maze-Ing ===")
    print("\n1. Re-generate a new maze using config.txt\n2. Show/Hide path from entry to exit")
    print("3. Choose maze colors\n4. Quit\nChoice? (1-4)")
    choice = sys.stdin.readline().strip()
    if (choice == "1"):
        main()
    elif (choice == "2"):
        print("\nWork in progress, please choose something else")
        make_choice()
    elif (choice == "3"):
        try:
            color_num = int(input("\nPlease choose the color you want between:\n1. White\n2. Red\n3. Green\n4. Blue\n"))
            if (1 <= color_num <= 4):
                main(color_num - 1)
            else:
                print('Invalid color choice. Please retry')
                make_choice()
        except Exception:
            print('Invalid color choice. Please retry')
            make_choice()
    elif (choice != "4"):
        print("\nInvalid input. Please enter a number between 1 and 4")
    return

def transform_list(solution_list: list[tuple[int,int]], width: int) -> list[int]:
    res = []
    for solution in solution_list:
        res.append(solution[1] * width + solution[0] + 1)
    return (res)

def main(color_num: Optional[int] = 0):
    solution_list = [(2,2), (3,2)]
    try:
        maze_config = parser.parse_config("./config.txt")
        try:
            maze = Maze(maze_config.width, maze_config.height, maze_config.entry, maze_config.exit_, maze_config.seed, maze_config.perfect)
            interpreter.interpreter(maze.maze, maze_config.entry[1]*maze_config.width + maze_config.entry[0] + 1, maze_config.exit_[1]*maze_config.width + maze_config.exit_[0] + 1, color_num, transform_list(solution_list, maze_config.width))
            output_file.output_file(maze, maze_config.entry, maze_config.exit_)
        except ValueError as e:
            print(e)
    except ValueError as e:
        print(e)
    make_choice()


if __name__ == "__main__":
    main()