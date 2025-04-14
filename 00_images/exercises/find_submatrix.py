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
    """
    Find all occurrences of a pattern matrix within a larger matrix.
    
    First principles:
    - Sliding window approach: Check every possible position where the pattern could fit
    - Element-wise comparison: Compare each element in the pattern with corresponding elements in the matrix
    - Early termination: Stop checking a position as soon as a mismatch is found
    
    Time Complexity: O((M-m+1) * (N-n+1) * m * n) where:
    - M, N are dimensions of the main matrix
    - m, n are dimensions of the pattern
    
    Parameters:
        matrix: The larger 2D matrix to search within
        pattern: The smaller 2D matrix pattern to find
        
    Returns:
        List of (row, col) pairs indicating top-left positions where pattern is found
    """
    M, N = len(matrix), len(matrix[0])    # Dimensions of the main matrix
    m, n = len(pattern), len(pattern[0])  # Dimensions of the pattern matrix
    
    matches = []  # List to store the matching positions

    # Iterate through all possible starting positions in the matrix
    # Only need to check positions where the pattern can fully fit
    for i in range(M - m + 1):
        for j in range(N - n + 1):
            match = True  # Assume there's a match until proven otherwise
            for x in range(m):
                for y in range(n):
                    if matrix[i + x][j + y] != pattern[x][y]:
                        match = False  # Found a mismatch
                        break  # No need to check further elements in this row
                if not match:
                    break  # Pattern doesn't match at this position, try the next position
            if match:
                matches.append((i, j))  # Add the matching position to our results

    return matches  # Return all matching positions

# Increasing delta increases flexibility, useful in image matching with noise, quantized image data, or sensor errors.
def find_submatrix_approx(matrix: List[List[int]], pattern: List[List[int]], delta: int = 0) -> List[Tuple[int, int]]:
    """
    Find all approximate matches of a pattern matrix within a larger matrix, allowing for some margin of error.
    
    First principles:
    - Similar to exact matching but allows for values to be within a delta range
    - Useful for image processing where values might have small variations due to noise
    - A larger delta means more permissive matching (more tolerant to differences)
    
    Parameters:
        matrix: The larger 2D matrix to search within
        pattern: The smaller 2D matrix pattern to find
        delta: Maximum allowed absolute difference between corresponding elements
        
    Returns:
        List of (row, col) pairs indicating top-left positions where pattern approximately matches
    """
    M, N = len(matrix), len(matrix[0])
    m, n = len(pattern), len(pattern[0])
  
    matches = []
  
    for i in range(M - m + 1):
        for j in range(N - n + 1):
            match = True
            for x in range(m):
                for y in range(n):
                    # Check if the absolute difference is within the allowed delta
                    if abs(matrix[i + x][j + y] - pattern[x][y]) > delta:
                        match = False
                        break
                if not match:
                    break
            if match:
                matches.append((i, j))
  
    return matches

def find_submatrix_numpy(matrix: np.ndarray, pattern: np.ndarray) -> List[Tuple[int, int]]:
    """
    Find all occurrences of a pattern matrix using NumPy for more efficient operations.
    
    First principles:
    - Vectorized approach using NumPy's array operations for better performance
    - The core algorithm is the same, but implementation is optimized
    - np.array_equal provides efficient array comparison
    
    Parameters:
        matrix: The larger 2D numpy array to search within
        pattern: The smaller 2D numpy array pattern to find
        
    Returns:
        List of (row, col) pairs indicating top-left positions where pattern is found
    """
    M, N = matrix.shape
    m, n = pattern.shape
  
    matches = []
  
    for i in range(M - m + 1):
        for j in range(N - n + 1):
            # Extract the submatrix at the current position
            submatrix = matrix[i:i+m, j:j+n]
            # Use numpy's array_equal for efficient comparison
            if np.array_equal(submatrix, pattern):
                matches.append((i, j))
    
    return matches

if __name__ == "__main__":
    print("Testing submatrix finding algorithms")
    
    # Test Case 1: Basic example from the problem statement
    print("\n=== Test Case 1: Basic Example ===")
    matrix1 = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 0, 1, 2],
        [3, 4, 5, 6]
    ]
    
    pattern1 = [
        [7, 8],
        [1, 2]
    ]
    
    result1 = find_submatrix(matrix1, pattern1)
    print(f"Matrix:\n{np.array(matrix1)}")
    print(f"Pattern:\n{np.array(pattern1)}")
    print(f"Matches found at: {result1}")
    
    # Test Case 2: Multiple matches
    print("\n=== Test Case 2: Multiple Matches ===")
    matrix2 = [
        [1, 2, 1, 2],
        [3, 4, 3, 4],
        [1, 2, 1, 2],
        [3, 4, 3, 4]
    ]
    
    pattern2 = [
        [1, 2],
        [3, 4]
    ]
    
    result2 = find_submatrix(matrix2, pattern2)
    print(f"Matrix:\n{np.array(matrix2)}")
    print(f"Pattern:\n{np.array(pattern2)}")
    print(f"Matches found at: {result2}")
    
    # Test Case 3: No matches
    print("\n=== Test Case 3: No Matches ===")
    matrix3 = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    
    pattern3 = [
        [5, 5],
        [8, 9]
    ]
    
    result3 = find_submatrix(matrix3, pattern3)
    print(f"Matrix:\n{np.array(matrix3)}")
    print(f"Pattern:\n{np.array(pattern3)}")
    print(f"Matches found at: {result3}")
    
    # Test Case 4: Approximate matching
    print("\n=== Test Case 4: Approximate Matching ===")
    matrix4 = [
        [10, 20, 30],
        [40, 51, 61],
        [70, 81, 90]
    ]
    
    pattern4 = [
        [50, 60],
        [80, 90]
    ]
    
    # No exact matches
    result4_exact = find_submatrix(matrix4, pattern4)
    # With delta=1, should find a match
    result4_approx = find_submatrix_approx(matrix4, pattern4, delta=1)
    
    print(f"Matrix:\n{np.array(matrix4)}")
    print(f"Pattern:\n{np.array(pattern4)}")
    print(f"Exact matches found at: {result4_exact}")
    print(f"Approximate matches (delta=1) found at: {result4_approx}")
    
    # Test Case 5: NumPy implementation
    print("\n=== Test Case 5: NumPy Implementation ===")
    # Convert to NumPy arrays
    np_matrix = np.array(matrix1)
    np_pattern = np.array(pattern1)
    
    result5 = find_submatrix_numpy(np_matrix, np_pattern)
    print(f"Using NumPy implementation:")
    print(f"Matches found at: {result5}")
    
    # Compare performance on larger matrices
    print("\n=== Performance Comparison ===")
    import time
    
    # Generate a larger random matrix and pattern
    large_matrix = np.random.randint(0, 10, (100, 100))
    small_pattern = large_matrix[25:30, 25:30].copy()  # Extract a portion as pattern
    
    # Time the standard implementation
    start = time.time()
    find_submatrix(large_matrix.tolist(), small_pattern.tolist())
    standard_time = time.time() - start
    
    # Time the NumPy implementation
    start = time.time()
    find_submatrix_numpy(large_matrix, small_pattern)
    numpy_time = time.time() - start
    
    print(f"Time with standard implementation: {standard_time:.6f} seconds")
    print(f"Time with NumPy implementation: {numpy_time:.6f} seconds")
    print(f"NumPy speedup: {standard_time/numpy_time:.2f}x")
    