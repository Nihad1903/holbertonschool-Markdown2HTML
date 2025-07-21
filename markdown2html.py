#!/usr/bin/python3

import sys
import os

def main():
    # Check if we have enough arguments (need 2 arguments plus script name)
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)
    
    markdown_file = sys.argv[1]  # First argument: Markdown file name
    output_file = sys.argv[2]    # Second argument: Output file name
    
    # Check if markdown file exists
    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)
    
    # Otherwise, exit successfully without printing anything
    sys.exit(0)

if __name__ == "__main__":
    main()