from parser import parse_config, MazeConfig
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 config_parser.py <config_file>")
        sys.exit(1)
    try:
        cfg = parse_config(sys.argv[1])
        print("Config parsed successfully:")
        print(cfg)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)