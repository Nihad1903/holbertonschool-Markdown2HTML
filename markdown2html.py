#!/usr/bin/python3
import sys
import os

def markdownparser(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(output_file):
        print(f"Missing {output_file}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    markdownparser(sys.argv[1], sys.argv[2])