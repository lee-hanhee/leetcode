'''
Given two strings s and t, return true if the two strings are anagrams of each other, otherwise return false.

An anagram is a string that contains the exact same characters as another string, but the order of the characters can be different.

Example 1:

Input: s = "racecar", t = "carrace"

Output: true
Example 2:

Input: s = "jar", t = "jam"

Output: false
Constraints:

s and t consist of lowercase English letters.
'''

from collections import Counter

class Solution: 
    def isAnagram0(self, s, t) -> bool:
        # Brute Force: O(nlogn + mlogm) time, O(n + m) space 
        sSort = ''.join(sorted(s))
        tSort = ''.join(sorted(t))
        
        # Base case (so 2nd conditional doesn't get messed up)
        if len(sSort) != len(tSort):
            return False
        
        i = 0
        for char in sSort: 
            if char == tSort[i]:
                i += 1
        
        if i == len(sSort):
            return True

        return False

    def isAnagram1(self, s, t) -> bool:
        # Brute Force: O(nlogn + mlogm) time, O(1) space 
        if len(s) != len(t):
            return False 
        
        return sorted(s) == sorted(t)

    def isAnagram2(self, s, t) -> bool: 
        # Count: O(n + m) time, O(1) space
        sCount = Counter(s)
        tCount = Counter(t)
        
        return sCount == tCount
    
    def isAnagram3(self, s, t) -> bool: 
        # Hash Table (basically creating Counter()): O(n + m) time, O(1) space
        if len(s) != len(t): 
            return False 
        
        sDict, tDict = {}, {}
        for i in range(len(s)):
            sDict[s[i]] = 1 + sDict.get(s[i],0)
            tDict[t[i]] = 1 + tDict.get(t[i],0)
        
        return sDict == tDict
        
if __name__ == '__main__':
    s = "carrace"
    t = "racecar"
    print(Solution().isAnagram3(s,t))
        