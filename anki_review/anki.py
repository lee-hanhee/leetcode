#!/usr/bin/env python3
import os
import sys

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
review_tool_path = os.path.join(script_dir, "review_tool.py")

# Forward all arguments to the review tool
if __name__ == "__main__":
    args = " ".join(sys.argv[1:])
    os.system(f"python {review_tool_path} {args}") 