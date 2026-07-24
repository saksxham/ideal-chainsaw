class Solution:
    def selectionSort(self, nums):
        l=len(nums)
        for i in range(l-1):
            min_e=nums[i]
            idx=i
            for j in range(i+1,l):
                if nums[j]<min_e:
                    min_e=nums[j]
                    idx=j
                    print('min_e: ',min_e,' idx: ',idx,' in iteration: ',i)
                    
            temp=nums[i]
            nums[i]=nums[idx]
            nums[idx]=temp
            print('after reshuffle: ',nums)
        return nums
