"""Terminal renderer for the A-Maze-ing maze.

Converts the internal hex-bitmask grid produced by :mod:`maze` into a
human-readable three-row-per-cell ASCII/Unicode representation and prints
it to *stdout* using ANSI escape codes for colour.

Each cell is rendered as three lines of six characters:

.. code-block:: text

    top_row    (e.g.  ┘    └  or  ──────)
    middle_row (e.g.    ██    or  │ ██ │)
    bottom_row (e.g.  ┐    ┌  or  └────┘)

The ``██`` block in the middle row is coloured according to the cell's
role: entry (blue), exit (red), path (pink), or default (none).
"""

from typing import Optional

# ---------------------------------------------------------------------------
# Bitmask-to-character mapping reference
# ---------------------------------------------------------------------------
# The hex digit stored in each maze cell encodes four wall bits.
# The comments below show which combinations of top / bottom horizontal
# walls and left / right vertical walls correspond to each glyph group.
#
# 0 / 4  => top open,    bottom open,    no vertical walls
# 1 / 5  => top closed,  bottom open/closed, no vertical walls  (── row)
# 2 / 6  => open top-right corner, right wall present
# 3 / 7  => closed top, right wall present
# 8 / C  => left wall present, open bottom-left
# 9 / D  => left wall + closed top
# A / E  => both vertical walls
# B / F  => both vertical walls + closed top/bottom

# ANSI colour codes
_COLOR_LIST = [
    "\033[0;37m",   # 0 – white
    "\033[0;31m",   # 1 – red
    "\033[0;32m",   # 2 – green
    "\033[0;34m",   # 3 – blue
]
_RESET = "\033[0m"
_COLOR_ENTRY = "\033[0;34m"  # blue  – entry cell
_COLOR_EXIT = "\033[0;31m"  # red   – exit cell
_COLOR_PATH = "\033[38;5;205m"  # pink  – solution path cell


def interpreter(
    maze: list[list[str]],
    start: int,
    exit_: int,
    color_num: int,
    solution: Optional[list[int]] = None,
) -> None:
    """Print a coloured Unicode rendering of *maze* to *stdout*.

    The maze is printed as a grid where every logical cell occupies
    three terminal lines (top wall row, content row, bottom wall row).
    Special cells are highlighted:

    * **Entry** (1-based index *start*) – blue ``██``.
    * **Exit** (1-based index *exit_*) – red ``██``.
    * **Solution path** (indices in *solution*) – pink ``██``.

    Args:
        maze: 2-D grid of single hex-digit strings as produced by
            :class:`maze.Maze`.
        start: 1-based linear index of the entry cell
            (``y * width + x + 1``).
        exit_: 1-based linear index of the exit cell.
        color_num: 0-based index into the colour palette
            (0 = white, 1 = red, 2 = green, 3 = blue).
        solution: Optional list of 1-based linear cell indices that form
            the solution path.  Defaults to an empty list (no path shown).
    """
    if solution is None:
        solution = []

    wall = _COLOR_LIST[color_num]
    count = 0

    for row in maze:
        # ---- top border row ------------------------------------------------
        for cell in row:
            if cell in "04":
                print(f"{wall}┘    └{_RESET}", end="")
            elif cell in "15":
                print(f"{wall}──────{_RESET}", end="")
            elif cell in "26":
                print(f"{wall}┘    │{_RESET}", end="")
            elif cell in "37":
                print(f"{wall}─────┐{_RESET}", end="")
            elif cell in "8C":
                print(f"{wall}│    └{_RESET}", end="")
            elif cell in "9D":
                print(f"{wall}┌─────{_RESET}", end="")
            elif cell in "AE":
                print(f"{wall}│    │{_RESET}", end="")
            elif cell in "BF":
                print(f"{wall}┌────┐{_RESET}", end="")
        print()

        # ---- middle (content) row ------------------------------------------
        for cell in row:
            count += 1
            if count == start:
                spe = _COLOR_ENTRY
            elif count == exit_:
                spe = _COLOR_EXIT
            elif count in solution:
                spe = _COLOR_PATH
            else:
                spe = _RESET

            if cell in "0145":
                print(f"  {spe}██{_RESET}  ", end="")
            elif cell in "2367":
                print(f"  {spe}██ {wall}│{_RESET}", end="")
            elif cell in "89CD":
                print(f"{wall}│ {spe}██{_RESET}  ", end="")
            elif cell in "ABEF":
                print(f"{wall}│ {spe}██ {wall}│{_RESET}", end="")
        print()

        # ---- bottom border row ---------------------------------------------
        for cell in row:
            if cell in "01":
                print(f"{wall}┐    ┌{_RESET}", end="")
            elif cell in "23":
                print(f"{wall}┐    │{_RESET}", end="")
            elif cell in "45":
                print(f"{wall}──────{_RESET}", end="")
            elif cell in "67":
                print(f"{wall}─────┘{_RESET}", end="")
            elif cell in "89":
                print(f"{wall}│    ┌{_RESET}", end="")
            elif cell in "AB":
                print(f"{wall}│    │{_RESET}", end="")
            elif cell in "CD":
                print(f"{wall}└─────{_RESET}", end="")
            elif cell in "EF":
                print(f"{wall}└────┘{_RESET}", end="")
        print()
