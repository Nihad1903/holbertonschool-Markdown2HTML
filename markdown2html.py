#!/usr/bin/python3

"""Converts a Markdown file to an HTML file."""

import sys
import os


def markdownparser():
    if len(sys.argv) < 3:
        usage = "Usage: ./markdown2html.py README.md README.html"
        print(usage, file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


def headings():
    with open(sys.argv[2], "w") as output:
        with open(sys.argv[1], 'r') as file:
            for line in file:
                if line.startswith("#"):
                    num = len(line) - len(line.lstrip('#'))
                    # Check that it's a valid heading (1–6 #s followed by space)
                    if 1 <= num <= 6 and line[num:num+1] == " ":
                        text = line[num:].strip()
                        new_line = f"<h{num}>{text}</h{num}>"
                        output.write(new_line + "\n")


if __name__ == "__main__":
    # markdownparser()
    headings()
