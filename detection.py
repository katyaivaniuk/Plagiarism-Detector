from collections import deque
import math
from typing import List
from requests import get

class CountingBloomFilter:
    """
    Implements the Counting Bloom Filter which supports:
    
    - search: queries the membership of an element
    - insert: inserts a string to the filter
    - delete: removes a string from the filter
    - hash_cbf: calculating hash values for the elements inserted
    - compute_cbf_arr: 
    """
    def __init__(self, num_item: int, fpr: float):
        """
        This is a Counting Bloom Filter class that stores the information about the main aspects of CBF: 
        input size, and false positive rate that can be further used to find memory size, initialize bit 
        array, find number of hash functions.
        
        Attributes
        ----------
        num_item : integer
            number of elements in Counting Bloom Filter, corresponding to the parameter num_item.
        fpr : float
            false positive rate of Counting Bloom Filter, corresponding to the parameter fpr.
        memory_size : integer
            length of bit array of Counting Bloom Filter, corresponding to the parameter memory_size.
        cbf_array : list
            initialized bit array of Counting Bloom Filter, corresponding to the parameter fpr.
        num_hashfn : integer
            number of hash functions, corresponding to the parameter num_hashfn.
        prime_list : list 
            list of prime numbers used for CBF, corresponding to the parameter prime_list
        primes : list
            list of primes numbers used for calculating hash values based on number of hash functions
        """
        self.num_item = num_item
        self.fpr = fpr 
        self.memory_size = -1*round((self.num_item * math.log(self.fpr))/(math.log(2))**2) #formula for computing memory_size
        self.cbf_array = [0] * self.memory_size #initializing bit array
        self.num_hashfn = int(round(self.memory_size/self.num_item)*math.log(2))
        self.num_hashfn = min(10, self.num_hashfn) 
        self.prime_list = [127, 149, 179, 197, 233, 257, 283, 313, 379, 401]
        self.primes = self.prime_list[:self.num_hashfn]  #choosing the appropriate number of primes based on the number of hash functions

        
    def hash_cbf(self, item: str):
        """
        Finding the hash values of the item based on the given primes by finding unicode of each character of 
        the string with ord() and using primes as bases. 
    
        Parameters
        ----------
        item: string
            String for which we will be computing k hash values based on k hash functions

        Returns
        ----------
        List
            List containing different hash values of one string depending on the number of hash functions used, 
            and therefore, depending on the number of primes used. 

        """

        hash_indices = [] 
        
        for prime_num in self.primes:
            char_hash = 0
            string_hash = 0
            
            for char in range(len(item)):
                char_hash = ord(item[char]) * (prime_num ** (len(item)- char-1)) #hash value of one character
                string_hash = string_hash + char_hash  #hash value of the whole string

            hash_indices.append(string_hash % self.memory_size)
        return hash_indices



    def compute_cbf_arr(self, text: List[str], window_size: int):
        """
        Uses a deque to create a window of the specified size and computes the hash values of each of the string. 
        The function then adds the computed hash values to the array and increment values at index positions 

        Parameters
        ----------
        text: list
            list of strings that will be used for creating windows to compute hash values 
            
        window_size: int
            integer that represents the sliding window size; number of strings in the window

        Returns
        ----------
        None

        """
          
        cur_window = deque()
        end = 0

        while end < len(text): 
            
            #continue appending strings into the current window until it reaches the desired number 
            # of strings (windows size)
            
            while len(cur_window) < window_size: 
                cur_window.append(text[end])
                end += 1
            
            cur_word = "".join(cur_window) #join several strings into one
            hash_idxs = self.hash_cbf(cur_word)  

            for idx in hash_idxs:
                self.cbf_array[idx] += 1

            #removing the leftmost element in the window --> first string 
            cur_window.popleft()
            


    def search(self, input_word: str) -> bool:
        """
        Searches for the given input word in the Counting Bloom Filter (CBF) array by checking indices that 
        correspond to the computed hash values. 

        Parameters:
        ----------
        input_word: str
            The word/phrase to search for in the CBF array. 

        Returns: 
        ----------
        bool: 
            True if the word is found, False otherwise. 
            True occurs when all the values at index positions are greater than 0, False occurs when one of the 
            values at index positions (hash values) is equal to 0. 

        """
        indices = self.hash_cbf("".join(input_word)) 
        #print("".join(input_word))
        count = len(indices)
        
        for index in indices: 
            if self.cbf_array[index] == 0:
                return False
            else:
                count -= 1
        return count == 0 #return True when all of the indices are checked 

    
    def insert(self, item: str):
        """
        Inserts a given item into the Counting Bloom Filter (CBF) array by finding indices that correspond
        to computed hash values and incrementing the values found at those indices by 1. 

        Parameters:
        ----------
        item: str 
            The string we will insert into the CBF array with the use of computed hash values. 

        Returns:
        ----------
        self.cbf_array: List[int]: 
            The updated CBF array where indices corresponding to hash values 
            have the buckets incremented by 1.
            
        """

        indeces = self.hash_cbf(item) 

        for index in indeces: #for each of the hash value in the list
            self.cbf_array[index] += 1 #find the index that corresponds to the hashvalue and increment by 1
        return self.cbf_array
        

    def delete(self, item: str):
        """
        Deletes a given item from the Counting Bloom Filter (CBF) array by by finding indices that correspond
        to computed hash values of item and decrementing the values found at those indices by 1. 

        Parameters:
        ----------
        item: str
            The item we need to delete from the CBF array. 

        Raises KeyError: 
        If the item is not found in the CBF array. 

        Returns:
        ----------
        None 
        """
        if self.search(item):
            indeces = self.hash_cbf(item) 

            for index in indeces: 
                self.cbf_array[index] -= 1 #find the index that corresponds to the hashvalue and decrement by 1
        else:
            raise KeyError(f'The item {item} you are searching for is not in the list. There is nothing to delete') 


