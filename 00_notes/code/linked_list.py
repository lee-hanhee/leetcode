# Implement (I did with tail pointer & without):
#  size() - returns the number of data elements in the list
#  empty() - bool returns true if empty
#  value_at(index) - returns the value of the nth item (starting at 0 for first)
#  push_front(value) - adds an item to the front of the list
#  pop_front() - remove the front item and return its value
#  push_back(value) - adds an item at the end
#  pop_back() - removes end item and returns its value
#  front() - get the value of the front item
#  back() - get the value of the end item
#  insert(index, value) - insert value at index, so the current item at that index is pointed to by the new item at the index
#  erase(index) - removes node at given index
#  value_n_from_end(n) - returns the value of the node at the nth position from the end of the list
#  reverse() - reverses the list
#  remove_value(value) - removes the first item in the list with this value

class Node: 
    def __init__(self, data):
        self.data = data
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None 
        self.tail = None 
        self.count = 0 
    
    def size(self):
        return self.count
    
    def empty(self):
        return True if self.count == 0 else False
    
    def value_at(self, index):
        # error check 
        if index < 0 or index >= self.count: 
            return None

        # Go until at index and return its data
        current = self.head 
        for i in range(index): # 0 indexed
            current = current.next  
        return current.data 
    
    def push_front(self, value):
        # New node (and move next to current head)
        new_head = Node(value) 
        new_head.next = self.head 
        
        # New node is new head 
        self.head = new_head
   
        # Special case
        if self.count == 0: 
            self.tail = self.head 
             
        # Update count
        self.count += 1
    
    
    def pop_front(self):
        if self.empty():
            return None
        else: 
            pop_node = self.head 
            self.head = self.head.next
            self.count -= 1
            
            if self.count == 0: 
                self.tail = None 
                
        return pop_node.data
    
    def pop_back(self):
        return None
    
    def front(self):
        return self.head.data
    
    def back(self):
        return self.tail.data
    
    def insert(self, index, value):
        return None
        
    def erase(self, index):
        return None
    
    def value_n_from_end(self, n):
        return None
    
    def reverse(self):
        return None
    
    def remove_value(self, value):
        return None