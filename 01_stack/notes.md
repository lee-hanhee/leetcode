# Stack Method 

# Valid Parentheses: 
- Stack is used b/c 
    - Every opening bracket must be closed by the correct type of closing bracket.
    - Brackets must be closed in the correct order, meaning the most recently opened bracket must be the first one to close.

# Min Stack 
- Keep track of min value by using a second stack to keep track of the min value that will be at the top of this auxiliary stack.
- When pushing, check if <= to the top of the auxiliary stack. If it is, push it onto the auxiliary stack.
- When popping, check if the value is == to the top of the auxiliary stack. If it is, pop the auxiliary stack (i.e. remove min value)

# Evaluate Reverse Polish Notation
- Use a stack to keep track of the numbers.
- When we encounter an operator, pop the last two numbers from the stack, perform the operation, and push the result back onto the stack.
- int(): if num <0, int(num) = ceil(num), if num >0, int(num) = floor(num)
    - this is needed to satisfy the truncation to 0