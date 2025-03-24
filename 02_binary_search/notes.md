## Binary Search 
- get low and high index, then while low <= high, get mid index and compare with target 
    - if num[mid] > target, then high = mid - 1
    - if num[mid] < target, then low = mid + 1
- ASSUMES increasing sorted array

# Search a 2D Matrix 
- since each row is sorted in non-dec, then apply bin search across the rows, then apply bin search on the row (i.e. columns)
- O(log(m) + log(n)) = O(log(m*n))