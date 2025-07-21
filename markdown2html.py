#!/usr/bin/python3

"""Converts a Markdown file to an HTML file."""

import sys
import os


def markdownparser():
    if len(sys.argv) < 3:
        print(
            "Usage: ./markdown2html.py README.md "
            "README.html",
            file=sys.stderr
        )

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    markdownparser()
