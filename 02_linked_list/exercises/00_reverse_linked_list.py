'''
Reverse Linked List
Given the beginning of a singly linked list head, reverse the list, and return the new beginning of the list.

Example 1:

Input: head = [0,1,2,3]

Output: [3,2,1,0]
Example 2:

Input: head = []

Output: []
Constraints:

0 <= The length of the list <= 1000.
-1000 <= Node.val <= 1000
'''

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reverseList(self, head) -> ListNode:
        prev = None 
        cur = head 
        while cur: 
            temp = cur.next # save this since we will switching links
            cur.next = prev # next node should pt. to prev node 
            prev = cur # prev node should now be at the head **
            cur = temp # cur node should now reverse the next set of nodes
            
        return prev # this will be the head now
        