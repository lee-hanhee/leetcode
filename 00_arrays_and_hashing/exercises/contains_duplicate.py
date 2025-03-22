"""
Given an integer array nums, return true if any value appears more than once in the array, otherwise return false.

Example 1:

Input: nums = [1, 2, 3, 3]

Output: true

Example 2:

Input: nums = [1, 2, 3, 4]

Output: false

You should aim for a solution with O(n) time and O(n) space, where n is the size of the input array.
"""

class Solution: 
    def hasDuplicate0(self, nums) -> bool: 
        # Brute Force: O(n^2) time, O(1) space
        i = 0
        for num in nums: 
            i += 1
            for num1 in nums[i:]:
                if num == num1: 
                    return True 
        return False
    
    def hasDuplicate1(self, nums) -> bool: 
        # Sort: O(nlogn) time, O(1) space
        nums = sorted(nums)
        for i in range(len(nums) - 1): # [1,2,3,4]
            if nums[i] == nums[i+1]:
                return True 
        return False
    
    def hasDuplicate2(self, nums) -> bool:
        # Hash Set: O(n) time, O(n) space
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False
    
    def hasDuplicate3(self, nums) -> bool:
        # Hash Set Length: O(n) time, O(n) space
        return len(nums) != len(set(nums)) 
    
if __name__ == '__main__':
    nums = [1, 2, 3]
    print(Solution().hasDuplicate1(nums)) # Output: True

    nums = [1, 2, 3, 4,3]
    print(Solution().hasDuplicate1(nums)) # Output: False