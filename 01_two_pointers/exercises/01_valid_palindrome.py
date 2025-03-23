'''
Valid Palindrome
-Given a string s, return true if it is a palindrome, otherwise return false.
-A palindrome is a string that reads the same forward and backward. 
    -It is also case-insensitive and ignores all non-alphanumeric characters.

Example 1:
Input: s = "Was it a car or a cat I saw?"
Output: true

Explanation: After considering only alphanumerical characters we have "wasitacaroracatisaw", which is a palindrome.

Example 2:
Input: s = "tab a cat"
Output: false

Explanation: "tabacat" is not a palindrome.

Constraints:

1 <= s.length <= 1000
s is made up of only printable ASCII characters.
'''

class Solution:
    def isPalindrome(self, s: str) -> bool:
        # Two Pointer: O(n) time, O(1) space 
        lowerS = ''.join(char for char in s if char.isalnum()).lower()

        left = 0
        right = len(lowerS) - 1
        
        while left <= right: # equal for middle 
            if lowerS[left] == lowerS[right]: 
                left += 1
                right -= 1
            else: 
                return False
            
        return True
    
if __name__ == '__main__':
    s = "Was it a car or a cat I saw?"
    res = Solution().isPalindrome(s)
    print(res)
        
            