from collections import deque
import math
from typing import List
#from requests import get

class Window:
    def __init__(self):
        self.first = ""
        self.second = ""
        self.third = ""
    
    def get_word(self):
        return "".join([self.first, self.second, self.third])

class CountingBloomFilter:

    def __init__(self, num_item: int, fpr: float):
        """
        """
        self.num_item = num_item
        self.fpr = fpr #false positive rate
        self.memory_size = -1*round((self.num_item * math.log(self.fpr))/(math.log(2))**2)
        self.cbf_array = [0] * self.memory_size
        # rework this later
        self.num_hashfn = min(5, int(round(self.memory_size/self.num_item)*math.log(2)))
        self.prime_list = [127, 149, 277, 397, 401]
        #choosing the appropriate number of primes based on the number of hash functions
        self.primes = self.prime_list[:self.num_hashfn]
           

        
    def hash_cbf(self, item):
        """
        calculating hash values based on the prime numbers
        """
        hash_indices = [] 
        
        for prime_num in self.primes:
            char_hash = 0
            string_hash = 0

            for char in range(len(item)):
                char_hash = (ord(item[char]) * prime_num)   #hash value of one character
                string_hash = string_hash + char_hash #hash value of the whole string

            hash_indices.append(string_hash % self.memory_size)
        return hash_indices
    
  
  
    def compute_cbf_arr(self, text: List[str], window_size: int):
        cur_window = deque() #window of length of the input (3 strings ) 
        end = 0

        #when we delete
        #we recompute the hash value


        while end < len(text): 
            while len(cur_window) < window_size:
                cur_window.append(text[end])
                end += 1
            cur_word = "".join(cur_window)
            print("WHAT ID CUR WORD", cur_word)
            hash_idxs = self.hash_cbf(cur_word)
            print("INDICES", hash_idxs)
            for idx in hash_idxs:
                self.cbf_array[idx] += 1
            cur_window.popleft()
        

  
  
    # def word_to_int(self, word):
    #     total = 0
    #     power = len(word) - 1
    #     for i in range(len(word)):
    #             total += (ord(word[i])*(127**power)) 
    #             total %= 5323
    #             power -= 1
    #     return total



    # def sliding_window_hash(self, text: List[str], window_size: int):
    #     """
    #     calculating hash values of the strings based on the sliding window technique 
    #     """
        
    #     hashed_indices = []
    #     start = 0
    #     end = 0
    #     cur_window= deque()
    #     while end < window_size:
    #         cur_window.append(text[end])
    #         end += 1

    #     while end <= len(text) - 1:
    #         print(cur_window)
    #         adding_el = 0
    #         removing_el = 0
    #         hashed_indices = []
    #         for prime in self.primes:
    #             cur_word = "".join(cur_window)

    #             for word in cur_window:
    #                 hash_value_total += self.word_to_int(word)   
    #                 adding_el = hash_value_total + self.word_to_int(cur_window[-1]) % self.memory_size
    #                 removing_el = (adding_el - self.word_to_int(cur_window[0]))*(prime**(len(cur_window)-1)) % self.memory_size

    #                 #hash value for three words
    #                 #add hash value of the netx word
    #                 #delete hash value of the first 
                    
    #             hashed_indices.append(removing_el % self.memory_size)

    #         for idx in hashed_indices:
    #             print(idx)
    #             self.cbf_array[idx] += 1
    #         cur_window.popleft()
    #         end += 1
            
    #     return 


    def search(self, input_word: str) -> bool:
        """
        """
        indices = self.hash_cbf(input_word) 
        count = len(indices)
        for index in indices: #getting all the hash values of the item
            if self.cbf_array[index] == 0:
                return False
            else:
                count -= 1
        return count == 0

    
    def insert(self, item):
        '''
        Takes the item as an input, and insert its hash values 
        Outputs:

        '''
        indeces = self.hash_cbf(item) 

        
        for index in indeces: #for each of the hash value in the list
            self.cbf_array[index] += 1 #find the index that corresponds to the hashvalue and increment by 1
        return self.cbf_array
        

    def delete(self, item):
        
        """
        """
        if self.search(item):
            indeces = self.hash_cbf(item) 

            for index in indeces: #for each of the hash value in the list
                self.cbf_array[index] -= 1 #find the index that corresponds to the hashvalue and decrement by 1
        else:
            raise KeyError(f'The item {item} you are searching for is not in the list. There is nothing to delete') 


num_item = 
fpr = 0.02
cbf = CountingBloomFilter(num_item, fpr)
print("Array size", cbf.memory_size)
print("Bit array", cbf.cbf_array)
print("Number of hash functions", cbf.num_hashfn)
print(cbf.insert("apple"))
print("All the hash values of the given string", cbf.hash_cbf("apple"))

