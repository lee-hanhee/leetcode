#!/usr/bin/env python3
import json
import os
import sys
import datetime
from pathlib import Path

METADATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "metadata")
DATE_FORMAT = "%Y-%m-%d"

def sanitize_filename(path):
    """Convert a problem path to a valid filename for metadata storage"""
    return path.replace("/", "__").replace("\\", "__") + ".json"

def desanitize_filename(filename):
    """Convert a sanitized filename back to the problem path"""
    return filename.replace("__", "/").replace(".json", "")

def get_metadata_path(problem_path):
    """Get the metadata file path for a problem"""
    return os.path.join(METADATA_DIR, sanitize_filename(problem_path))

def initialize_metadata_dir():
    """Ensure the metadata directory exists"""
    os.makedirs(METADATA_DIR, exist_ok=True)

def add_problem(problem_path, difficulty):
    """Add a new problem to the review system"""
    if not os.path.exists(problem_path):
        print(f"Warning: Problem path '{problem_path}' does not exist in the repository.")
        
    metadata_path = get_metadata_path(problem_path)
    
    if os.path.exists(metadata_path):
        print(f"Metadata already exists for '{problem_path}'. Use 'update' to modify it.")
        return
    
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    
    metadata = {
        "difficulty_rating": difficulty.lower(),
        "ease_factor": 2.5,
        "interval": 1,
        "last_reviewed": today.strftime(DATE_FORMAT),
        "next_review": tomorrow.strftime(DATE_FORMAT)
    }
    
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Added '{problem_path}' to review system with difficulty '{difficulty}'")

