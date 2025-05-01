##### Naive Search #####
# Implement for real-time search in documents

# Naive string matching
def naive_search(text, pattern):
    positions = [] # to store indices where pattern is found
    n = len(text)
    m = len(pattern)

    # Loop through all positions starting positions
    for i in range(n - m + 1):
        match = True
        for j in range(m): # compare each character
            if text[i + j] != pattern[j]:
                match = False # Mismatch found
                break   
        if match:
            positions.append(i) # store the index of the match

    return positions
