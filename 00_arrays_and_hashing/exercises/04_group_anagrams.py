'''
Group Anagrams
Given an array of strings strs, group all anagrams together into sublists. You may return the output in any order.

An anagram is a string that contains the exact same characters as another string, but the order of the characters can be different.

Example 1:
Input: strs = ["act","pots","tops","cat","stop","hat"]
Output: [["hat"],["act", "cat"],["stop", "pots", "tops"]]

Example 2:
Input: strs = ["x"]
Output: [["x"]]

Example 3:
Input: strs = [""]
Output: [[""]]

Constraints:
1 <= strs.length <= 1000.
0 <= strs[i].length <= 100
strs[i] is made up of lowercase English letters.
'''

from collections import Counter

class Solution:
    def groupAnagrams0(self, strs) -> list:
        # Brute Force: O(m * nlog n) time, O(m * n) space
            # m is # of strings, n is length of average string
        res = {}
        
        for str in strs: 
            sortStr = ''.join(sorted(str)) # sorted str as key 
            res[sortStr] = res.get(sortStr,[]) + [str] # if doesn't exist then [] + [str] = [str]. If exists then [strOld, str]
        
        return list(res.values())
    
    def groupAnagrams1(self, strs) -> list:
        # Hashmap: O(m * n) times, O(m) space
        res = {}
        
        for str in strs: 
            key = [0] * 26
            for char in str: 
                key[ord(char) - ord('a')] += 1 
            res[tuple(key)] = res.get(tuple(key),[]) + [str]
            
        return list(res.values())
        
if __name__ == '__main__':
    strs = ["act","pots","tops","cat","stop","hat"]
    res = Solution().groupAnagrams1(strs)
    print(res)