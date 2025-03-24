'''
Search a 2D Matrix
You are given an m x n 2-D integer array matrix and an integer target.

Each row in matrix is sorted in non-decreasing order.
The first integer of every row is greater than the last integer of the previous row.
Return true if target exists within matrix or false otherwise.

Can you write a solution that runs in O(log(m * n)) time?

Example 1:
Input: matrix = [[1,2,4,8],[10,11,12,13],[14,20,30,40]], target = 10
Output: true

Example 2:
Input: matrix = [[1,2,4,8],[10,11,12,13],[14,20,30,40]], target = 15
Output: false

Constraints:
m == matrix.length
n == matrix[i].length
1 <= m, n <= 100
-10000 <= matrix[i][j], target <= 10000
'''

class Solution:
    def searchMatrix(self, matrix, target) -> bool:
        # Binary Search: O(log n + log m) time, O(1) space 
        n = len(matrix)
        m = len(matrix[0])
        tRow = 0
        bRow = n-1
        
        while tRow <= bRow: # Binary search on the rows
            mRow = (tRow + bRow) // 2
            if matrix[mRow][0] < target: 
                tRow = mRow + 1
            elif matrix[mRow][0] > target: 
                bRow = mRow - 1
            else: 
                return True
        
        if matrix[mRow][0] < target: # Determine which row to use 
            row_ind = mRow
        else: 
            row_ind = mRow - 1 # if greater, than use prev row 
            
        l = 0
        r = m - 1 
        while l <= r: 
            m = (l + r) // 2
            if matrix[row_ind][m] < target: 
                l = m + 1
            elif matrix[row_ind][m] > target: 
                r = m - 1
            else: 
                return True
        
        return False
    
if __name__ == '__main__':
    matrix = [[1,2,4,8],[10,11,12,13],[14,20,30,40]]
    target = 10
    res = Solution().searchMatrix(matrix,target)
    print(res)
        