#!/usr/bin/env python3
import json
import os
import sys
import glob
import datetime
from pathlib import Path

METADATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "metadata")
DATE_FORMAT = "%Y-%m-%d"

# Define base directories for LeetCode problems
BASE_DIRS = [
    "00_arrays_and_hashing",
    "01_two_pointers",
    "01_stack",
    "02_binary_search",
    "02_linked_list",
    "02_sliding_window",
    "05_1d_dp"
    # Add other directories as needed
]

def sanitize_filename(path):
    """Convert a problem path to a valid filename for metadata storage"""
    # Ensure the path doesn't start with '../' or './'
    normalized_path = os.path.normpath(path)
    # Remove any leading '../' or './'
    if normalized_path.startswith("../"):
        normalized_path = normalized_path[3:]
    elif normalized_path.startswith("./"):
        normalized_path = normalized_path[2:]
    
    # Replace path separators with double underscores
    return normalized_path.replace("/", "__").replace("\\", "__") + ".json"

def desanitize_filename(filename):
    """Convert a sanitized filename back to the problem path"""
    # Remove .json extension and replace double underscores with path separators
    return filename.replace("__", "/").replace(".json", "")

def get_metadata_path(problem_path):
    """Get the metadata file path for a problem"""
    return os.path.join(METADATA_DIR, sanitize_filename(problem_path))

def resolve_problem_path(input_path):
    """
    Resolve the full problem path from a simplified input.
    Accepts either a full path or just a filename.
    """
    # If it's already a full path and the file exists, use it directly
    if os.path.exists(input_path):
        return os.path.normpath(input_path)
    
    # Try to find the file in known directories
    root_path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Case 1: User provided just the filename (e.g., "01_two_sum.py")
    if os.path.basename(input_path) == input_path:
        matching_files = []
        
        # Search in all base directories' exercises folders
        for base_dir in BASE_DIRS:
            exercises_dir = root_path / base_dir / "exercises"
            if exercises_dir.exists():
                for file_path in exercises_dir.glob(f"*{input_path}*"):
                    if file_path.is_file():
                        matching_files.append(str(file_path.relative_to(root_path)))
        
        if len(matching_files) == 1:
            return matching_files[0]
        elif len(matching_files) > 1:
            print(f"Multiple matches found for '{input_path}':")
            for i, path in enumerate(matching_files, 1):
                print(f"  {i}. {path}")
            
            try:
                choice = int(input("Enter the number of the correct file: "))
                if 1 <= choice <= len(matching_files):
                    return matching_files[choice - 1]
                else:
                    print("Invalid choice. Using the first match.")
                    return matching_files[0]
            except ValueError:
                print("Invalid input. Using the first match.")
                return matching_files[0]
        else:
            # If no matches, warn but continue with the original input
            print(f"Warning: Could not find a file matching '{input_path}' in known directories.")
            return input_path
    
    # Case 2: User provided a partial path (e.g., "exercises/01_two_sum.py")
    else:
        # Try to find matches for the partial path
        matching_files = []
        pattern = f"**/{input_path}"
        
        for file_path in root_path.glob(pattern):
            if file_path.is_file():
                matching_files.append(str(file_path.relative_to(root_path)))
        
        if len(matching_files) == 1:
            return matching_files[0]
        elif len(matching_files) > 1:
            print(f"Multiple matches found for '{input_path}':")
            for i, path in enumerate(matching_files, 1):
                print(f"  {i}. {path}")
            
            try:
                choice = int(input("Enter the number of the correct file: "))
                if 1 <= choice <= len(matching_files):
                    return matching_files[choice - 1]
                else:
                    print("Invalid choice. Using the first match.")
                    return matching_files[0]
            except ValueError:
                print("Invalid input. Using the first match.")
                return matching_files[0]
        else:
            # If no matches, warn but continue with the original input
            print(f"Warning: Could not find a file matching '{input_path}' in known directories.")
            return input_path

def initialize_metadata_dir():
    """Ensure the metadata directory exists"""
    os.makedirs(METADATA_DIR, exist_ok=True)

