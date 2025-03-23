'''
Design a stack class that supports the push, pop, top, and getMin operations.

-MinStack() initializes the stack object.
-void push(int val) pushes the element val onto the stack.
-void pop() removes the element on the top of the stack.
-int top() gets the top element of the stack.
-int getMin() retrieves the minimum element in the stack.
Each function should run in O(1) time.

Example 1:
Input: ["MinStack", "push", 1, "push", 2, "push", 0, "getMin", "pop", "top", "getMin"]
Output: [null,null,null,null,0,null,2,1]

Explanation:
MinStack minStack = new MinStack();
minStack.push(1);
minStack.push(2);
minStack.push(0);
minStack.getMin(); // return 0
minStack.pop();
minStack.top();    // return 2
minStack.getMin(); // return 1
Constraints:

-2^31 <= val <= 2^31 - 1.
pop, top and getMin will always be called on non-empty stacks.
'''

class MinStack:
    def __init__(self):
        self.stack = []         # main stack for values
        self.min_stack = []     #  min will always be at top of stack

    def push(self, val) -> None:
        self.stack.append(val)
        if self.min_stack == [] or val <= self.min_stack[-1]: 
            self.min_stack.append(val)

    def pop(self) -> None:
        if self.stack == []:
            return
        val = self.stack.pop()
        if val == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]

if __name__ == '__main__':
    ms = MinStack()
    ms.push(2)
    ms.push(2)
    ms.push(1)
    ms.push(3)
    ms.push(1)
    print("Top:", ms.top())   
    ms.pop() # pop 1
    print("Min:", ms.getMin())  
    ms.pop() # pop 3
    print("Min:", ms.getMin())  
    ms.pop() # pop 1
    print("Min:", ms.getMin())  
    ms.pop() # pop 2      
    print("Min:", ms.getMin())  
    ms.pop() # pop 2
    print("Min:", ms.getMin())  
