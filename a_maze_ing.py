import hunt_kill_maze_algo
import interpreter
import output_file
import parser


def main():
    maze_config = parser.parse_config("./config.txt")
    maze = hunt_kill_maze_algo.Maze(maze_config.width, maze_config.height, maze_config.entry, maze_config.seed)
    maze.hunt_kill_algo()
    interpreter.interpreter(maze.maze, maze_config.entry[1]*maze_config.width + maze_config.entry[0] + 1, maze_config.exit_[1]*maze_config.width + maze_config.exit_[0] + 1)
    output_file.output_file(maze, maze_config.entry, maze_config.exit_)


if __name__ == "__main__":
    main()