def add_problem(problem_path, rating=None):
    """Add a new problem to the review system"""
    # Resolve the problem path if it's simplified
    resolved_path = resolve_problem_path(problem_path)
    
    if not os.path.exists(resolved_path):
        print(f"Warning: Problem path '{resolved_path}' does not exist in the repository.")
        
    metadata_path = get_metadata_path(resolved_path)
    
    if os.path.exists(metadata_path):
        print(f"Metadata already exists for '{resolved_path}'. Use 'update' to modify it.")
        return
    
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    
    metadata = {
        "ease_factor": 2.5,
        "interval": 1,
        "last_reviewed": today.strftime(DATE_FORMAT),
        "next_review": tomorrow.strftime(DATE_FORMAT)
    }
    
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Added '{resolved_path}' to review system")
    
    # If rating is provided, update the problem immediately
    if rating is not None:
        update_problem(resolved_path, from_wrapper=True, provided_rating=rating)

def reset_problem(problem_path):
    """Reset a problem to default values"""
    # Resolve the problem path if it's simplified
    resolved_path = resolve_problem_path(problem_path)
    metadata_path = get_metadata_path(resolved_path)
    
    # Create the metadata with default values
    metadata = {
        "ease_factor": 2.5,
        "interval": 1,
        "last_reviewed": "-",
        "next_review": "-"
    }
    
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Reset '{resolved_path}' to default values")

