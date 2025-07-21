#!/usr/bin/python3
import sys

def markdownparser(md_name, md_file):
    num_of_args = len(sys.argv) - 1

    if num_of_args < 2:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        return 1
    elif ".md" not in sys.argv[1]:
        print("Missing <README.md>", file=sys.stderr)

if __name__ == "__main__":
    markdownparser(md_name='test', md_file='test')