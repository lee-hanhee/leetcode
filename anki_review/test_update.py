#!/usr/bin/env python3
import os
import json
import datetime
from pathlib import Path

# Function to update metadata file with simulated review
def simulate_review(problem_path, rating):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    metadata_dir = os.path.join(script_dir, "metadata")
    
    # Calculate sanitized filename
    sanitized_name = problem_path.replace("/", "__").replace("\\", "__") + ".json"
    metadata_path = os.path.join(metadata_dir, sanitized_name)
    
    if not os.path.exists(metadata_path):
        print(f"No metadata found for '{problem_path}'")
        return
    
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    print(f"Current metadata for {problem_path}:")
    print(f"  Difficulty: {metadata['difficulty_rating']}")
    print(f"  Ease factor: {metadata['ease_factor']}")
    print(f"  Current interval: {metadata['interval']} days")
    print(f"  Last reviewed: {metadata['last_reviewed']}")
    print(f"  Next review: {metadata['next_review']}")
    print()
    
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
    
    metadata["last_reviewed"] = today.strftime("%Y-%m-%d")
    metadata["next_review"] = next_review.strftime("%Y-%m-%d")
    
    print(f"After rating {rating}:")
    print(f"  New ease factor: {metadata['ease_factor']}")
    print(f"  New interval: {metadata['interval']} days")
    print(f"  Next review: {metadata['next_review']}")
    
    print("\nNote: This is just a simulation. The metadata file has not been changed.")

if __name__ == "__main__":
    problem_path = "00_arrays_and_hashing/exercises/03_two_sum.py"
    
    print("Simulating review ratings for Two Sum problem:\n")
    
    print("If you rate as 'Again' (1):")
    simulate_review(problem_path, 1)
    print("\n---------------------------\n")
    
    print("If you rate as 'Hard' (2):")
    simulate_review(problem_path, 2)
    print("\n---------------------------\n")
    
    print("If you rate as 'Good' (3):")
    simulate_review(problem_path, 3)
    print("\n---------------------------\n")
    
    print("If you rate as 'Easy' (4):")
    simulate_review(problem_path, 4) 