def update_problem(problem_path, from_wrapper=False, provided_rating=None):
    """Update the review metadata for a problem after a review"""
    # Resolve the problem path if it's simplified
    resolved_path = resolve_problem_path(problem_path)
    metadata_path = get_metadata_path(resolved_path)
    
    if not os.path.exists(metadata_path):
        print(f"No metadata found for '{resolved_path}'. Use 'add' to create it first.")
        return
    
    # Load metadata
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    # Remove difficulty_rating if it exists (for backward compatibility)
    if "difficulty_rating" in metadata:
        del metadata["difficulty_rating"]
    
    # Display current metadata only if not called from wrapper
    if not from_wrapper:
        # Display current metadata
        print(f"\nCurrent metadata for '{resolved_path}':")
        print(f"  Ease factor: {metadata['ease_factor']}")
        print(f"  Interval: {metadata['interval']} days")
        print(f"  Last reviewed: {metadata['last_reviewed']}")
        print(f"  Next review: {metadata['next_review']}")
        
        # Check if the problem is overdue
        if metadata["next_review"] != "-":
            try:
                today = datetime.date.today()
                next_review_date = datetime.datetime.strptime(metadata["next_review"], DATE_FORMAT).date()
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
    
    # Reload metadata in case it was modified by wrapper
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    # Remove difficulty_rating if it exists (for backward compatibility)
    if "difficulty_rating" in metadata:
        del metadata["difficulty_rating"]
    
    # Get user rating for this review
    rating = None
    
    # If rating was provided as an argument, use it
    if provided_rating is not None:
        try:
            rating = int(provided_rating)
            if rating < 1 or rating > 4:
                print(f"Invalid rating: {provided_rating}. Please use a number between 1 and 4.")
                return
        except ValueError:
            print(f"Invalid rating: {provided_rating}. Please use a number between 1 and 4.")
            return
    # Otherwise, prompt the user for a rating
    else:
        print("\nRate your performance:")
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
    
    print(f"\nUpdated '{resolved_path}'")
    print(f"Ease factor: {metadata['ease_factor']:.2f}")
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
        
        # Only add problems with actual review dates
        if metadata["next_review"] != "-" and metadata["next_review"] <= today:
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
                metadata_data = json.load(f)
                
                # Remove difficulty_rating if present
                if "difficulty_rating" in metadata_data:
                    del metadata_data["difficulty_rating"]
                    
                metadata[problem_path] = metadata_data
    
    # Generate the README content
    readme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")
    
    # Get today's date for overdue checking
    today = datetime.date.today().strftime(DATE_FORMAT)
    
    with open(readme_path, 'w') as f:
        f.write("# LeetCode Anki Review\n\n")
        f.write("A spaced repetition system for LeetCode problems.\n\n")
        
        # Write instructions for using the tool
        f.write("## What This Tool Does\n\n")
        f.write("An Anki-style review tracker for LeetCode problems, storing metadata separately from your code to enable spaced repetition.\n\n")
        
        f.write("## Requirements\n\n")
        f.write("- Python 3.x\n")
        f.write("- No external libraries required\n\n")
        
        f.write("## How to Use\n\n")
        f.write("```bash\n")
        f.write("# Add a new problem to the review system\n")
        f.write("python anki.py add path/to/problem.py [rating]\n")
        f.write("# or simply use the filename:\n")
        f.write("python anki.py add problem_name.py [rating]\n\n")
        f.write("# Update your rating after reviewing the problem\n")
        f.write("python anki.py update path/to/problem.py [rating]\n")
        f.write("# or simply use the filename:\n")
        f.write("python anki.py update problem_name.py [rating]\n")
        f.write("# If rating is not provided, prompts for one of: again / hard / good / easy\n\n")
        f.write("# List all problems that are due for review today\n")
        f.write("python anki.py list_due\n\n")
        f.write("# Reset review history for a problem\n")
        f.write("python anki.py reset path/to/problem.py\n")
        f.write("# or simply use the filename:\n")
        f.write("python anki.py reset problem_name.py\n")
        f.write("```\n\n")
        
        f.write("## Rating Options (1-4):\n\n")
        f.write("- **1 - Again**: Failed completely, review again tomorrow\n")
        f.write("- **2 - Hard**: Recalled with significant difficulty\n")
        f.write("- **3 - Good**: Recalled with some effort\n")
        f.write("- **4 - Easy**: Perfect recall with no hesitation\n\n")
        
        f.write("## Metadata Format\n\n")
        f.write("Each file is stored in anki_review/metadata/ and looks like this:\n\n")
        f.write("```json\n")
        f.write("{\n")
        f.write("  \"ease_factor\": 2.5,\n")
        f.write("  \"interval\": 3,\n")
        f.write("  \"last_reviewed\": \"2025-03-23\",\n")
        f.write("  \"next_review\": \"2025-03-26\"\n")
        f.write("}\n")
        f.write("```\n\n")
        
        f.write("## Due for Review\n\n")
        
        # Add the table for problems due today
        f.write("<sub>Problem</sub> | <sub>Last Reviewed</sub> | <sub>Next Review</sub> | <sub>Source</sub>\n")
        f.write("---- | ---- | ---- | ----\n")
        
        due_problems = []
        
        for problem_path, meta in metadata.items():
            if meta["next_review"] != "-" and meta["next_review"] <= today:
                due_problems.append((problem_path, meta))
        
        if due_problems:
            for problem_path, meta in sorted(due_problems, key=lambda x: x[1]["next_review"]):
                problem_info = problem_dirs.get(problem_path, {"name": problem_path.split('/')[-1], "category": "Unknown"})
                
                # Generate LeetCode URL (best guess based on problem name)
                leetcode_slug = problem_info["name"].lower().replace(' ', '-')
                leetcode_url = f"https://leetcode.com/problems/{leetcode_slug}"
                
                f.write(f"<sub>[{problem_info['name']}]({leetcode_url})</sub> | ")
                f.write(f"<sub>{meta['last_reviewed']}</sub> | ")
                
                # Check if problem is overdue
                if meta["next_review"] != "-" and meta["next_review"] < today:
                    f.write(f"<sub>⚠️ <span style=\"color:red\">{meta['next_review']}</span></sub> | ")
                else:
                    f.write(f"<sub>{meta['next_review']}</sub> | ")
                
                f.write(f"<sub>[Python](../{problem_path})</sub>\n")
        else:
            f.write("<sub>No problems due for review</sub> | <sub>—</sub> | <sub>—</sub> | <sub>—</sub>\n")
        
        f.write("\n## All Problems\n\n")
        
        # Add sections for each category
        for category, problems in sorted(problem_categories.items()):
            f.write(f"### {category}\n\n")
            
            f.write("<sub>Problem</sub> | <sub>Last Reviewed</sub> | <sub>Next Review</sub> | <sub>Source</sub>\n")
            f.write("---- | ---- | ---- | ----\n")
            
            for problem_path in sorted(problems):
                problem_info = problem_dirs[problem_path]
                
                # Generate LeetCode URL (best guess based on problem name)
                leetcode_slug = problem_info["name"].lower().replace(' ', '-')
                leetcode_url = f"https://leetcode.com/problems/{leetcode_slug}"
                
                f.write(f"<sub>[{problem_info['name']}]({leetcode_url})</sub> | ")
                
                if problem_path in metadata:
                    meta = metadata[problem_path]
                    f.write(f"<sub>{meta['last_reviewed']}</sub> | ")
                    
                    # Check if problem is overdue
                    if meta["next_review"] != "-" and meta["next_review"] < today:
                        f.write(f"<sub>⚠️ <span style=\"color:red\">{meta['next_review']}</span></sub> | ")
                    else:
                        f.write(f"<sub>{meta['next_review']}</sub> | ")
                else:
                    f.write("<sub>—</sub> | <sub>—</sub> | ")
                
                f.write(f"<sub>[Python](../{problem_path})</sub>\n")
            
            f.write("\n")
    
    print(f"Updated README at {readme_path}")

