'''
Valid Parentheses
You are given a string s consisting of the following characters: '(', ')', '{', '}', '[' and ']'.

The input string s is valid if and only if:
-Every open bracket is closed by the same type of close bracket.
-Open brackets are closed in the correct order.
-Every close bracket has a corresponding open bracket of the same type.
-Return true if s is a valid string, and false otherwise.

Example 1:

Input: s = "[]"

Output: true
Example 2:

Input: s = "([{}])"

Output: true
Example 3:

Input: s = "[(])"

Output: false
Explanation: The brackets are not closed in the correct order.

Constraints:

1 <= s.length <= 1000
'''

class Solution:
    def isValid0(self, s) -> bool:
        # Brute force: O(n^2) time, O(n) space
        while '()' in s or '{}' in s or '[]' in s: # check the inner brackets then work outwards 
            s = s.replace('()', '')
            s = s.replace('{}', '')
            s = s.replace('[]', '')
        return s == '' # if empty then this must mean its valid
    
    def isValid1(self, s) -> bool:
        # Stack: O(n) time, O(n)
        stack = []
        closeToOpen = {")": "(", "]": "[", "}": "{"}
        
        for char in s: 
            if char in closeToOpen.keys(): # closing bracket 
                if stack != [] and stack[-1] == closeToOpen[char]: # stack not empty and last element is corresponding open bracket then pop from it
                    stack.pop()
                else:
                    return False
        
            else: # open brackets
                stack.append(char)
        
        return True if stack == [] else False
        
if __name__ == '__main__':
    s = "[]"
    res = Solution().isValid0(s)
    print(res)
    
    s = "([{}])"
    res = Solution().isValid1(s)
    print(res)
    
    s = ")"
    res = Solution().isValid1(s)
    print(res)
    
    s = "(]"
    res = Solution().isValid1(s)
    print(res)
    
    s = ")("
    res = Solution().isValid1(s)
    print(res)
    
    s = "()()()()"
    res = Solution().isValid1(s)
    print(res)
    