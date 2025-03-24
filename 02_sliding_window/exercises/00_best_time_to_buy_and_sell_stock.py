'''
Best Time to Buy and Sell Stock
You are given an integer array prices where prices[i] is the price of NeetCoin on the ith day.

You may choose a single day to buy one NeetCoin and choose a different day in the future to sell it.

Return the maximum profit you can achieve. You may choose to not make any transactions, in which case the profit would be 0.

Example 1:

Input: prices = [10,1,5,6,7,1]

Output: 6
Explanation: Buy prices[1] and sell prices[4], profit = 7 - 1 = 6.

Example 2:

Input: prices = [10,8,7,5,2]

Output: 0
Explanation: No profitable transactions can be made, thus the max profit is 0.

Constraints:

1 <= prices.length <= 100
0 <= prices[i] <= 100
'''

class Solution:
    def maxProfit(self, prices) -> int:
        # Sliding Window: O(n) time, O(1) space
        maxP = 0
        buy, sell = 0, 1
        
        while sell < len(prices):
            if prices[buy] < prices[sell]:
                profit = prices[sell] - prices[buy]
                maxP = max(maxP, profit)
            else: # p[b] > p[s] so shift it to be lower 
                buy = sell
            sell += 1
                
        return maxP
    
    def maxProfit1(self, prices) -> int:
        # Dynamic Programming: O(n) time, O(n) space
        dp = [0] * len(prices)
        minPrice = prices[0]
        
        for i in range(1, len(prices)):
            minPrice = min(minPrice, prices[i])
            dp[i] = max(dp[i-1], prices[i] - minPrice)
            
        return dp[-1]
            
if __name__ == '__main__':
    prices = [10,1,5,6,7,1]
    res = Solution().maxProfit(prices)
    print(res)