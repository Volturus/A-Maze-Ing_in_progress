"""Maze generation module using the Hunt-and-Kill algorithm.

This module provides the :class:`Maze` class, which generates a 2-D maze
stored as a grid of hexadecimal wall-bitmask strings.  Each cell's value
encodes which of its four walls are *closed* (bit set) using the following
layout::

    bit 0 (LSB) = North wall closed
    bit 1       = East  wall closed
    bit 2       = South wall closed
    bit 3       = West  wall closed

The generator can optionally embed a decorative '42' pattern at the centre
of the maze and supports both perfect (tree) mazes and imperfect (looped)
mazes.
"""

import math
import random
from typing import Optional

# Cardinal direction indices
N, E, S, W = 0, 1, 2, 3

# Column / row deltas for each direction
_DX = (0, 1, 0, -1)
_DY = (-1, 0, 1, 0)

# Bit index in the wall bitmask for each direction
_DIR_BIT = (0, 1, 2, 3)

# Opposite direction for each cardinal direction
_OPP = (S, W, N, E)

# Pre-defined pattern that renders the number '42' inside the maze.
# Each character is a hexadecimal wall bitmask; 'N' means the cell has
# not yet been visited by the generator.
_PATTERN_42 = [
    ["B", "N", "N", "B", "N", "D", "5", "5", "3"],
    ["A", "N", "N", "A", "N", "N", "N", "N", "A"],
    ["C", "5", "5", "2", "N", "9", "5", "5", "6"],
    ["N", "N", "N", "A", "N", "A", "N", "N", "N"],
    ["N", "N", "N", "E", "N", "C", "5", "5", "7"],
]

# Minimum maze dimensions required to fit the '42' pattern
_PATTERN_MIN_WIDTH = 11
_PATTERN_MIN_HEIGHT = 7


