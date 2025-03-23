'''
3Sum
-Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] where nums[i] + nums[j] + nums[k] == 0, and the indices i, j and k are all distinct.
-The output should not contain any duplicate triplets. You may return the output and the triplets in any order.

Example 1:
Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]

Explanation:
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].

Example 2:
Input: nums = [0,1,1]
Output: []
Explanation: The only possible triplet does not sum up to 0.

Example 3:
Input: nums = [0,0,0]
Output: [[0,0,0]]
Explanation: The only possible triplet sums up to 0.

Constraints:

3 <= nums.length <= 1000
-10^5 <= nums[i] <= 10^5
'''

class Solution:
    def threeSum(self, nums) -> list:
        # Brute Force: O(n^3) time, O(1) space
        res = set() # keeps unique triplets
        nums.sort() # removes the case of (0,1,-1) and (-1,0,1) [-1,0,1,2,-1,-4] 
        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                for k in range(j+1, len(nums)):
                    if nums[i] + nums[j] + nums[k] == 0:
                        tmp = [nums[i],nums[j],nums[k]] # 
                        res.add(tuple(tmp)) # convert to tuple b/c lists are unhashable
        
        return [list(i) for i in res]
    
    def threeSum1(self, nums) -> list:
        # Two Pointer: O(n^2) time, O(1) space
        res = []
        nums.sort()
        for i, val in enumerate(nums):
            if i > 0 and val == nums[i-1]: # same value as before, then skip it 
                continue # since we don't want to have duplciates. 

            # do two sum on the remaining part of list
            start, end = i + 1, len(nums) - 1
            while start < end: 
                threeSum = val + nums[start] + nums[end]
                if threeSum > 0: 
                    end -= 1
                elif threeSum < 0: 
                    start += 1 
                else: 
                    res.append([val, nums[start], nums[end]])
                    
                    # update one pointer until its not a dup similar as before but for the condensed list
                    # [-2,-2,0,0,2,2]
                    l += 1 
                    while nums[l] == nums[l-1] and l < r: 
                        l += 1
        
        return res
        
if __name__ == '__main__':
    nums = [-1,0,1,2,-1,-4]
    res = Solution().threeSum(nums)
    print(res)
    
    res = Solution().threeSum1(nums)
    print(res)