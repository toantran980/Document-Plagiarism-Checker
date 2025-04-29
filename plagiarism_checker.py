#String Matching: Use Rabin-Karp and KMP algorithms to detect duplicate phrases
# or plagiarized content. Refer to rabin karp.py and kmp algorithm.py.

# Use Rabin-Karp and KMP algorithms to detect duplicate phrases or plagiarized content.
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

# modified the algorithm so instead of reading kmp from input, it reads from a file


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

# Example input
#text = "Hello World, this is Computer Science !!!"
#pattern = "Computer"

# Output
#print("KMP Pattern found at:", kmp_search(text, pattern))

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


# Example input
#text = "Hello World, this is Computer Science !!!"
#pattern = "Computer"

# Output
#print("Rabin Karp Pattern found at:", rabin_karp(text, pattern))


# even if this positions are not check for plagiarized content, so positions does not matter
# modify kabin karp to check for plagiarized content

# check for matching phrases in two files

def check_matching_phrases(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        text1 = f1.read()
        text2 = f2.read()

    kmp_positions = kmp_search(text1, text2)
    rk_positions = rabin_karp(text1, text2)

    return kmp_positions, rk_positions


def extract_plagiarized_words(text1, text2):
    # Normalize text (convert to lowercase and strip whitespace)
    text1 = text1.strip().lower()
    text2 = text2.strip().lower()

    # Split texts into sentences or phrases
    phrases1 = text1.split('.')
    phrases2 = text2.split('.')

    plagiarized_words = set()

    # Check each phrase in text1 against text2 using Rabin-Karp and KMP
    for phrase1 in phrases1:
        for phrase2 in phrases2:
            # Ensure phrases are non-empty
            phrase1 = phrase1.strip()
            phrase2 = phrase2.strip()
            if phrase1 and phrase2:
                # Split phrases into words
                words1 = phrase1.split()
                words2 = phrase2.split()

                # Compare each word in words1 with words2 using Rabin-Karp and KMP
                for i in words1: 
                    for j in words2:
                        if len(i) >= len(j):
                            # Use KMP
                            if kmp_search(i, j):
                                plagiarized_words.add(j)
                            # Use Rabin-Karp
                            elif rabin_karp(i, j):
                                plagiarized_words.add(j)

    return plagiarized_words

# Main function to check plagiarism and print plagiarized words
def check_plagiarism(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        text1 = f1.read()
        text2 = f2.read()

    # Detect plagiarized words using both algorithms
    plagiarized_words = extract_plagiarized_words(text1, text2)

    if plagiarized_words:
        print("Plagiarism detected!")
        print("Plagiarized words:")
        print(" ".join(plagiarized_words))
    else:
        print("No plagiarism detected.")

# Example usage
check_plagiarism('file1.txt', 'file2.txt')

# File 1: Hello, this is pencil pen.
# File 2: Hello, this is a pen.
# Output: Plagiarism detected! 
# Plagiarized words: pencil, pen.