def update_problem(problem_path):
    """Update the review metadata for a problem after a review"""
    metadata_path = get_metadata_path(problem_path)
    
    if not os.path.exists(metadata_path):
        print(f"No metadata found for '{problem_path}'. Use 'add' to create it first.")
        return
    
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    # Get user rating for this review
    print("Rate your performance:")
    print("1 - Again (Failed completely)")
    print("2 - Hard (Significant difficulty)")
    print("3 - Good (Some difficulty)")
    print("4 - Easy (Perfect recall)")
    
    while True:
        try:
            rating = int(input("Enter your rating (1-4): "))
            if rating < 1 or rating > 4:
                print("Please enter a number between 1 and 4.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    # Implementation of SM-2 algorithm for spaced repetition
    if rating == 1:  # Again
        metadata["interval"] = 1
        metadata["ease_factor"] = max(1.3, metadata["ease_factor"] - 0.2)
    elif rating == 2:  # Hard
        metadata["interval"] = max(1, round(metadata["interval"] * 1.2))
        metadata["ease_factor"] = max(1.3, metadata["ease_factor"] - 0.15)
    elif rating == 3:  # Good
        metadata["interval"] = round(metadata["interval"] * metadata["ease_factor"])
        # Ease factor doesn't change for "Good" rating
    elif rating == 4:  # Easy
        metadata["interval"] = round(metadata["interval"] * metadata["ease_factor"] * 1.3)
        metadata["ease_factor"] = metadata["ease_factor"] + 0.15
    
    today = datetime.date.today()
    next_review = today + datetime.timedelta(days=metadata["interval"])
    
    metadata["last_reviewed"] = today.strftime(DATE_FORMAT)
    metadata["next_review"] = next_review.strftime(DATE_FORMAT)
    
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Updated '{problem_path}'")
    print(f"Next review: {metadata['next_review']} (in {metadata['interval']} days)")

def list_due():
    """List all problems that are due for review"""
    if not os.path.exists(METADATA_DIR):
        print("No metadata directory found. No problems have been added yet.")
        return
    
    today = datetime.date.today().strftime(DATE_FORMAT)
    due_problems = []
    
    for filename in os.listdir(METADATA_DIR):
        if not filename.endswith('.json'):
            continue
        
        metadata_path = os.path.join(METADATA_DIR, filename)
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        if metadata["next_review"] <= today:
            problem_path = desanitize_filename(filename)
            due_problems.append((problem_path, metadata["next_review"]))
    
    if not due_problems:
        print("No problems are due for review.")
        return
    
    print("Problems due for review:")
    for problem_path, next_review in sorted(due_problems, key=lambda x: x[1]):
        print(f"- {problem_path} (due: {next_review})")

def update_readme():
    """Update the README.md file with the Anki review table"""
    from collections import defaultdict
    
    # First, scan the repository for problem files and create a mapping
    problem_dirs = {}
    problem_categories = defaultdict(list)
    
    # Get all directories starting with a number (likely problem categories)
    root_path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    category_dirs = [d for d in root_path.iterdir() 
                    if d.is_dir() and d.name[0].isdigit() and not d.name.startswith('.')]
    
    # For each category, find the problem files
    for category_dir in category_dirs:
        category_name = category_dir.name
        if not '_' in category_name:
            continue
            
        # Clean up the category name for display
        display_name = category_name.split('_', 1)[1].replace('_', ' ').title()
        
        # Look for problems in exercises subdirectory if it exists
        exercises_dir = category_dir / "exercises"
        if exercises_dir.exists():
            problem_dir = exercises_dir
        else:
            problem_dir = category_dir
            
        # Find all Python files in the problem directory
        for problem_file in problem_dir.glob("*.py"):
            if problem_file.name.startswith("__") or problem_file.name == "tempCodeRunnerFile.py":
                continue
                
            relative_path = str(problem_file.relative_to(root_path))
            problem_id = None
            problem_name = problem_file.stem
            
            # Try to extract a problem ID if it exists
            if problem_name[0].isdigit() and '_' in problem_name:
                parts = problem_name.split('_', 1)
                if parts[0].isdigit():
                    problem_id = parts[0]
                    problem_name = parts[1].replace('_', ' ').title()
                    
            # If we couldn't extract an ID, just use the filename
            if problem_id is None:
                problem_name = problem_name.replace('_', ' ').title()
                
            problem_dirs[relative_path] = {
                "category": display_name,
                "name": problem_name,
                "id": problem_id
            }
            problem_categories[display_name].append(relative_path)
    
    # Load all metadata files
    metadata = {}
    if os.path.exists(METADATA_DIR):
        for filename in os.listdir(METADATA_DIR):
            if not filename.endswith('.json'):
                continue
                
            problem_path = desanitize_filename(filename)
            metadata_path = os.path.join(METADATA_DIR, filename)
            
            with open(metadata_path, 'r') as f:
                metadata[problem_path] = json.load(f)
    
    # Generate the README content
    readme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")
    
    with open(readme_path, 'w') as f:
        f.write("# LeetCode Anki Review\n\n")
        f.write("A spaced repetition system for LeetCode problems.\n\n")
        
        f.write("## Due for Review\n\n")
        
        # Add the table for problems due today
        f.write("<sub>Problem</sub> | <sub>Difficulty</sub> | <sub>Last Reviewed</sub> | <sub>Next Review</sub> | <sub>Source</sub>\n")
        f.write("---- | ---- | ---- | ---- | ----\n")
        
        today = datetime.date.today().strftime(DATE_FORMAT)
        due_problems = []
        
        for problem_path, meta in metadata.items():
            if meta["next_review"] <= today:
                due_problems.append((problem_path, meta))
        
        if due_problems:
            for problem_path, meta in sorted(due_problems, key=lambda x: x[1]["next_review"]):
                problem_info = problem_dirs.get(problem_path, {"name": problem_path.split('/')[-1], "category": "Unknown"})
                
                # Generate LeetCode URL (best guess based on problem name)
                leetcode_slug = problem_info["name"].lower().replace(' ', '-')
                leetcode_url = f"https://leetcode.com/problems/{leetcode_slug}"
                
                f.write(f"<sub>[{problem_info['name']}]({leetcode_url})</sub> | ")
                f.write(f"<sub>{meta['difficulty_rating'].capitalize()}</sub> | ")
                f.write(f"<sub>{meta['last_reviewed']}</sub> | ")
                f.write(f"<sub>{meta['next_review']}</sub> | ")
                f.write(f"<sub>[Python](../{problem_path})</sub>\n")
        else:
            f.write("<sub>No problems due for review</sub> | <sub>—</sub> | <sub>—</sub> | <sub>—</sub> | <sub>—</sub>\n")
        
        f.write("\n## All Problems\n\n")
        
        # Add sections for each category
        for category, problems in sorted(problem_categories.items()):
            f.write(f"### {category}\n\n")
            
            f.write("<sub>Problem</sub> | <sub>Difficulty</sub> | <sub>Last Reviewed</sub> | <sub>Next Review</sub> | <sub>Source</sub>\n")
            f.write("---- | ---- | ---- | ---- | ----\n")
            
            for problem_path in sorted(problems):
                problem_info = problem_dirs[problem_path]
                
                # Generate LeetCode URL (best guess based on problem name)
                leetcode_slug = problem_info["name"].lower().replace(' ', '-')
                leetcode_url = f"https://leetcode.com/problems/{leetcode_slug}"
                
                f.write(f"<sub>[{problem_info['name']}]({leetcode_url})</sub> | ")
                
                if problem_path in metadata:
                    meta = metadata[problem_path]
                    f.write(f"<sub>{meta['difficulty_rating'].capitalize()}</sub> | ")
                    f.write(f"<sub>{meta['last_reviewed']}</sub> | ")
                    f.write(f"<sub>{meta['next_review']}</sub> | ")
                else:
                    f.write("<sub>—</sub> | <sub>—</sub> | <sub>—</sub> | ")
                
                f.write(f"<sub>[Python](../{problem_path})</sub>\n")
            
            f.write("\n")
    
    print(f"Updated README at {readme_path}")

def main():
    """Main CLI entry point"""
    initialize_metadata_dir()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  review_tool.py add <problem_path> <difficulty>")
        print("  review_tool.py update <problem_path>")
        print("  review_tool.py list_due")
        print("  review_tool.py update_readme")
        return
    
    command = sys.argv[1]
    
    if command == "add" and len(sys.argv) == 4:
        add_problem(sys.argv[2], sys.argv[3])
        update_readme()
    elif command == "update" and len(sys.argv) == 3:
        update_problem(sys.argv[2])
        update_readme()
    elif command == "list_due" and len(sys.argv) == 2:
        list_due()
    elif command == "update_readme" and len(sys.argv) == 2:
        update_readme()
    else:
        print("Invalid command or arguments")
        print("Usage:")
        print("  review_tool.py add <problem_path> <difficulty>")
        print("  review_tool.py update <problem_path>")
        print("  review_tool.py list_due")
        print("  review_tool.py update_readme")

if __name__ == "__main__":
    main() 