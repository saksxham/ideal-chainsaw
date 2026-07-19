from collections import defaultdict

class Solution:
    # Function to count the frequency of each element in the input array
    def countFrequencies(self, nums):
        freq = defaultdict(int)  # Default dictionary to store the frequency of each element

        # Step 1: Count the frequency of each element in the array
        for num in nums:
            freq[num] += 1  # Increment the count of the current element

        # Step 2: Prepare the result in the form of a 2D list
        result = [[key, value] for key, value in freq.items()]

        # Step 3: Return the result
        return result

# Main function to test the solution
if __name__ == "__main__":
    nums = [1, 2, 2, 3, 3, 3, 4]  # Example input array

    sol = Solution()
    result = sol.countFrequencies(nums)

    # Print result
    for pair in result:
        print(f"Element: {pair[0]}, Frequency: {pair[1]}")