# num_item = 10000
# fpr = 0.01
# cbf = CountingBloomFilter(num_item, fpr)

class PlagiarismDetector:
    """
    This class implements a Plagiarism Detector using a Counting Bloom Filter that supports:
    
    - split_text_to_words: Cleans the text data 
    - check_phrase_for_plagiarism: Checks phrase of specified length, which is number of words for plagiarism 
    - get_all_windows: Creates a list of all the windows of strings of the specified length in the text
    - check_for_plagiarism: Finds the percent of plagiarism based on the number of matches between two texts
    
    """

    def __init__(self, url):
        """
        This is a Plagiarism Detector class using Counting Bloom Filter that takes as input several attributes:
        
        Attributes
        ----------
        url: str
            Input text (inserted as url) that will be used for checking plagiarism between two pieces of text
        
        words: list
            List of "cleaned-up" words sorted by the order they appear in the original file.
            
        bloom_filters: dict
            dictionary where key corresponds to the number of words (windows of certain size), 
            and value corresponds to the bit array with the corresponding values at indices 
           
        """
        
        self.url = url
        self.words = self.split_text_to_words(url)
        self.bloom_filters = {} 

    def split_text_to_words(self, url: str) -> List[str]:
        '''
        Cleans the text data
        
        Parameters
        ----------
        url : string
            The URL for the txt file.
        
        Returns
        -------
        data_just_words_lower_case: list
            List of "cleaned-up" words sorted by the order they appear in the original file.
        '''
        bad_chars = [';', ',', '.', '?', '!', '_', '[', ']', '(', ')', '*']
        data = get(url).text
        data = ''.join(c for c in data if c not in bad_chars)
        data_without_newlines = ''.join(c if (c not in ['\n', '\r', '\t']) else " " for c in data)
        data_just_words = [word for word in data_without_newlines.split(" ") if word != ""]
        data_just_words_lower_case = [word.lower() for word in data_just_words]
        return data_just_words_lower_case


    def split_words_simple(self, text: str):
        '''
        Splits the string
        
        Parameters
        ----------
        text : string
            the phrase that will be splitted into words
        
        Returns
        -------
        text.split(""): list
            List of words sorted by the order they appear in the original phrase.
        '''
        return text.split(" ")
    
    
    def check_phrase_for_plagiarism(self, input_: str):
        """
        Checks phrase for plagiarism by computing the number of words in it, and cheking whether the key with
        this number is already in dictionary. If it is, we are searching for the given input word in the 
        CBF array by checking indices that correspond to the computed hash values. Otherwise, we create a new key
        with new phrase length, and compute array of indices for it.

        Parameters:
        ----------
        input_: str
            string(phrase) that will be checked for 
            

        Returns: 
        ----------
        self.bloom_filters[num_words].search(input_words): bool
            True is the phrase was found, False otherwise
        """
        
        input_words = self.split_words_simple(input_)
        num_words = len(input_words)
    
        #check if key representing number of words in phrase is in the dictionary
        
        if self.bloom_filters.get(num_words) is None: 
            bloom_filter_for_given_size = CountingBloomFilter(10000, 0.001) 
            
            #finding aray of indices for the initial text we have in arguments by splitting it 
            #into window sizes of length of inputted phrases
            
            bloom_filter_for_given_size.compute_cbf_arr(self.words, num_words) 
            self.bloom_filters[num_words] = bloom_filter_for_given_size 
        
        
        return self.bloom_filters[num_words].search(input_words) 




    def get_all_windows(self, text: List[str], window_size: int):
        """
        This function takes a list of strings and a window size as arguments and uses a deque to create a 
        window of the specified size and appends each window to the list.
        
        Parameters
        ----------
        text : list
            List of strings that will be used for creating windows
        window_size: int
            Integer representing the number of words in the window
        
        Returns
        -------
        windows: list
            List of all windows of the specified size

        """
        windows = [] #initializing list of all windows 
        cur_window = deque() 
        end = 0

        while end < len(text): 
            while len(cur_window) < window_size: 
                cur_window.append(text[end]) #append window with the number of words to reach window size 
                end += 1
            windows.append(" ".join(cur_window)) 
            cur_window.popleft() #popping leftmost word in the phrase 
        return windows 



    def check_for_plagiarism(self, plag_text: str):
        """
        This function takes a string(url) as input and gets windows of 4 words that are further used
        as a phrase to be checked for plagiarism. 
        
        Parameters
        ----------
        plag_text : str
            String (url in our case) that will be checked for plagiarism with regard to another piece of text

        Returns
        -------
        count / len(all_words_of_len_4): float
            Float representing the ratio of plagiarised phrases over the all phrases

        """
        words = self.split_text_to_words(plag_text)
        
        if (len(words) < 4):
            return self.get_all_windows(words, 3)
        
        all_words_of_len_4 = self.get_all_windows(words, 4) #getting all phrases of 4 joint words  in a list
        #print(all_words_of_len_4)
        
        count = 0 #initialize counter for plagiarised phrases 
        
        for phrase in all_words_of_len_4:
            if self.check_phrase_for_plagiarism(phrase): #check if the phrase is plagiarized 
                
                count += 1 
         
        return count / len(all_words_of_len_4) 



detect_1 = PlagiarismDetector("https://bit.ly/39MurYb")
print("The plagiarism percentage between the first text and second text is:", detect_1.check_for_plagiarism("https://bit.ly/3we1QCp")*100, "%")

detect_2 = PlagiarismDetector("https://bit.ly/39MurYb")
print("The plagiarism percentage between the first text and third text is:", detect_2.check_for_plagiarism('https://bit.ly/3vUecRn')*100, "%")

detect_3 = PlagiarismDetector("https://bit.ly/3vUecRn")
print("The plagiarism percentage between the second text and third text is:", detect_3.check_for_plagiarism('https://bit.ly/3we1QCp')*100, "%")
