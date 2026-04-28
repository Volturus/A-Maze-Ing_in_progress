"""Entry point and interactive menu for A-Maze-ing.

Usage::

    python3 a_maze_ing.py <path_to_config>

Where ``<path_to_config>`` is a maze configuration file as described in
:mod:`parser`.

The program generates a maze, displays it in the terminal, and then
presents a simple interactive menu that lets the user:

1. Re-generate a new maze using the same config file.
2. Toggle display of the shortest path from entry to exit.
3. Change the wall render colour.
4. Quit.
"""

import sys
from typing import Optional

import find_shortest
import interpreter
import output_file
import parser
from mazegen.maze import Maze

current_maze: Optional[Maze] = None
maze_config: Optional[parser.MazeConfig] = None


def transform_list(
    solution_list: list[tuple[int, int]],
    width: int,
) -> list[int]:
    """Convert a list of ``(x, y)`` path coordinates to 1-based cell indices.

    The interpreter uses a flat 1-based index (``y * width + x + 1``) to
    identify highlighted cells, so the BFS path must be converted before
    being passed to :func:`interpreter.interpreter`.

    Args:
        solution_list: Ordered list of ``(x, y)`` coordinates forming the
            solution path.
        width: Maze width in cells (used to compute the linear index).

    Returns:
        List of 1-based integer indices corresponding to each path cell.
    """
    return [sol[1] * width + sol[0] + 1 for sol in solution_list]


def trad_in_letters(sol: list[tuple[int, int]]) -> str:
    """Encode a coordinate path as a string of cardinal-direction letters.

    Consecutive ``(x, y)`` pairs are compared to determine the direction
    of movement.  The result is a compact string such as ``"NEESSWN"``
    used by :func:`output_file.output_file`.

    Args:
        sol: Ordered list of ``(x, y)`` coordinates, e.g. as returned by
            :func:`find_shortest.find_shortest`.

    Returns:
        String of direction characters (``'N'``, ``'E'``, ``'S'``, ``'W'``).
        Returns an empty string if *sol* has fewer than two elements.
    """
    text = ""
    for i in range(len(sol) - 1):
        cx, cy = sol[i]
        nx, ny = sol[i + 1]
        if (nx, ny) == (cx, cy - 1):
            text += "N"
        elif (nx, ny) == (cx + 1, cy):
            text += "E"
        elif (nx, ny) == (cx, cy + 1):
            text += "S"
        elif (nx, ny) == (cx - 1, cy):
            text += "W"
    return text


def regen_maze() -> None:
    """Generate a new maze from the current :data:`maze_config`.

    Creates a fresh :class:`~mazegen.maze.Maze` instance, computes the
    shortest path from entry to exit, and writes the serialised maze to
    the output file specified in the config.

    Raises:
        ValueError: If the entry or exit position overlaps the '42' pattern.
    """
    global current_maze
    assert maze_config is not None, (
        "maze_config must be set before calling regen_maze"
    )

    current_maze = Maze(
        maze_config.width,
        maze_config.height,
        maze_config.entry,
        maze_config.exit_,
        maze_config.seed,
        maze_config.perfect,
    )
    current_maze.path = find_shortest.find_shortest(
        current_maze.maze,
        maze_config.entry,
        maze_config.exit_,
    )
    output_file.output_file(
        current_maze,
        maze_config.entry,
        maze_config.exit_,
        trad_in_letters(current_maze.path),
    )


def display_maze(
    color_num: int = 0,
    solution_list: Optional[list[int]] = None,
) -> None:
    """Render the current maze to the terminal.

    Delegates to :func:`interpreter.interpreter` after computing the
    1-based linear indices for entry and exit from :data:`maze_config`.

    Args:
        color_num: 0-based colour index (0 = white, 1 = red, 2 = green,
            3 = blue).  Defaults to ``0`` (white).
        solution_list: Optional list of 1-based cell indices to highlight
            as the solution path.  Defaults to no path shown.
    """
    if solution_list is None:
        solution_list = []
    assert maze_config is not None
    assert current_maze is not None

    num_entry = (
        maze_config.entry[1] * maze_config.width + maze_config.entry[0] + 1
    )
    num_exit = (
        maze_config.exit_[1] * maze_config.width + maze_config.exit_[0] + 1
    )
    interpreter.interpreter(
        current_maze.maze,
        num_entry,
        num_exit,
        color_num,
        solution_list,
    )


def _display_current() -> None:
    """Re-render the maze, respecting the current path-visibility flag."""
    assert current_maze is not None
    if current_maze.display_path and current_maze.path is not None:
        display_maze(
            current_maze.color - 1,
            transform_list(current_maze.path, current_maze._width),
        )
    else:
        display_maze(current_maze.color - 1)


def make_choice() -> None:
    """Display the interactive menu and handle one iteration of user input.

    Reads a single line from *stdin* and dispatches to the appropriate
    action.  The function calls itself recursively until the user chooses
    to quit (option ``4``).
    """
    assert current_maze is not None

    print("\n=== A-Maze-Ing ===")
    print(
        "\n1. Re-generate a new maze using config.txt\n"
        "2. Show/Hide path from entry to exit\n"
        "3. Choose maze colors\n"
        "4. Quit\n"
        "Choice? (1-4)"
    )
    choice = sys.stdin.readline().strip()

    if choice == "1":
        try:
            regen_maze()
            _display_current()
        except ValueError as exc:
            print(exc)
        make_choice()

    elif choice == "2":
        current_maze.display_path = not current_maze.display_path
        _display_current()
        make_choice()

    elif choice == "3":
        try:
            color = int(
                input(
                    "\nPlease choose the color you want between:"
                    "\n1. White\n2. Red\n3. Green\n4. Blue\n"
                )
            )
            if 1 <= color <= 4:
                current_maze.color = color
                _display_current()
                make_choice()
            else:
                print("Invalid color choice. Please retry")
                make_choice()
        except (ValueError, EOFError):
            print("Invalid color choice. Please retry")
            make_choice()

    elif choice != "4":
        print("\nInvalid input. Please enter a number between 1 and 4")
        make_choice()


def main() -> None:
    """Parse CLI arguments, generate the initial maze, and start the menu.

    Expects exactly one positional argument: the path to a configuration
    file.  Prints a usage message and returns early if the argument count
    is wrong or if the config file is missing or invalid.
    """
    global maze_config

    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py pathtofile")
        return

    try:
        maze_config = parser.parse_config(sys.argv[1])
    except (ValueError, FileNotFoundError) as exc:
        print(exc)
        return

    try:
        regen_maze()
        _display_current()
    except ValueError as exc:
        print(exc)

    make_choice()


if __name__ == "__main__":
    main()
