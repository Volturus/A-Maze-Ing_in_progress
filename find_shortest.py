"""Shortest-path finder for the A-Maze-ing maze.

Uses Breadth-First Search (BFS), which guarantees the shortest path
in an unweighted grid.  Wall passability is determined by reading the
source cell's own wall bits, not the neighbour's value.

Cell bit layout (matching the Hunt-and-Kill generation algorithm):

.. code-block:: text

    bit 0 (LSB) = North wall closed
    bit 1       = East  wall closed
    bit 2       = South wall closed
    bit 3       = West  wall closed

A set bit means the wall is closed (cannot pass); a clear bit means open.
"""

from collections import deque

# (dx, dy, wall_bit) for each of the four cardinal directions.
# If the corresponding bit of the *source* cell is 0 (wall open), the move
# is allowed.
_DIRECTIONS = [
    (0, -1, 0),   # North: dy=-1, check bit 0
    (1,  0, 1),   # East:  dx=+1, check bit 1
    (0,  1, 2),   # South: dy=+1, check bit 2
    (-1, 0, 3),   # West:  dx=-1, check bit 3
]


def _can_move(
    maze: list[list[str]],
    x: int,
    y: int,
    direction: int,
) -> bool:
    """Return ``True`` if the wall in *direction* from ``(x, y)`` is open.

    Checks the wall bit of the *source* cell rather than the neighbour so
    that special pattern cells (which may store non-standard values) are
    handled correctly.

    Args:
        maze: 2-D grid of single hex-digit strings.
        x: Column of the source cell.
        y: Row of the source cell.
        direction: 0 = N, 1 = E, 2 = S, 3 = W.

    Returns:
        ``True`` if the wall bit is 0 (open) and the neighbour lies within
        the grid bounds.
    """
    dx, dy, bit = _DIRECTIONS[direction]
    nx, ny = x + dx, y + dy
    height = len(maze)
    width = len(maze[0])
    if not (0 <= nx < width and 0 <= ny < height):
        return False
    return not (int(maze[y][x], 16) >> bit) & 1


def find_shortest(
    maze: list[list[str]],
    entry: tuple[int, int],
    exit_: tuple[int, int],
) -> list[tuple[int, int]]:
    """Find the shortest path from *entry* to *exit_* using BFS.

    BFS on an unweighted grid guarantees that the first time *exit_* is
    reached it is via the fewest possible steps.  Each queue item carries
    the full path taken so far to avoid a separate parent-map reconstruction.

    Args:
        maze: 2-D grid of single hex-digit strings where each character
            encodes the closed walls of that cell as a bitmask.
        entry: ``(x, y)`` coordinates of the starting cell.
        exit_: ``(x, y)`` coordinates of the target cell.

    Returns:
        A list of ``(x, y)`` tuples representing the shortest path from
        *entry* to *exit_* inclusive.  Returns an empty list if no path
        exists.
    """
    queue: deque[list[tuple[int, int]]] = deque()
    queue.append([entry])
    visited: set[tuple[int, int]] = {entry}

    while queue:
        path = queue.popleft()
        x, y = path[-1]

        if (x, y) == exit_:
            return path

        for direction in range(4):
            dx, dy, _ = _DIRECTIONS[direction]
            nx, ny = x + dx, y + dy
            neighbour = (nx, ny)

            if neighbour not in visited and _can_move(maze, x, y, direction):
                visited.add(neighbour)
                queue.append(path + [neighbour])

    return []
