"""
Evaluate Reverse Polish Notation
You are given an array of strings tokens that represents a valid arithmetic expression in Reverse Polish Notation.

Return the integer that represents the evaluation of the expression.

The operands may be integers or the results of other operations.
The operators include '+', '-', '*', and '/'.
Assume that division between integers always truncates toward zero.

Example 1:
Input: tokens = ["1","2","+","3","*","4","-"]
Output: 5
Explanation: ((1 + 2) * 3) - 4 = 5

Constraints:
1 <= tokens.length <= 1000.
tokens[i] is "+", "-", "*", or "/", or a string representing an integer in the range [-100, 100].
"""

class Solution:
    def evalRPN(self, tokens) -> int:
        # Stack: O(n) time and space 
        op = {"+", "-", "*", "/"}
        stack = [] # only add num to the stack
        for ele in tokens:
            res = 0
            if stack == [] or ele not in op: # must be a num to be on the stack
                res = int(ele) # accounts for 1 element 
                stack.append(ele) 
            elif ele in op: 
                num1 = stack.pop()
                num2 = stack.pop() 
                res = int(eval(num2 + ele + num1)) # eval is by convention b op a not a op b
                
                stack.append(str(res))
                
        return res
        
if __name__ == '__main__':
    tokens = ["1","2","+","3","*","4","-"]
    res = Solution().evalRPN(tokens)
    print(res)
    
    tokens=["4","13","5","/","+"]
    res = Solution().evalRPN(tokens)
    print(res)
    
    tokens=["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
    res = Solution().evalRPN(tokens)
    print(res)
        
    tokens=["4","-2","/","2","-3","-","-"]
    res = Solution().evalRPN(tokens)
    print(res)
    