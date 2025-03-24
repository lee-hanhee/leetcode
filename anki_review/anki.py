#!/usr/bin/env python3
import os
import sys
import json
import datetime
from pathlib import Path

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
review_tool_path = os.path.join(script_dir, "review_tool.py")
metadata_dir = os.path.join(script_dir, "metadata")

# Helper function to display metadata
def display_metadata(problem_path, metadata):
    """Display metadata for a problem with formatting"""
    print(f"\nCurrent metadata for '{problem_path}':")
    print(f"  Ease factor: {metadata['ease_factor']}")
    print(f"  Interval: {metadata['interval']} days")
    print(f"  Last reviewed: {metadata['last_reviewed']}")
    print(f"  Next review: {metadata['next_review']}")
    
    # Check if the problem is overdue
    today = datetime.date.today()
    next_review_date = datetime.datetime.strptime(metadata["next_review"], "%Y-%m-%d").date()
    if next_review_date < today:
        print(f"  Status: ⚠️ OVERDUE (was due {(today - next_review_date).days} days ago)")
    else:
        days_until_due = (next_review_date - today).days
        print(f"  Status: Due in {days_until_due} days")
    
    print()

def get_metadata_path(problem_path):
    """Get the path to the metadata file for a problem"""
    sanitized_name = problem_path.replace("/", "__").replace("\\", "__") + ".json"
    return os.path.join(metadata_dir, sanitized_name)

def reset_command(problem_path):
    """Reset the metadata for a problem to default values"""
    # Ensure metadata directory exists
    os.makedirs(metadata_dir, exist_ok=True)
    
    metadata_path = get_metadata_path(problem_path)
    
    # Get today's date
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    
    # Create default metadata
    metadata = {
        "ease_factor": 2.5,
        "interval": 1,
        "last_reviewed": today.strftime("%Y-%m-%d"),
        "next_review": tomorrow.strftime("%Y-%m-%d")
    }
    
    # Save the metadata to file
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Metadata for '{problem_path}' has been reset.")
    
    # Update the README
    os.system(f"python {review_tool_path} update_readme")
    return 0

def update_command(problem_path):
    """Update command for reviewing a problem"""
    metadata_path = get_metadata_path(problem_path)
    
    # Check if metadata exists
    if not os.path.exists(metadata_path):
        print(f"No metadata found for '{problem_path}'. Use 'add' command to create it first.")
        return 1
    
    # Load and display current metadata
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    # Remove difficulty_rating if it exists (for backward compatibility)
    if "difficulty_rating" in metadata:
        del metadata["difficulty_rating"]
        # Save the updated metadata back to the file
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    display_metadata(problem_path, metadata)
    
    # Now forward to the review tool to handle the review update
    # Pass --from-wrapper flag to indicate this is being called from anki.py
    os.system(f"python {review_tool_path} update {problem_path} --from-wrapper")
    return 0

def main():
    """Main entry point for the Anki CLI wrapper"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  anki.py add <problem_path>")
        print("  anki.py update <problem_path>")
        print("  anki.py reset <problem_path>")
        print("  anki.py list_due")
        print("  anki.py update_readme")
        return 1
    
    command = sys.argv[1]
    
    # Handle enhanced update command
    if command == "update" and len(sys.argv) == 3:
        return update_command(sys.argv[2])
    
    # Handle reset command
    if command == "reset" and len(sys.argv) == 3:
        return reset_command(sys.argv[2])
    
    # For other commands, forward to the review tool
    args = " ".join(sys.argv[1:])
    return os.system(f"python {review_tool_path} {args}")

if __name__ == "__main__":
    sys.exit(main()) 