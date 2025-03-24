#!/usr/bin/env python3
import os
import sys
import json
import datetime
import importlib.util
from pathlib import Path

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
review_tool_path = os.path.join(script_dir, "review_tool.py")
metadata_dir = os.path.join(script_dir, "metadata")

# Import review_tool.py to use its resolve_problem_path function directly
spec = importlib.util.spec_from_file_location("review_tool", review_tool_path)
review_tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review_tool)

# Helper function to display metadata
def display_metadata(problem_path, metadata):
    """Display metadata for a problem with formatting"""
    print(f"\nCurrent metadata for '{problem_path}':")
    print(f"  Ease factor: {metadata['ease_factor']}")
    print(f"  Interval: {metadata['interval']} days")
    print(f"  Last reviewed: {metadata['last_reviewed']}")
    print(f"  Next review: {metadata['next_review']}")
    
    # Check if the problem is overdue, but only if review dates are actual dates
    if metadata["next_review"] != "-":
        try:
            today = datetime.date.today()
            next_review_date = datetime.datetime.strptime(metadata["next_review"], "%Y-%m-%d").date()
            if next_review_date < today:
                print(f"  Status: ⚠️ OVERDUE (was due {(today - next_review_date).days} days ago)")
            else:
                days_until_due = (next_review_date - today).days
                print(f"  Status: Due in {days_until_due} days")
        except ValueError:
            print(f"  Status: Not scheduled for review (invalid date format)")
    else:
        print(f"  Status: Not yet reviewed")
    
    print()

def get_metadata_path(problem_path):
    """Get the path to the metadata file for a problem"""
    sanitized_name = problem_path.replace("/", "__").replace("\\", "__") + ".json"
    return os.path.join(metadata_dir, sanitized_name)

def reset_command(problem_path):
    """Reset the metadata for a problem to default values"""
    # Resolve the problem path using the review_tool's function
    resolved_path = review_tool.resolve_problem_path(problem_path)
    
    # Ensure metadata directory exists
    os.makedirs(metadata_dir, exist_ok=True)
    
    metadata_path = get_metadata_path(resolved_path)
    
    # Create default metadata
    metadata = {
        "ease_factor": 2.5,
        "interval": 1,
        "last_reviewed": "-",
        "next_review": "-"
    }
    
    # Save the metadata to file
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Metadata for '{resolved_path}' has been reset.")
    
    # Update the README
    os.system(f"python {review_tool_path} update_readme")
    return 0

def update_command(problem_path, rating=None):
    """Update command for reviewing a problem"""
    # Simply forward to review tool, which will handle path resolution
    cmd = f"python {review_tool_path} update {problem_path} --from-wrapper"
    
    # If rating was provided, pass it to the review tool
    if rating is not None:
        cmd += f" --rating {rating}"
    
    return_code = os.system(cmd)
    if return_code != 0:
        print(f"Error updating problem '{problem_path}'")
        return 1
    return 0

def add_command(problem_path, rating=None):
    """Add command for adding a new problem to the review system"""
    # Forward to review tool, which will handle path resolution
    cmd = f"python {review_tool_path} add {problem_path}"
    
    # If rating was provided, pass it to the review tool
    if rating is not None:
        cmd += f" --rating {rating}"
        
    return_code = os.system(cmd)
    if return_code != 0:
        print(f"Error adding problem '{problem_path}'")
        return 1
    return 0

def list_due_command():
    """List all problems due for review"""
    # Forward to review tool
    return_code = os.system(f"python {review_tool_path} list_due")
    if return_code != 0:
        print("Error listing due problems")
        return 1
    return 0

def update_readme_command():
    """Update the README.md file"""
    # Forward to review tool
    return_code = os.system(f"python {review_tool_path} update_readme")
    if return_code != 0:
        print("Error updating README")
        return 1
    return 0

def fix_metadata_command():
    """Fix metadata filenames with incorrect ..__ prefix"""
    # Forward to review tool
    return_code = os.system(f"python {review_tool_path} fix_metadata")
    if return_code != 0:
        print("Error fixing metadata filenames")
        return 1
    return 0

def main():
    """Main entry point for the Anki CLI wrapper"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  anki.py add <problem_path> [rating]")
        print("  anki.py update <problem_path> [rating]")
        print("  anki.py reset <problem_path>")
        print("  anki.py list_due")
        print("  anki.py update_readme")
        print("  anki.py fix_metadata")
        print("\nRating options (1-4):")
        print("  1 - Again (Failed completely)")
        print("  2 - Hard (Significant difficulty)")
        print("  3 - Good (Some difficulty)")
        print("  4 - Easy (Perfect recall)")
        print("\nNote: You can use just the filename (e.g., 01_two_sum.py) instead of the full path")
        return 1
    
    command = sys.argv[1]
    
    # Handle commands
    if command == "add":
        if len(sys.argv) < 3:
            print("Error: Missing problem path")
            return 1
        rating = None
        if len(sys.argv) >= 4:
            rating = sys.argv[3]
        return add_command(sys.argv[2], rating)
    elif command == "update":
        if len(sys.argv) < 3:
            print("Error: Missing problem path")
            return 1
        rating = None
        if len(sys.argv) >= 4:
            rating = sys.argv[3]
        return update_command(sys.argv[2], rating)
    elif command == "reset" and len(sys.argv) == 3:
        return reset_command(sys.argv[2])
    elif command == "list_due" and len(sys.argv) == 2:
        return list_due_command()
    elif command == "update_readme" and len(sys.argv) == 2:
        return update_readme_command()
    elif command == "fix_metadata" and len(sys.argv) == 2:
        return fix_metadata_command()
    else:
        print("Invalid command or arguments")
        print("Usage:")
        print("  anki.py add <problem_path> [rating]")
        print("  anki.py update <problem_path> [rating]")
        print("  anki.py reset <problem_path>")
        print("  anki.py list_due")
        print("  anki.py update_readme")
        print("  anki.py fix_metadata")
        print("\nYou can use just the filename (e.g., 01_two_sum.py) instead of the full path")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 