# print("Rolling hash with resulting hash values:", cbf.rolling_hash("apple"))
# print("Rolling hash with resulting hash values:", cbf.rolling_hash("pple"))
# print("Rolling hash with resulting hash values:", cbf.rolling_hash("vinegar"))


class PlagiarismDetector:

    # n - input length
    #key - window length (i.e length - 3 words)
    # value - array with computed indices (incremented)
    def __init__(self, url, test_words):
        # dictionary: n: int -> bloom_filter: arr[int]
        # store bloom filter for windows of certain length
        self.bloom_filters = {}
        self.url = url
        # don;t forget to uncomment when doing real stuff
        # self.words = self.split_text_to_words(url)
        self.test_words = test_words


    def split_text_to_words(self, url: str) -> List[str]:
        bad_chars = [';', ',', '.', '?', '!', '_', '[', ']', '(', ')', '*']
        data = get(url).text
        data = ''.join(c for c in data if c not in bad_chars)
        data_without_newlines = ''.join(c if (c not in ['\n', '\r', '\t']) else " " for c in data)
        data_just_words = [word for word in data_without_newlines.split(" ") if word != ""]
        data_just_words_lower_case = [word.lower() for word in data_just_words]
        return data_just_words_lower_case

    def split_words_simple(self, text: str):
        return text.split(" ")
    
    # your function
    # 1. Init plagdetector with 1 true_text
    # 2. input plag_text as a parameter to check for plagiarism
    # 3. if plag_test has only 3 words? -> figure it out
    # 4. if plag_text is big, then u split it into windows of x words and run check_for_plagiarism for each one
    # 5. compute percentage

    
    
    def check_phrase_for_plagiarism(self, input: str):
        input_words = self.split_words_simple(input) #phrase is an input:
        num_words = len(input_words)
        
        # key is the length of the sliding window; value is the bit array with indices 

        if self.bloom_filters.get(num_words) is None: #if key is not in the dictionary
            bloom_filter_for_given_size = CountingBloomFilter(10000, 0.02) 
            print("BLOOM", bloom_filter_for_given_size)
            # also look here it's test words for u to test, change to real words once you are done
            bloom_filter_for_given_size.compute_cbf_arr(self.test_words, num_words) #finding aray of indices 
            self.bloom_filters[num_words] = bloom_filter_for_given_size #inserting this key-value pair in dictionary
            print("DICTIONARY", self.bloom_filters)
        return self.bloom_filters[num_words].search(input_words) 



    def get_all_windows(text: List[str], window_size: int):
        windows = []
        cur_window = deque() #window of length of the input (3 strings ) 
        end = 0

        #when we delete
        #we recompute the hash value

        while end < len(text): 
            while len(cur_window) < window_size:
                cur_window.append(text[end])
                end += 1
            windows.append("".join(cur_window))
            cur_window.popleft()
        return windows 



    def check_for_plagiarism(self, plag_text: str):
        words = self.split_to_words(plag_text)
        if (len(words) < 4):
            return 0
        all_words_of_len_4 = self.get_all_windows(words)
        count = 0
        for word in all_words_of_len_4:
            if self.check_phrase_for_plagiarism(word):
                count += 1
        
        return count / len(all_words_of_len_4)



    # def get_all_windows(text: List[str], window_size: int):
    #     windows = []
    #     cur_window = deque() #window of length of the input (3 strings ) 
    #     end = 0

    #     #when we delete
    #     #we recompute the hash value

    #     while end < len(text): 
    #         while len(cur_window) < window_size:
    #             cur_window.append(text[end])
    #             end += 1
    #         windows.append("".join(cur_window))
    #         cur_window.popleft()
    #     return windows 


    #inout text - divide by 4 words
    #check if they are encountered in text 

    def detect_percentage(self, input): 
        pass
        #one in url
        #second to check_for_plagiarism

        #for each of the phrase 
        #do lines 213 - 218


        #if elngth of the inout pharse is less than 4, 

        # all windows of length 4
        # count all of them -> this will help you compute percentage
        # run check_plagiarism on each one
        # if it returns true increment counter
        # once checked all phrases count/number of all 4 word combinations -> this is your plagiarism detector
        


detect = PlagiarismDetector("https://bit.ly/39MurYb", ["here", "is", "some", "text", "that", "we", "found"])
print(detect.check_phrase_for_plagiarism("some text nothtat"))







#create strings with 5 words 
#compute hash indices 
#insert in counting bloom filter
#store the bloom gilter for different length 

