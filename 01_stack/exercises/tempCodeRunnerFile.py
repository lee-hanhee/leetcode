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
                res = eval(num2 + ele + num1) # eval is by convention b op a not a op b
                
                res = round(res)
                
                stack.append(str(res))
                
        return res