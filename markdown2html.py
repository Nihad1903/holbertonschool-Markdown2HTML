#!/usr/bin/python3
"""Converts a Markdown file to an HTML file."""

import sys
import os
import re


def markdownparser():
    if len(sys.argv) < 3:
        output = "Usage: ./markdown2html.py README.md README.html"
        print(output, file=sys.stderr)
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
    if line.startswith("* "):
        if not state["in_ol"]:
            state["buffer"].append("<ol>")
            state["in_ol"] = True
        item = line[2:].strip()
        state["buffer"].append(f"<li>{item}</li>")
        return True
    else:
        if state["in_ol"]:
            state["buffer"].append("</ol>")
            state["in_ol"] = False
    return False


def parse_paragraph(line, state):
    # If it's a potential paragraph line (not a heading or list)
    state["paragraph_lines"].append(line)
    return True


def close_paragraph(state):
    if state["paragraph_lines"]:
        # Join lines with <br /> if more than one line
        lines = [line.strip() for line in state["paragraph_lines"]]
        joined = "<br />\n    ".join(lines)
        paragraph = f"<p>\n    {joined}\n</p>"
        state["buffer"].append(paragraph)
        state["paragraph_lines"] = []


def parse_line(line, state):
    stripped = line.strip()

    # Handle empty lines: close blocks and paragraphs
    if not stripped:
        if state["in_ul"]:
            state["buffer"].append("</ul>")
            state["in_ul"] = False
        if state["in_ol"]:
            state["buffer"].append("</ol>")
            state["in_ol"] = False
        close_paragraph(state)
        return

    heading = parse_heading(stripped)
    if heading:
        if state["in_ul"]:
            state["buffer"].append("</ul>")
            state["in_ul"] = False
        if state["in_ol"]:
            state["buffer"].append("</ol>")
            state["in_ol"] = False
        close_paragraph(state)
        state["buffer"].append(heading)
        return

    if parse_unordered(stripped, state):
        close_paragraph(state)
        return

    if parse_ordered(stripped, state):
        close_paragraph(state)
        return

    # If not any known syntax, assume it's paragraph content
    parse_paragraph(stripped, state)


def convert_markdown(input_file, output_file):
    state = {
        "in_ul": False,
        "in_ol": False,
        "paragraph_lines": [],
        "buffer": []
    }

    with open(input_file, 'r') as file:
        for line in file:
            parse_line(line, state)

    # Close any remaining open blocks
    if state["in_ul"]:
        state["buffer"].append("</ul>")
    if state["in_ol"]:
        state["buffer"].append("</ol>")
    close_paragraph(state)

    with open(output_file, 'w') as output:
        output.write("\n".join(state["buffer"]) + "\n")


if __name__ == "__main__":
    input_file, output_file = markdownparser()
    convert_markdown(input_file, output_file)