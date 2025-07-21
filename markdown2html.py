#!/usr/bin/python3
"""Converts a Markdown file to an HTML file."""

import sys
import os
import re


def markdownparser():
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    return input_file, output_file


def parse_heading(line):
    num = len(line) - len(line.lstrip('#'))
    if 1 <= num <= 6 and line[num:num+1] == " ":
        text = line[num:].strip()
        return f"<h{num}>{text}</h{num}>"
    return None


def parse_unordered(line, state):
    if line.startswith("- "):
        if not state["in_ul"]:
            state["buffer"].append("<ul>")
            state["in_ul"] = True
        item = line[2:].strip()
        state["buffer"].append(f"<li>{item}</li>")
        return True
    else:
        if state["in_ul"]:
            state["buffer"].append("</ul>")
            state["in_ul"] = False
    return False


# Placeholder for future features
def parse_ordered(line, state):
    # Future: handle "1. Item" etc.
    return False


def parse_paragraph(line, state):
    # Future: handle paragraphs
    return False


def parse_line(line, state):
    stripped = line.strip()
    if not stripped:
        if state["in_ul"]:
            state["buffer"].append("</ul>")
            state["in_ul"] = False
        return

    heading = parse_heading(stripped)
    if heading:
        if state["in_ul"]:
            state["buffer"].append("</ul>")
            state["in_ul"] = False
        state["buffer"].append(heading)
        return

    if parse_unordered(stripped, state):
        return

    if parse_ordered(stripped, state):  # reserved
        return

    if parse_paragraph(stripped, state):  # reserved
        return

    # Unknown line — ignore or later handle
    if state["in_ul"]:
        state["buffer"].append("</ul>")
        state["in_ul"] = False


def convert_markdown(input_file, output_file):
    state = {
        "in_ul": False,
        "buffer": []
    }

    with open(input_file, 'r') as file:
        for line in file:
            parse_line(line, state)

    if state["in_ul"]:
        state["buffer"].append("</ul>")

    with open(output_file, 'w') as output:
        output.write("\n".join(state["buffer"]) + "\n")


if __name__ == "__main__":
    input_file, output_file = markdownparser()
    convert_markdown(input_file, output_file)
