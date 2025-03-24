## Sliding Window Fixed Size 
1. Initialize two pointers (start, end) and a variable to store window results (e.g., sum, max).
2. Expand the end pointer to include new elements until the window size equals k.
3. Once the window size reaches k, process the window (e.g., compute average/sum) and move the start pointer by 1 to slide the window.
4. Repeat until the end of the array is reached.

## Sliding Window Variable Size
1. Initialize two pointers (start, end) and a tracking structure (e.g., hash map, set).
2. Expand the end pointer to grow the window until a constraint is violated.
3. Once the constraint is violated, shrink the window by moving the start pointer until the constraint is satisfied.
4. Track the optimal window size or other criteria during the process.

Sliding Window Type	Window Size	Typical Use Case
Fixed	Constant	Subarray averages, sums, max in fixed size
Variable	Dynamic	Longest/shortest subarrays, substrings with constraints