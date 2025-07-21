#!/usr/bin/python3
import sys
import os
def markdownparser():
    """Markdown to HTML argument validator"""

    import sys
    import os

    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.isfile(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    # All conditions passed — exit silently
    sys.exit(0)

if __name__ == "__main__":
    markdownparser()