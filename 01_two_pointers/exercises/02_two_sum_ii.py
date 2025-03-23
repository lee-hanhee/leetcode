'''
Given an array of integers numbers that is sorted in non-decreasing order.

Return the indices (1-indexed) of two numbers, [index1, index2], such that they add up to a given target number target and index1 < index2. 
    -Note that index1 and index2 cannot be equal, therefore you may not use the same element twice.

There will always be exactly one valid solution.

Your solution must use O(1) additional space.

Example 1:
Input: numbers = [1,2,3,4], target = 3
Output: [1,2]

Explanation:
The sum of 1 and 2 is 3. Since we are assuming a 1-indexed array, index1 = 1, index2 = 2. We return [1, 2].

Constraints:

2 <= numbers.length <= 1000
-1000 <= numbers[i] <= 1000
-1000 <= target <= 1000
'''

class Solution:
    def twoSum0(self, numbers, target) -> list:
        # Two Pointer: O(n) time, O(1) space 
        # Assume only one valid solution
        start,end = 0, len(numbers) - 1
        
        while start < end:
            sum = numbers[start] + numbers[end]
            
            if sum > target:
                end -= 1
            elif sum < target:
                start += 1   
            else:
                return [start + 1, end + 1]             
            
        return []     
        
if __name__ == "__main__":
    numbers = [100,200,300,500]
    target = 500
    res = Solution().twoSum0(numbers,target)
    print(res)
        
