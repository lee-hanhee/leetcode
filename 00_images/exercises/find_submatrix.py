'''Problem Statement:
-Given two 2D integer matrices: matrix of size M x N, and a smaller matrix pattern of size m x n.
-Your task is to find the top-left coordinate(s) where the pattern exactly matches a submatrix in matrix.

Return:
-A list of (row, col) pairs where the submatrix starting at (row, col) matches the pattern exactly.
-If no match is found, return an empty list.

Function Signature:
def find_submatrix(matrix: List[List[int]], pattern: List[List[int]]) -> List[Tuple[int, int]]:

Example:
Input:
matrix = [
  [1, 2, 3, 4],
  [5, 6, 7, 8],
  [9, 0, 1, 2],
  [3, 4, 5, 6]
]

pattern = [
  [7, 8],
  [1, 2]
]
Output:
[(1, 2)]
Explanation: The pattern matches the submatrix starting at row 1, column 2.

🧠 Follow-up 1: One Best Match
If the problem only asks for the first or best match, you can optimize by returning early.

🧠 Follow-up 2: Approximate Matching
Extend the question to allow for a small margin of error, like:
if abs(matrix[i+x][j+y] - pattern[x][y]) <= delta
Useful as a precursor to template matching in images.
'''

from typing import List, Tuple
import numpy as np

def find_submatrix(matrix: List[List[int]], pattern: List[List[int]]) -> List[Tuple[int, int]]:
    # Get dimensions of both matrices
    M, N = len(matrix), len(matrix[0])    # M rows, N columns in the main matrix
    m, n = len(pattern), len(pattern[0])  # m rows, n columns in the pattern matrix
    
    matches = []  # List to store the coordinates of matching positions

    # Iterate through all possible top-left positions where pattern can fit
    # We only need to check positions where pattern can fully fit within matrix
    for i in range(M - m + 1):  # Iterate through valid row positions
        for j in range(N - n + 1):  # Iterate through valid column positions
            match = True  # Assume there's a match until proven otherwise
            
            # Check if the pattern matches at the current position (i,j)
            for x in range(m):  # Iterate through pattern rows
                for y in range(n):  # Iterate through pattern columns
                    # Compare the current element in pattern with corresponding element in matrix
                    # matrix[i+x][j+y] is the element in the main matrix
                    # pattern[x][y] is the element in the pattern matrix
                    if matrix[i + x][j + y] != pattern[x][y]:
                        match = False  # Mismatch found, so this position doesn't work
                        break  # No need to check further elements in this row
                
                if not match:
                    break  # Pattern doesn't match, so skip to next position
            
            # If we've checked all elements and match is still True, we found a match
            if match:
                matches.append((i, j))  # Add the top-left coordinates to our results

    return matches  # Return all matching positions
  
# Increasing delta increases flexibility, useful in image matching with noise, quantized image data, or sensor errors.
def find_submatrix_approx(matrix: List[List[int]], pattern: List[List[int]], delta: int = 0) -> List[Tuple[int, int]]:
  M, N = len(matrix), len(matrix[0])
  m, n = len(pattern), len(pattern[0])

  matches = []

  for i in range(M - m + 1):
      for j in range(N - n + 1):
          match = True
          for x in range(m):
              for y in range(n):
                  if abs(matrix[i + x][j + y] - pattern[x][y]) > delta:
                      match = False
                      break
              if not match:
                  break
          if match:
              matches.append((i, j))

  return matches

def find_submatrix_numpy(matrix: np.ndarray, pattern: np.ndarray) -> List[Tuple[int, int]]:
    M, N = matrix.shape
    m, n = pattern.shape

    matches = []

    for i in range(M - m + 1):
        for j in range(N - n + 1):
            submatrix = matrix[i:i+m, j:j+n]
            if np.array_equal(submatrix, pattern):
                matches.append((i, j))
    
    return matches


    