class Maze:
    """A randomly generated maze using the Hunt-and-Kill algorithm.

    The maze is stored in :attr:`maze` as a 2-D list of single
    hexadecimal characters where each character encodes the open/closed
    state of the four walls of that cell (see module docstring for the
    bit layout).

    Attributes:
        perfect (bool): ``True`` if the maze is a perfect (acyclic) maze.
        maze (list[list[str]]): 2-D grid of wall-bitmask strings.
        list42 (set[tuple[int, int]]): Coordinates occupied by the '42'
            pattern (these cells are excluded from further generation).
        display_path (bool): Flag used by the UI to toggle path display.
        path (Optional[list[tuple[int, int]]]): Shortest path from entry
            to exit, populated externally after generation.
        color (int): 1-based colour index used by the renderer.
    """

    def __init__(
        self,
        width: int,
        height: int,
        start: tuple[int, int],
        end: tuple[int, int],
        seed: Optional[int] = None,
        perfect: bool = True,
    ) -> None:
        """Initialise and immediately generate the maze.

        Args:
            width: Number of columns (cells).
            height: Number of rows (cells).
            start: ``(x, y)`` coordinates of the maze entrance.
            end: ``(x, y)`` coordinates of the maze exit.
            seed: Optional integer seed for the random-number generator.
                Pass the same seed to reproduce an identical maze.
            perfect: If ``True`` (default) the maze is a spanning tree
                (no loops).  If ``False``, a small fraction of redundant
                passages are carved to create cycles.

        Raises:
            ValueError: If *start* or *end* overlaps a cell reserved for
                the '42' pattern.
        """
        random.seed(seed)
        self.perfect = perfect
        self.maze: list[list[str]] = []
        self.list42: set[tuple[int, int]] = set()
        self.display_path = False
        self.path: Optional[list[tuple[int, int]]] = None
        self.color = 1
        self._width = width
        self._height = height
        self._exit = end
        self._entry = start
        self._current = start
        self._last = start
        self._create_empty_maze(width, height)

    def _create_empty_maze(self, width: int, height: int) -> None:
        """Initialise the grid, stamp the '42' pattern, and run generation.

        All cells are first set to ``"N"`` (unvisited).  If the maze is
        large enough the '42' pattern is stamped in the centre, then
        :meth:`hunt_kill_algo` carves the actual passages.

        Args:
            width: Number of columns.
            height: Number of rows.

        Raises:
            ValueError: If the entry or exit coordinate coincides with a
                cell belonging to the '42' pattern.
        """
        self.maze = [["N"] * width for _ in range(height)]

        if width < _PATTERN_MIN_WIDTH or height < _PATTERN_MIN_HEIGHT:
            print("Maze too small to display the '42' pattern.")
            self.hunt_kill_algo()
            return

        ox = math.floor(width / 2) - 4
        oy = math.floor(height / 2) - 2

        for dy, row in enumerate(_PATTERN_42):
            for dx, cell in enumerate(row):
                self.maze[oy + dy][ox + dx] = cell
                if cell != "N":
                    if (
                        ox + dx == self._entry[0]
                        and oy + dy == self._entry[1]
                    ):
                        raise ValueError(
                            f"ENTRY {self._entry} overlaps 42 pattern"
                        )
                    if (
                        ox + dx == self._exit[0]
                        and oy + dy == self._exit[1]
                    ):
                        raise ValueError(
                            f"EXIT {self._exit} overlaps 42 pattern"
                        )
                    self.list42.add((ox + dx, oy + dy))
        self.hunt_kill_algo()

    @staticmethod
    def _clear_wall(cell: str, direction: int) -> str:
        """Return a new cell value with the wall in *direction* opened.

        Args:
            cell: Single hexadecimal character representing current walls.
            direction: Direction index (``N``, ``E``, ``S``, or ``W``).

        Returns:
            A new single hexadecimal character with the relevant bit cleared.
        """
        val = int(cell, 16) & ~(1 << _DIR_BIT[direction])
        return hex(val)[2:].upper()

    def _open_passage(self, x: int, y: int, direction: int) -> None:
        """Carve an open passage from cell ``(x, y)`` toward *direction*.

        Both the source cell and the neighbouring cell have their shared
        wall bit cleared so the passage is bidirectional.

        Args:
            x: Column of the source cell.
            y: Row of the source cell.
            direction: Direction of travel (``N``, ``E``, ``S``, or ``W``).
        """
        nx, ny = x + _DX[direction], y + _DY[direction]
        self.maze[y][x] = self._clear_wall(self.maze[y][x], direction)
        self.maze[ny][nx] = self._clear_wall(
            self.maze[ny][nx], _OPP[direction]
        )

    def _check_surrounding(self, x: int, y: int) -> list[str]:
        """Return a four-element list describing the neighbours of ``(x, y)``.

        Each element corresponds to a cardinal direction
        (index 0 = N, 1 = E, 2 = S, 3 = W) and contains one of:

        * ``"W"`` - out-of-bounds (border wall).
        * ``"L"`` - occupied by the '42' pattern.
        * ``"P"`` - the previously visited cell (also opens the reverse wall).
        * The cell's current hex character for any other neighbour.

        When the previous cell is found in a given direction the wall on
        ``_last`` facing back toward ``(x, y)`` is immediately cleared.

        Args:
            x: Column of the cell to inspect.
            y: Row of the cell to inspect.

        Returns:
            List of four status strings, one per cardinal direction.
        """
        result: list[str] = []
        lx, ly = self._last

        for d in (N, E, S, W):
            nx, ny = x + _DX[d], y + _DY[d]

            if not (0 <= nx < self._width and 0 <= ny < self._height):
                result.append("W")
            elif (nx, ny) in self.list42:
                result.append("L")
            elif (nx, ny) == (lx, ly):
                self.maze[ly][lx] = self._clear_wall(
                    self.maze[ly][lx], _OPP[d]
                )
                result.append("P")
            else:
                result.append(self.maze[ny][nx])

        return result

    def _hunt(self) -> bool:
        """Scan the grid for an unvisited cell adjacent to a visited one.

        When such a cell is found :attr:`_current` and :attr:`_last` are
        updated so that :meth:`hunt_kill_algo` can continue carving from
        that position.

        Returns:
            ``True`` if a suitable cell was found; ``False`` if the entire
            grid has been visited (generation is complete).
        """
        for cy in range(self._height):
            for cx in range(self._width):
                if self.maze[cy][cx] != "N":
                    continue

                saved_last = self._last
                self._last = (self._width + 2, self._height + 2)
                neighbours = self._check_surrounding(cx, cy)
                self._last = saved_last

                visited = [
                    d for d in (N, E, S, W)
                    if neighbours[d] not in ("W", "N", "L")
                ]
                if not visited:
                    continue

                self._current = (cx, cy)
                chosen = random.choice(visited)
                self._last = (cx + _DX[chosen], cy + _DY[chosen])
                return True

        return False

    def hunt_kill_algo(self) -> None:
        """Run the Hunt-and-Kill maze generation algorithm.

        Iteratively carves passages from :attr:`_current`, choosing a
        random unvisited neighbour at each step (the *kill* phase).  When
        no unvisited neighbours exist it switches to the *hunt* phase,
        scanning for any unvisited cell that borders a visited one.
        Generation ends when every cell has been visited.

        If :attr:`perfect` is ``False``, :meth:`_add_loops` is called
        afterwards to introduce a small number of redundant passages.
        """
        while True:
            x, y = self._current
            neighbours = self._check_surrounding(x, y)

            walls = 0
            unvisited: list[int] = []
            for d in (N, E, S, W):
                if neighbours[d] != "P":
                    walls |= (1 << _DIR_BIT[d])
                if neighbours[d] == "N":
                    unvisited.append(d)

            self.maze[y][x] = hex(walls)[2:].upper()
            self._last = (x, y)

            if unvisited:
                chosen = random.choice(unvisited)
                self._current = (x + _DX[chosen], y + _DY[chosen])
            elif self._hunt():
                pass
            else:
                break

        if not self.perfect:
            self._add_loops()

    def _add_loops(self, loop_ratio: float = 0.05) -> None:
        """Randomly remove extra walls to create loops in the maze.

        Iterates over every cell and, with probability *loop_ratio*, opens
        the East or South wall if the neighbour is accessible and not part
        of the '42' pattern.  This turns the spanning-tree maze into a
        graph with cycles.

        Args:
            loop_ratio: Probability (0-1) of removing each candidate wall.
                Defaults to ``0.05`` (5 %).
        """
        for y in range(self._height):
            for x in range(self._width):
                if (x, y) in self.list42:
                    continue

                if (
                    x + 1 < self._width
                    and (x + 1, y) not in self.list42
                    and (int(self.maze[y][x], 16) >> _DIR_BIT[E]) & 1
                    and random.random() < loop_ratio
                ):
                    self._open_passage(x, y, E)

                if (
                    y + 1 < self._height
                    and (x, y + 1) not in self.list42
                    and (int(self.maze[y][x], 16) >> _DIR_BIT[S]) & 1
                    and random.random() < loop_ratio
                ):
                    self._open_passage(x, y, S)
