"""Maze serialisation module.

Writes the current maze state (grid, entry/exit coordinates, and solution
path) to a plain-text file so it can be reloaded or inspected externally.

Output format
-------------
The file contains the following sections in order:

1. One line per maze row: the cell values concatenated without separators.
2. A blank line.
3. Entry coordinates as ``x,y``.
4. Exit coordinates as ``x,y``.
5. The solution path encoded as a string of cardinal letters
   (e.g. ``"NEESSWN"``).
"""

from mazegen.maze import Maze


def output_file(
    maze: Maze,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    path: str,
) -> None:
    """Serialise *maze* and write it to ``./output_maze.txt``.

    Args:
        maze: The :class:`~mazegen.maze.Maze` instance whose grid is to be
            serialised.
        entry: ``(x, y)`` coordinates of the maze entrance.
        exit_: ``(x, y)`` coordinates of the maze exit.
        path: Solution path as a string of cardinal-direction characters
            (``'N'``, ``'E'``, ``'S'``, ``'W'``).  Pass an empty string
            if no path has been computed.
    """
    lines: list[str] = []

    for row in maze.maze:
        # Join the cell values for this row without any separator.
        row_str = (
            str(row)
            .replace("[", "")
            .replace("]", "")
            .replace("'", "")
            .replace(",", "")
            .replace(" ", "")
        )
        lines.append(row_str)

    lines.append("")
    lines.append(f"{entry[0]},{entry[1]}")
    lines.append(f"{exit_[0]},{exit_[1]}")
    lines.append(path)

    with open("./output_maze.txt", "w") as fd:
        fd.write("\n".join(lines) + "\n")
