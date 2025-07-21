#!/usr/bin/python3

import sys
import os

def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the Markdown file exists
    if not os.path.exists(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)
    # Check if the number of arguments is correct
    if len(sys.argv) == 1 or len(sys.argv) == 2:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)
    # Convert Markdown to HTML
    sys.exit(0)

if __name__ == "__main__":
    main()