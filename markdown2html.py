#!/usr/bin/python3
"""Converts a Markdown file to an HTML file."""

import sys
import os
import re
import hashlib


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
        text = apply_inline_formatting(text)
        return f"<h{num}>{text}</h{num}>"
    return None


def parse_unordered(line, state):
    if line.startswith("- "):
        if not state["in_ul"]:
            state["buffer"].append("<ul>")
            state["in_ul"] = True
        item = line[2:].strip()
        item = apply_inline_formatting(item)
        state["buffer"].append(f"<li>{item}</li>")
        return True
    else:
        if state["in_ul"]:
            state["buffer"].append("</ul>")
            state["in_ul"] = False
    return False


def parse_ordered(line, state):
    if line.startswith("* "):
        if not state["in_ol"]:
            state["buffer"].append("<ol>")
            state["in_ol"] = True
        item = line[2:].strip()
        item = apply_inline_formatting(item)
        state["buffer"].append(f"<li>{item}</li>")
        return True
    else:
        if state["in_ol"]:
            state["buffer"].append("</ol>")
            state["in_ol"] = False
    return False


def parse_paragraph(line, state):
    state["paragraph_lines"].append(line)
    return True


def close_paragraph(state):
    if state["paragraph_lines"]:
        lines = [apply_inline_formatting(line.strip())
                 for line in state["paragraph_lines"]]
        joined = "<br/>\n    ".join(lines)
        paragraph = f"<p>\n    {joined}\n</p>"
        state["buffer"].append(paragraph)
        state["paragraph_lines"] = []


def parse_line(line, state):
    stripped = line.strip()

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

    parse_paragraph(stripped, state)


def apply_inline_formatting(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)

    text = re.sub(r'__(.+?)__', r'<em>\1</em>', text)

    def md5_replacer(match):
        content = match.group(1)
        return hashlib.md5(content.encode()).hexdigest()

    text = re.sub(r'\[\[(.+?)\]\]', md5_replacer, text)

    def remove_c(match):
        content = match.group(1)
        return re.sub(r'[cC]', '', content)

    text = re.sub(r'\(\((.+?)\)\)', remove_c, text)

    return text


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
