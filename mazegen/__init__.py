"""mazegen – reusable maze generation package.

Provides :class:`mazegen.maze.Maze`, a Hunt-and-Kill maze generator that
produces a 2-D hexadecimal wall-bitmask grid, optionally embedding a '42'
pattern at the centre.

Typical usage::

    from mazegen.maze import Maze

    maze = Maze(width=20, height=15, start=(0, 0), end=(19, 14), seed=42)
    print(maze.maze)   # 2-D list of hex strings
"""

from mazegen.maze import Maze

__all__ = ["Maze"]
__version__ = "1.0.0"