'''
Given an integer array nums and an integer k, return the k most frequent elements within the array.

The test cases are generated such that the answer is always unique.

You may return the output in any order.

Example 1:

Input: nums = [1,2,2,3,3,3], k = 2

Output: [2,3]
Example 2:

Input: nums = [7,7], k = 1

Output: [7]
Constraints:

1 <= nums.length <= 10^4.
-1000 <= nums[i] <= 1000
1 <= k <= number of distinct elements in nums.
'''

class Solution:
    def topKFrequent0(self, nums, k) -> list:
        # Hashmap: O(n log n) time, O(n) space
        dict = {}
        res = []
        for num in nums:
            dict[num] = dict.get(num, 0) + 1 # {1: 1, 2: 2, 3: 3}
            
        sortDictList = sorted(dict.items(), key=lambda x:x[1]) # O(n log n) 
        # [(1,1),(2,2),(3,3)]
    
        n = len(sortDictList)
        for i, key in enumerate(sortDictList): 
            if i < n - k: # disregard first i elements that aren't the last k
                continue
            res.append(key[0])
                
        return res

if __name__ == '__main__':
    nums = [1,1,1,2,2,3,3,3,3,3]
    k = 2
    
    res = Solution().topKFrequent0(nums,k)
    print(res)