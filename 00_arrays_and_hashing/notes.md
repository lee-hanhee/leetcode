# Arrays and Hashing 
## Contains Duplicates 
- set(): good to check for unique elements. 
- len(): length 
- sorted(): sort the list

## Valid Anagram 
- sSort = ''.join(sorted(s)) to sort a string.
- dict is good to store the frequency of each character.

## Two Sum 
- nums[i] = target - nums[j], so we can see if nums[i] in hashmap. 
- If it is, then return the index of nums[i] and i, otherwise, add nums[j] to hashmap.

## Group Anagram 
- dict.get(key, default): get the value of key, if not found, return default.
- dict[key] = dict.get(key, []) + [word]: append word to the list of key.
- list() to convert something to a list.
- ord(): convert a character to its ASCII value.
- ord(char) - ord('a'): get the index of the character in the list.
- dict and list are unhashable, so convert to tuple. 

## Top K Frequent Elements 
- for key, value in dict.items() 
- for i, key in enumerate(list) will give the index and the value of the list.
- sorted(dict.items(), key=lambda x:x[1]) will sort the dictionary by value.