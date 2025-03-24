# LeetCode

A collection of LeetCode problems organized by category.

## Anki Spaced Repetition Review System

This repository includes a spaced repetition system for reviewing LeetCode problems, inspired by Anki flashcards. The system helps track which problems need to be reviewed based on the SM-2 algorithm.

### How to Use

Navigate to the `anki_review` directory and use the following commands:

```bash
# Add a new problem to the review system
python anki.py add <problem_path> [rating]

# Review a problem and update its next review date
python anki.py update <problem_path> [rating]

# Reset a problem's review history
python anki.py reset <problem_path>

# List all problems due for review today
python anki.py list_due

# Update the README with the current problem status
python anki.py update_readme
```

### Simplified Command Format

You can also use a simplified format by just providing the filename:

```bash
# Add a problem using just the filename
python anki.py problem_name.py [rating]

# Examples
python anki.py 00_two_sum.py 3
python anki.py valid_palindrome.py 4
```

The system will automatically search for the file in the repository.

### Rating System

The optional rating argument (1-4) allows you to quickly rate problems:

- 1: Again (Failed completely)
- 2: Hard (Significant difficulty)
- 3: Good (Some difficulty)
- 4: Easy (Perfect recall)

Example:

```bash
# Add a problem and rate it as "Good" (3)
python anki.py add 00_arrays_and_hashing/exercises/03_two_sum.py 3

# Update a problem rating to "Easy" (4)
python anki.py update 00_arrays_and_hashing/exercises/03_two_sum.py 4

# Even simpler: just use the filename
python anki.py 03_two_sum.py 3
```

For more details, see the [Anki Review README](anki_review/README.md).

## Problem Categories

- Arrays & Hashing
- Two Pointers
- Stack
- Binary Search
- Sliding Window
- Linked List
- Trees
- Tries
- Heap/Priority Queue
- Backtracking
- Graphs
- 1D Dynamic Programming
- 2D Dynamic Programming
- Greedy
- Intervals
- Math & Geometry
- Bit Manipulation
