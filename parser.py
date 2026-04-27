"""Configuration file parser for the A-Maze-ing maze generator.

Parses and fully validates a KEY=VALUE config file, returning a MazeConfig
dataclass. Raises ValueError with a descriptive message on any error.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class MazeConfig:
    """Holds every validated parameter needed to generate a maze.

    Attributes:
        width: Number of columns (cells).
        height: Number of rows (cells).
        entry: (x, y) coordinates of the maze entrance.
        exit_: (x, y) coordinates of the maze exit.
        output_file: Path to the output file.
        perfect: Whether the maze must be a perfect maze.
        seed: Optional RNG seed for reproducibility.
        algorithm: Optional name of the generation algorithm.
    """

    width: int
    height: int
    entry: tuple[int, int]
    exit_: tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int] = field(default=None)
    algorithm: Optional[str] = field(default=None)

_MANDATORY_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}


def _parse_int(value: str, key: str) -> int:
    """Parse a string as a positive integer.

    Args:
        value: Raw string value from the config file.
        key: Config key name (used in error messages).

    Returns:
        The parsed integer.

    Raises:
        ValueError: If the value is not a strictly positive integer.
    """
    try:
        result = int(value)
    except ValueError:
        raise ValueError(f"{key} must be an integer, got: {value!r}")
    if result <= 0:
        raise ValueError(f"{key} must be > 0, got: {result}")
    return result


def _parse_coord(value: str, key: str) -> tuple[int, int]:
    """Parse a 'x,y' string as a pair of non-negative integers.

    Args:
        value: Raw string value from the config file (expected 'x,y').
        key: Config key name (used in error messages).

    Returns:
        A (x, y) tuple of non-negative integers.

    Raises:
        ValueError: If the format is wrong or values are negative.
    """
    parts = value.split(",")
    if len(parts) != 2:
        raise ValueError(
            f"{key} must be in 'x,y' format, got: {value!r}"
        )
    try:
        x, y = int(parts[0].strip()), int(parts[1].strip())
    except ValueError:
        raise ValueError(
            f"{key} coordinates must be integers, got: {value!r}"
        )
    if x < 0 or y < 0:
        raise ValueError(
            f"{key} coordinates must be >= 0, got: ({x}, {y})"
        )
    return (x, y)


def _parse_bool(value: str, key: str) -> bool:
    """Parse a string as a boolean (True/False, case-insensitive).

    Args:
        value: Raw string value from the config file.
        key: Config key name (used in error messages).

    Returns:
        The parsed boolean.

    Raises:
        ValueError: If the value is neither 'true' nor 'false'.
    """
    lower = value.strip().lower()
    if lower == "true":
        return True
    if lower == "false":
        return False
    raise ValueError(
        f"{key} must be 'True' or 'False', got: {value!r}"
    )


def _check_in_bounds(
    coord: tuple[int, int],
    width: int,
    height: int,
    key: str,
) -> None:
    """Ensure a coordinate lies strictly inside the maze grid.

    Args:
        coord: (x, y) pair to check.
        width: Maze width in cells.
        height: Maze height in cells.
        key: Config key name (used in error messages).

    Raises:
        ValueError: If the coordinate is outside [0, width) x [0, height).
    """
    x, y = coord
    if not (0 <= x < width and 0 <= y < height):
        raise ValueError(
            f"{key} ({x}, {y}) is out of bounds for a "
            f"{width}x{height} maze"
        )

def parse_config(path: str) -> MazeConfig:
    """Read, parse, and fully validate a maze configuration file.

    The file must contain one KEY=VALUE pair per line. Lines starting with
    '#' are treated as comments and ignored. Unknown keys are silently
    accepted as long as all mandatory keys are present.

    Mandatory keys: WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT.
    Optional keys:  SEED (int), ALGORITHM (str).

    Args:
        path: Path to the configuration file.

    Returns:
        A fully validated MazeConfig dataclass.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If any key is missing, malformed, or logically invalid.
    """
    raw: dict[str, str] = {}

    try:
        with open(path, "r", encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, start=1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ValueError(
                        f"Line {lineno}: expected KEY=VALUE, got: {line!r}"
                    )
                key, _, value = line.partition("=")
                key = key.strip().upper()
                value = value.strip()
                if not key:
                    raise ValueError(
                        f"Line {lineno}: empty key in: {line!r}"
                    )
                raw[key] = value
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Configuration file not found: {path!r}"
        )

    missing = _MANDATORY_KEYS - raw.keys()
    if missing:
        raise ValueError(
            f"Missing mandatory key(s): {', '.join(sorted(missing))}"
        )

    width = _parse_int(raw["WIDTH"], "WIDTH")
    height = _parse_int(raw["HEIGHT"], "HEIGHT")
    entry = _parse_coord(raw["ENTRY"], "ENTRY")
    exit_ = _parse_coord(raw["EXIT"], "EXIT")
    output_file = raw["OUTPUT_FILE"]
    perfect = _parse_bool(raw["PERFECT"], "PERFECT")

    if not output_file:
        raise ValueError("OUTPUT_FILE must not be empty")

    _check_in_bounds(entry, width, height, "ENTRY")
    _check_in_bounds(exit_, width, height, "EXIT")

    if entry == exit_:
        raise ValueError(
            f"ENTRY and EXIT must be different cells, both are {entry}"
        )

    seed: Optional[int] = None
    if "SEED" in raw:
        try:
            seed = int(raw["SEED"])
        except ValueError:
            raise ValueError(
                f"SEED must be an integer, got: {raw['SEED']!r}"
            )

    algorithm: Optional[str] = raw.get("ALGORITHM", None)

    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit_=exit_,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
        algorithm=algorithm,
    )