def fix_metadata_filenames():
    """Fix any metadata filenames that have incorrect ..__ prefix"""
    if not os.path.exists(METADATA_DIR):
        print("No metadata directory found.")
        return
    
    fixed_files = 0
    for filename in os.listdir(METADATA_DIR):
        if not filename.endswith('.json'):
            continue
            
        # Check if file starts with ..__ prefix
        if filename.startswith(".."):
            # Get the corrected filename
            corrected_filename = filename.replace("..__", "")
            old_path = os.path.join(METADATA_DIR, filename)
            new_path = os.path.join(METADATA_DIR, corrected_filename)
            
            # Rename the file
            os.rename(old_path, new_path)
            fixed_files += 1
            print(f"Fixed metadata filename: {filename} -> {corrected_filename}")
    
    if fixed_files > 0:
        print(f"Fixed {fixed_files} metadata filenames.")
    else:
        print("No incorrect metadata filenames found.")

def parse_arguments():
    """Parse command line arguments to find flags like --rating"""
    result = {}
    
    # Start from index 1 to skip the script name
    i = 1
    while i < len(sys.argv):
        # Check for flag arguments (starts with --)
        if sys.argv[i].startswith("--"):
            flag_name = sys.argv[i][2:]  # Remove -- prefix
            
            # If there's a next argument and it's not a flag, consider it the flag's value
            if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith("--"):
                result[flag_name] = sys.argv[i + 1]
                # Remove both the flag and its value from argv
                sys.argv.pop(i)
                sys.argv.pop(i)
            else:
                # Flag without value
                result[flag_name] = True
                sys.argv.pop(i)
        else:
            i += 1
    
    return result

def main():
    """Main CLI entry point"""
    initialize_metadata_dir()
    
    # Parse any flag arguments
    flags = parse_arguments()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  review_tool.py add <problem_path> [--rating <1-4>]")
        print("  review_tool.py update <problem_path> [--from-wrapper] [--rating <1-4>]")
        print("  review_tool.py reset <problem_path>")
        print("  review_tool.py list_due")
        print("  review_tool.py update_readme")
        print("  review_tool.py fix_metadata")
        print("\nYou can specify just the filename (e.g., 01_two_sum.py) instead of the full path.")
        return 1
    
    command = sys.argv[1]
    
    if command == "add" and len(sys.argv) == 3:
        rating = flags.get("rating")
        add_problem(sys.argv[2], rating)
        update_readme()
        return 0
    elif command == "update" and len(sys.argv) >= 3:
        # Check if the --from-wrapper flag is set
        from_wrapper = "from-wrapper" in flags
        rating = flags.get("rating")
        update_problem(sys.argv[2], from_wrapper, rating)
        update_readme()
        return 0
    elif command == "reset" and len(sys.argv) == 3:
        reset_problem(sys.argv[2])
        update_readme()
        return 0
    elif command == "list_due" and len(sys.argv) == 2:
        list_due()
        return 0
    elif command == "update_readme" and len(sys.argv) == 2:
        update_readme()
        return 0
    elif command == "fix_metadata" and len(sys.argv) == 2:
        fix_metadata_filenames()
        return 0
    else:
        print("Invalid command or arguments")
        print("Usage:")
        print("  review_tool.py add <problem_path> [--rating <1-4>]")
        print("  review_tool.py update <problem_path> [--from-wrapper] [--rating <1-4>]")
        print("  review_tool.py reset <problem_path>")
        print("  review_tool.py list_due")
        print("  review_tool.py update_readme")
        print("  review_tool.py fix_metadata")
        print("\nYou can specify just the filename (e.g., 01_two_sum.py) instead of the full path.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 