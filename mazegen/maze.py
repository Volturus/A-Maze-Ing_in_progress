import math
import random
from typing import Optional

N, E, S, W = 0, 1, 2, 3

_DX = (0, 1, 0, -1)
_DY = (-1, 0, 1, 0)

_DIR_BIT = (0, 1, 2, 3)

_OPP = (S, W, N, E)

_PATTERN_42 = [
    ["B", "N", "N", "B", "N", "D", "5", "5", "3"],
    ["A", "N", "N", "A", "N", "N", "N", "N", "A"],
    ["C", "5", "5", "2", "N", "9", "5", "5", "6"],
    ["N", "N", "N", "A", "N", "A", "N", "N", "N"],
    ["N", "N", "N", "E", "N", "C", "5", "5", "7"],
]
_PATTERN_MIN_WIDTH = 11
_PATTERN_MIN_HEIGHT = 7


class Maze:
    def __init__(
        self,
        width: int,
        height: int,
        start: tuple[int, int],
        end: tuple[int, int],
        seed: Optional[int] = None,
        perfect: bool = True,
    ) -> None:
        random.seed(seed)
        self.perfect = perfect
        self.maze: list[list[str]] = []
        self.list42: set[tuple[int, int]] = set()
        self._width = width
        self._height = height
        self._exit = end
        self._entry = start
        self._current = start
        self._last = start
        self._create_empty_maze(width, height)

    def _create_empty_maze(self, width: int, height: int) -> None:
        self.maze = [["N"] * width for _ in range(height)]

        if width < _PATTERN_MIN_WIDTH or height < _PATTERN_MIN_HEIGHT:
            print("Maze too small to display the '42' pattern.")
            return

        ox = math.floor(width / 2) - 4
        oy = math.floor(height / 2) - 2

        for dy, row in enumerate(_PATTERN_42):
            for dx, cell in enumerate(row):
                self.maze[oy + dy][ox + dx] = cell
                if cell != "N":
                    if ox + dx == self._entry[0] and oy + dy == self._entry[1]:
                        raise ValueError(f"ENTRY {self._entry} overlaps 42 pattern")
                    if ox + dx == self._exit[0] and oy + dy == self._exit[1]:
                        raise ValueError(f"EXIT {self._exit} overlaps 42 pattern")
                    self.list42.add((ox + dx, oy + dy))
        self.hunt_kill_algo()

    @staticmethod
    def _clear_wall(cell: str, direction: int) -> str:
        val = int(cell, 16) & ~(1 << _DIR_BIT[direction])
        return hex(val)[2:].upper()

    def _open_passage(self, x: int, y: int, direction: int) -> None:
        nx, ny = x + _DX[direction], y + _DY[direction]
        self.maze[y][x] = self._clear_wall(self.maze[y][x], direction)
        self.maze[ny][nx] = self._clear_wall(self.maze[ny][nx], _OPP[direction])

    def _check_surrounding(self, x: int, y: int) -> list[str]:
        result: list[str] = []
        lx, ly = self._last

        for d in (N, E, S, W):
            nx, ny = x + _DX[d], y + _DY[d]

            if not (0 <= nx < self._width and 0 <= ny < self._height):
                result.append("W")
            elif (nx, ny) in self.list42:
                result.append("L")
            elif (nx, ny) == (lx, ly):
                # Open the wall on the previous cell toward the current one.
                self.maze[ly][lx] = self._clear_wall(self.maze[ly][lx], _OPP[d])
                result.append("P")
            else:
                result.append(self.maze[ny][nx])

        return result

    def _hunt(self) -> bool:
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


def main() -> None:
    """Run a small maze and print the raw grid."""
    a = Maze(4, 6, (0, 0), 150)
    a.hunt_kill_algo()
    for row in a.maze:
        print(row)


if __name__ == "__main__":
    main()