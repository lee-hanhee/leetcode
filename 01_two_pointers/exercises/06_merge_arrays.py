class Solution(object):
    def merge(self, nums1, m, nums2, n):
        """
        :type nums1: List[int]
        :type m: int
        :type nums2: List[int]
        :type n: int
        :rtype: None Do not return anything, modify nums1 in-place instead.
        """
        # Two pointer at end, #[1,2,3,0,0,0] # [2,5,6]
        i1 = m-1
        i2 = n-1

        while i2 >= 0: 
            if i1 >= 0 and nums1[i1] >= nums2[i2]:
                nums1[i1 + i2 + 1] = nums1[i1]
                i1 -= 1
            else:
                nums1[i1 + i2 + 1] = nums2[i2]
                i2 -= 1
    
            




        