import time
import os

# Decorator to log execution and measure runtime
'''def log_execution(func):
    def wrapper(*args, **kwargs):
        print(f"Starting '{func.__name__}'...")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Finished '{func.__name__}' in {end_time - start_time:.6f} seconds.")
        return result
    return wrapper'''

# KMP algorithm
def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    length = 0 # length of the previous longest prefix suffix
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

# Main KMP function to search pattern in text
def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    lps = compute_lps(pattern) #preprocess the pattern
    i = j = 0
    positions = []

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == m:
            positions.append(i - j) # Mathching found
            j = lps[j - 1] # Continue searching here
        elif i < n and pattern[j] != text[i]:
            j = lps[j - 1] if j != 0 else 0
            if j == 0:
                i += 1
    return positions

#Rabin Karp String Matching
#Application: Dectecting duplicate phreases in documents
def rabin_karp(text, pattern, q = 101):
    d = 256
    m = len(pattern)
    n = len(text)
    h = pow(d, m - 1) % q #Precompute highest power for rolling hash
    p_hash = 0 # Hash value of pattern
    t_hash = 0 # Hash of current window of text
    positions = []

    #Compute initial hash for pattern and first window of the text
    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q

    #Slide the pattern over text one by one
    for i in range(n - m + 1):
        #Check if hash values match
        if p_hash == t_hash:
            if text[i:i + m] == pattern:
                positions.append(i)

        #Calculate hash value for next window using rolling hash
        if i < n - m:
            t_hash = (d * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % q
    
        if t_hash < 0: # Ensure positive hash
            t_hash += q

    return positions

# Helper function to check if a word matches using Rabin-Karp or KMP
def is_match(word1, word2):
    # Ensure word1 is longer or equal in length to word2
    return len(word1) >= len(word2) and (kmp_search(word1, word2) or rabin_karp(word1,word2))

# Function to extract plagiarized words from two texts
def check_matching_phrases(file1, file2):
    #print(os.path.exists("file1.txt"))  # Returns True if file exists
    #print(os.path.exists("file2.txt"))  # Returns True if file exists
    #if not os.path.exists(file1) or not os.path.exists(file2):
        #print("Error: One or both files do not exist.")
        #return set()

    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        text1 = f1.read().strip()
        text2 = f2.read().strip()

    # Split texts into words
    words1 = text1.split()
    words2 = set(text2.split())

    matching_phrases = set()

    # Compare each word in words1 with words2 using the helper function
    for word1 in words1:
        for word2 in words2:
            if is_match(word1, word2):
                matching_phrases.add(word2)

    return matching_phrases

# Function to check for plagiarism between two files
#@log_execution # decorator to log execution and measure runtime
def check_plagiarism(file1, file2):
    # Detect plagiarized words
    plagiarized_words = check_matching_phrases(file1, file2)

    if plagiarized_words:
        print("Plagiarism detected!")
        print("Plagiarized content:", " ".join(plagiarized_words))
    else:
        print("No plagiarism detected.")

    return plagiarized_words

# Example input files
#file1 = 'file1.txt'  # Content: "Hello, this is pencil pen."
#file2 = 'file2.txt'  # Content: "Hello, this is a pen."

# Detect plagiarized content
#check_plagiarism(file1, file2)