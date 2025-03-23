# 1st Variation: Slow and Fast pointers
- When to use: When you need to find a cycle in a linked list or when you need to find the middle of a linked list.
- Example: Find the middle of a linked list.

# 2nd Variation: Start and End pointers
- When to use: When you need to find a subarray that meets a certain condition.
- Example: Find the smallest subarray with a sum >= S.

# Valid Palindrome 
- isalnum(): Returns True if char in the string is alphanumeric.
- lower(): Converts all characters in the string to lowercase.
- 2nd Variation: Start and End pointers with s[start] ==/!= s[end]

# Two Sum 
- 2nd Variation: Start and End pointers w/ num[start] + num[end] >/</== target
- for i in range(len(nums)): # O(n)
    - for j in range(i+1, len(nums)): # O(n)
        - for k in range(j+1, len(nums)): # O(n)
- The above code will generate all possible unique triplets in the array.
- tuple is  