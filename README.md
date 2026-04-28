*This project has been created as part of the 42 curriculum by \<login1\>[, \<login2\>].*

---

# A-Maze-ing

## Description

A-Maze-ing is a terminal maze generator and solver written in Python 3. The
program reads a plain-text configuration file, generates a random maze using the
**Hunt-and-Kill** algorithm, and renders it directly in the terminal with Unicode
box-drawing characters and ANSI colour codes.

Key features:

- Every maze embeds a decorative **"42"** pattern at its centre (for mazes large
  enough to hold it: width ≥ 11, height ≥ 7).
- The shortest path from entry to exit is computed with **Breadth-First Search
  (BFS)** and can be toggled on or off at runtime.
- Mazes can be either *perfect* (single path between any two cells) or *imperfect*
  (with extra loops).
- A fixed seed produces a fully reproducible maze.
- After each generation the maze is serialised to a plain-text output file using a
  hexadecimal wall-bitmask format.
- The maze generation logic is packaged as a standalone, pip-installable **Poetry**
  package (`mazegen`) located in `mazegen_pkg/`.

---

## Instructions

### Requirements

- Python 3.10 or later
- [Poetry](https://python-poetry.org/docs/#installation) — dependency and
  package manager

Install Poetry if not already available:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Project structure

```
.
├── a_maze_ing.py          # Entry point and interactive menu
├── find_shortest.py       # BFS shortest-path solver
├── interpreter.py         # Terminal renderer (Unicode + ANSI colours)
├── output_file.py         # Maze serialiser → output_maze.txt
├── parser.py              # Config-file parser and validator
├── pyproject.toml         # Top-level Poetry project (dev tools + mazegen dep)
├── Makefile               # Automation (install / run / debug / lint / clean)
├── config.txt             # Default configuration file
├── README.md              # This file
└── mazegen_pkg/           # Standalone reusable package
    ├── pyproject.toml     # Package Poetry metadata
    ├── README.md          # Package-level documentation
    └── mazegen/
        ├── __init__.py
        └── maze.py        # Maze class (Hunt-and-Kill algorithm)
```

### Build and install

```bash
make install   # builds the mazegen .whl then runs `poetry install`
```

This single command:
1. Runs `poetry build` inside `mazegen_pkg/`, producing
   `mazegen_pkg/dist/mazegen-1.0.0-py3-none-any.whl` (and a `.tar.gz`).
2. Runs `poetry install` at the project root, which installs `mazegen` from
   the local wheel **and** all dev dependencies (`flake8`, `mypy`) into
   Poetry's managed virtual environment.

To build the wheel alone without installing:

```bash
make build
```

### Running

```bash
make run
# or, manually inside the Poetry environment:
poetry run python3 a_maze_ing.py config.txt
```

`config.txt` can be replaced with any valid configuration file path.

### Debugging

```bash
make debug
# equivalent to:
poetry run python3 -m pdb a_maze_ing.py config.txt
```

### Linting

```bash
make lint          # flake8 + mypy (standard subject flags)
make lint-strict   # flake8 + mypy --strict
```

The mypy flags used by `make lint` are exactly those required by the subject:
`--warn-return-any --warn-unused-ignores --ignore-missing-imports
--disallow-untyped-defs --check-untyped-defs`.

### Cleaning

```bash
make clean    # removes __pycache__, .mypy_cache, *.pyc, *.pyo
make fclean   # also removes mazegen_pkg/dist/ and poetry.lock files
```

---

## Configuration file

The configuration file uses one `KEY=VALUE` pair per line.
Lines beginning with `#` are treated as comments and ignored.

### Mandatory keys

| Key           | Type          | Description                             | Example                |
|---------------|---------------|-----------------------------------------|------------------------|
| `WIDTH`       | `int > 0`     | Number of columns (cells)               | `WIDTH=20`             |
| `HEIGHT`      | `int > 0`     | Number of rows (cells)                  | `HEIGHT=15`            |
| `ENTRY`       | `x,y`         | Entry cell coordinates (0-based)        | `ENTRY=0,0`            |
| `EXIT`        | `x,y`         | Exit cell coordinates (0-based)         | `EXIT=19,14`           |
| `OUTPUT_FILE` | string        | Path for the serialised maze output     | `OUTPUT_FILE=maze.txt` |
| `PERFECT`     | `True`/`False`| `True` = no loops; `False` = with loops | `PERFECT=True`         |

### Optional keys

| Key         | Type   | Description                                    | Example        |
|-------------|--------|------------------------------------------------|----------------|
| `SEED`      | int    | RNG seed for reproducible mazes                | `SEED=42`      |
| `ALGORITHM` | string | Generation algorithm name (informational only) | `ALGORITHM=hk` |

### Example `config.txt`

```ini
# A-Maze-ing default configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=output_maze.txt
PERFECT=True
SEED=42
```

---

## Output file format

After each generation, `OUTPUT_FILE` is written with the following layout:

```
<row 0 cell values, no separators>
<row 1 cell values, no separators>
...
<row N-1 cell values, no separators>
                              ← blank line
<entry_x>,<entry_y>
<exit_x>,<exit_y>
<solution path as cardinal letters, e.g. NEESSWWN>
```

Each cell is encoded as a single hexadecimal digit where each bit indicates
whether the corresponding wall is **closed** (1) or open (0):

| Bit     | Direction |
|---------|-----------|
| 0 (LSB) | North     |
| 1       | East      |
| 2       | South     |
| 3       | West      |

Example: `A` (binary `1010`) → East and West walls are closed.

---

## Generation algorithm

### Choice: Hunt-and-Kill

The maze is generated by the **Hunt-and-Kill** algorithm, a depth-first random
walk with a systematic scan phase:

1. **Kill phase** — from the current cell, move to a random *unvisited* neighbour,
   carving a passage. Repeat until no unvisited neighbours remain.
2. **Hunt phase** — scan the grid row-by-row for any unvisited cell adjacent to at
   least one visited cell. Connect them and restart the kill phase from there.
3. Repeat until every cell has been visited.

For imperfect mazes (`PERFECT=False`) a 5 % random wall-removal pass runs
afterwards, introducing cycles.

### Why Hunt-and-Kill?

- **Simplicity** — easy to implement correctly and to explain during peer
  evaluation.
- **Perfect mazes by construction** — the spanning-tree property arises naturally,
  with no extra bookkeeping.
- **Good texture** — produces a healthy mix of long corridors and branching,
  avoiding the "river" effect of pure recursive backtracking.
- **Seed reproducibility** — the only randomness comes from Python's `random`
  module; one seed call at construction makes every maze exactly reproducible.

---

## Reusable module (`mazegen`)

The maze generation logic is isolated inside `mazegen_pkg/` as a standalone
**Poetry** package that can be built and installed independently.

### Building the wheel

```bash
make build
# or manually:
cd mazegen_pkg && poetry build
# → mazegen_pkg/dist/mazegen-1.0.0-py3-none-any.whl
#   mazegen_pkg/dist/mazegen-1.0.0.tar.gz
```

### Installing from the wheel

```bash
pip install mazegen_pkg/dist/mazegen-1.0.0-py3-none-any.whl
# or with pipx for isolation:
pipx install mazegen_pkg/dist/mazegen-1.0.0-py3-none-any.whl
```

### What is reusable

The `mazegen.maze.Maze` class encapsulates the entire Hunt-and-Kill pipeline and
has **zero dependency** on the renderer, parser, or output writer — it can be
dropped into any project that only needs maze generation.

After instantiation it exposes:

| Attribute  | Type                              | Description                            |
|------------|-----------------------------------|----------------------------------------|
| `maze`     | `list[list[str]]`                 | 2-D grid of single hex-digit strings   |
| `list42`   | `set[tuple[int, int]]`            | Cells reserved by the '42' pattern     |
| `path`     | `Optional[list[tuple[int, int]]]` | Set externally with the solution path  |
| `perfect`  | `bool`                            | Whether the maze is a spanning tree    |

### Basic usage example

```python
from mazegen.maze import Maze

# Generate a 20×15 perfect maze, reproducible with seed 42.
maze = Maze(
    width=20,
    height=15,
    start=(0, 0),
    end=(19, 14),
    seed=42,
    perfect=True,
)

# Access the raw grid.
print(maze.maze[0])  # first row, e.g. ['9', 'C', '1', ...]

# Find and store the shortest path (BFS).
from find_shortest import find_shortest
maze.path = find_shortest(maze.maze, (0, 0), (19, 14))
print(maze.path)  # [(0, 0), (1, 0), ...]
```

### Constructor parameters

| Parameter | Type              | Default | Description                 |
|-----------|-------------------|---------|-----------------------------|
| `width`   | `int`             | —       | Number of columns           |
| `height`  | `int`             | —       | Number of rows              |
| `start`   | `tuple[int, int]` | —       | Entry cell `(x, y)`         |
| `end`     | `tuple[int, int]` | —       | Exit cell `(x, y)`          |
| `seed`    | `int` or `None`   | `None`  | RNG seed; `None` = random   |
| `perfect` | `bool`            | `True`  | `False` adds loops          |

---

## Interactive menu

Once the maze is displayed the program enters an interactive loop:

```
=== A-Maze-Ing ===

1. Re-generate a new maze using config.txt
2. Show/Hide path from entry to exit
3. Choose maze colors
4. Quit
Choice? (1-4)
```

| Option | Action                                          |
|--------|-------------------------------------------------|
| 1      | Re-reads the config and generates a new maze    |
| 2      | Toggles the BFS solution path overlay           |
| 3      | Pick a wall colour (white / red / green / blue) |
| 4      | Exit the program                                |

---

## Team and project management

### Roles

| Member     | Responsibilities                                              |
|------------|---------------------------------------------------------------|
| \<login1\> | Maze generation (`maze.py`), `mazegen` package, Makefile      |
| \<login2\> | BFS solver (`find_shortest.py`), renderer (`interpreter.py`)  |

*(Update with actual logins and role split.)*

### Planning

Initial estimate: 5 days.

| Day | Planned                                   | Actual                                          |
|-----|-------------------------------------------|-------------------------------------------------|
| 1   | Config parser + data model                | Done on schedule                                |
| 2   | Hunt-and-Kill algorithm                   | Done; wall-coherence debugging took extra time  |
| 3   | BFS solver + output file                  | Done on schedule                                |
| 4   | Terminal renderer + interactive menu      | Done; ANSI colour tuning took longer            |
| 5   | Poetry package, Makefile, README, linting | Done                                            |

### What worked well

- Encoding walls as a 4-bit hexadecimal value kept the grid compact and made
  bit-manipulation easy to reason about.
- Splitting generation, solving, rendering, and parsing into independent modules
  made the reusable package straightforward to extract.
- Using Poetry for both the package and the dev environment gave a single, clean
  `make install` workflow that builds the wheel and sets up linting in one step.

### What could be improved

- The interactive menu re-prints the entire maze on every action; a `curses`-based
  UI would give a much better experience.
- The Hunt-and-Kill hunt phase scans the whole grid each time (O(W×H) per scan).
  For very large mazes, maintaining an explicit frontier list would help.

### Tools used

- **Python 3.10+** — primary language.
- **Poetry** — package build and virtual environment management.
- **flake8** — PEP 8 style linting.
- **mypy** — static type checking.
- **pytest** — unit tests (not submitted).
- **Claude (Anthropic)** — used to generate and review docstrings across all
  modules, apply flake8/mypy fixes systematically, create the Poetry package
  scaffolding, and draft the README structure. All generated content was reviewed,
  understood, and adapted by the team before inclusion.

---

## Resources

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Hunt-and-Kill algorithm — Jamis Buck's blog](http://weblog.jamisbuck.org/2011/1/24/maze-generation-hunt-and-kill-algorithm)
- [Breadth-First Search — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Spanning tree & perfect mazes — think-maths.co.uk](https://www.think-maths.co.uk/mazes)
- [Poetry documentation](https://python-poetry.org/docs/)
- [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/)
- [mypy documentation](https://mypy.readthedocs.io/)
- [flake8 documentation](https://flake8.pycqa.org/)

### AI usage

Claude (Anthropic) was used for the following tasks:

- **Docstrings** — generating initial Google-style docstrings for all functions,
  methods, and modules; reviewed line-by-line against the actual code.
- **Linting fixes** — applying all flake8 and mypy compliance changes across the
  six source files.
- **Poetry scaffolding** — generating `pyproject.toml` files for both the top-level
  project and the `mazegen` package, and structuring the `make install` / `make build`
  workflow.
- **README structure** — drafting the layout and section content based on the
  subject's Chapter VII requirements.

In all cases the output was reviewed, tested manually, and adjusted by the team.