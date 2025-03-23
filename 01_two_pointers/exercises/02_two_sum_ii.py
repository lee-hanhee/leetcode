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
        start = numbers[0]
        start_ind = 0 # 0 indexed
        end = numbers[len(numbers) - 1]
        end_ind = len(numbers) - 1
        
        for i in range(1,len(numbers)):
            if start + end > target: 
                end_ind = len(numbers) - i - 1
                end = numbers[end_ind] 
                print(end)
            elif start + end < target: 
                start = numbers[i]
                start_ind = i + 1
            else: 
                return [start_ind,end_ind]
        
        return [start_ind,end_ind]
        
if __name__ == "__main__":
    numbers = [100,200,300,500]
    target = 500
    res = Solution().twoSum0(numbers,target)
    print(res)
        
