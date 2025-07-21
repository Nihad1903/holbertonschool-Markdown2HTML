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
    with open("README.html", "w") as output:
        with open(sys.argv[1], 'r') as file:
            for l in file.readlines():
                num = l.count('#')
                text = l.replace("#", "")[1:-1]
                new_line = f"<h{num}>{text}</h{num}>"
                output.write(new_line + "\n")

if __name__ == "__main__":
    # markdownparser()
    headings()
