# Huffman Tree Visualization
import matplotlib.pyplot as plt

def plot_huffman_tree(node, x=0, y=0, dx=1.5, depth=0, ax=None, parent=None):
    """Recursively plot Huffman tree using matplotlib."""
    if ax is None:
        fig, ax = plt.subplots(figsize=(22, 12))  # Increased figure size for wide trees
        ax.axis('off')
    if node is None:
        return
    label = f"{node.char if node.char else ''}\n{node.freq}"
    ax.text(x, y, label, ha='center', va='center', bbox=dict(facecolor='skyblue', edgecolor='black', boxstyle='round,pad=0.3'))
    if parent:
        ax.plot([parent[0], x], [parent[1], y], 'k-')
    # Increase horizontal spacing for lower levels
    spacing = dx * (2.0 if depth < 2 else 3.0)  # Further increase horizontal spacing for lower levels
    vertical_step = 1.5  # Increase vertical spacing between levels
    if node.left:
        plot_huffman_tree(node.left, x - spacing/(depth+1), y - vertical_step, dx, depth+1, ax, (x, y))
    if node.right:
        plot_huffman_tree(node.right, x + spacing/(depth+1), y - vertical_step, dx, depth+1, ax, (x, y))
    if depth == 0:
        plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
        plt.show()
    if depth == 0:
        plt.show()

def visualize_huffman_for_text(text):
    """Generate and plot Huffman tree for a given text."""
    freq_map = {char: text.count(char) for char in set(text)}
    root = build_huffman_tree(freq_map)
    plot_huffman_tree(root)
    
##### String Matching #####
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
text = "Hello World, this is Computer Science !!!"
pattern = "Computer"

# Output
print("KMP Pattern found at:", kmp_search(text, pattern))

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
text = "Hello World, this is Computer Science !!!"
pattern = "Computer"

# Output
print("Rabin Karp Pattern found at:", rabin_karp(text, pattern))


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

# Example input
text = "Hello World, this is Computer Science !!!"
pattern = "Computer"

# Output
print("Naive Search Matching found at:", naive_search(text, pattern))


##### Compression #####
# Apply Huffman Coding to compress extracted data 

import heapq # Heap Queue for priority queue operations

# Step 1: Define Huffman Node
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq
    
# Step 2: Build Huffman Tree
def build_huffman_tree(freq_map):
    heap = [HuffmanNode(char, freq) for char, freq in freq_map.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        new_node = HuffmanNode(None, left.freq + right.freq)
        new_node.left = left
        new_node.right = right
        heapq.heappush (heap, new_node)

    return heap[0] 
# Step 3: Generate Huffman Codes
def build_codes(node, prefix="", code_map={}):
    if node is None:
        return
    
    if node.char is not None:
        code_map[node.char] = prefix
    
    build_codes(node.left, prefix + "0", code_map) #left child(0)
    build_codes(node.right, prefix + "1", code_map) #right child(1)

    return code_map

# Step 4: Get user input and compute Huffman Encoding
def generate_huffman_codes(text):
    freq_map = {char: text.count(char) for char in set(text)}

    root = build_huffman_tree(freq_map)
    codes = build_codes(root)

    encoded_text = ''.join(codes[char] for char in text)

    encoded_text = ''.join(codes[char] for char in text)
    
    original_size = len(text.encode('utf-8'))  # Original size in bytes
    compressed_size = len(encoded_text) // 8  # Approximate compressed size in bytes
    
    return codes, encoded_text, original_size, compressed_size


#### Graph Traversal ####
# Model citations or references as a graph and use BFS/DFS to analyze connections.

# BFS and DFS
from collections import deque

def bfs(graph, start):
    visited = set() # Set to track visited cities
    queue = deque([start]) # Queue for BFS starting from the given city
    print("\nBFS Traversal Order:")
    while queue:
        city = queue.popleft() # Dequeue a city
        if city not in visited:
            print(city, end=" ") # Print visited city
            visited.add(city) # Mark as visited
            for neighbour in graph.get(city, []): # Traverse neighbours
                if neighbour not in visited:
                    queue.append(neighbour)
def dfs(graph, node, visited=None):
    # if this is the first call, intialize visited set
    if visited is None:
        visited = set()
    
    # If the curent node has not been visited
    if node not in visited:
        print(node) # Print the node (you can also store it in a list if needed)
        visited.add(node) # Mark the node as visited 
        
        # Recursively visit each unvisited neighbour
        for neighbor in graph.get(node, []):
            dfs(graph, neighbor, visited) # Recursive DFS call for the neighbor

if __name__ == "__main__":
    graph = {}
    print("Enter number of Connections:")
    edges = int(input()) # e.g 5

    print("Enter each Connection (City1 City2):")
    for _ in range(edges):
        u, v = input().split()
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append(v)
        graph[v].append(u) # undirected 

    print("Ennter starting city for BFS:")
    start_city = input()
    bfs(graph, start_city)


# Main Block of code
if __name__ == "__main__":
    # Initialize the graph as an empty dictionary
    graph = {}

    # Ask user how many connections (egdes) in the graph
    print("Enter number of connectionsns in the graph (edges):")
    edges = int(input())

    print("Now enter each connection in the format: node1 node2")
    print("This will assume the graph is undirected (2-way connections)")
    
    for _ in range(edges):
        u, v = input().split() # Read two connected nodes

        # Adding edge from u -> v
        if u not in graph:
            graph[u] = [] # initialize adjacency list for u
        graph[u].append(v)

        # Adding edge from v -> u
        if v not in graph:
            graph[v] = [] # initialize adjacency list for v
        graph[v].append(u)

    # Ask user for starting node to begin DFS traversal
    print("Ennter the starting node for DFS traversal:")
    start_node = input() # e.g., A

    print("\nDFS Traversal Order:")
    dfs(graph, start_node) # Call DFS Function

#### Sorting algo ####
# Organize files by author, title, or date using Merge Sort or Counting Sort.

# Merge Sort
import time # import time module to measure execution time

def mergeSort(flights: list) -> None:

    if len(flights) > 1:
        mid = len(flights) // 2 # find the middle index
        left_half = flights[:mid] # divide list into two halves
        right_half = flights[mid:]
        
        mergeSort(left_half)
        mergeSort(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                flights[k] = left_half[i]
                i += 1
            else:
                flights[k] = right_half[j]
                j += 1
            k += 1
        while i < len(left_half):
            flights[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            flights[k] = right_half[j]
            j += 1
            k += 1
        
if __name__ == "__main__":

    # Taking user input
    num_flights = int(input("Enter number of flights: "))

    flights = []
    for _ in range(num_flights):
        flight_no = int(input("Enter flight number: "))
        dep_time = int(input(f"Enter departure time for {flight_no}: "))
        flights.append((flight_no, dep_time))
    
    mergeSort(flights)

    # Measure the execution time
    start_time = time.time()
    mergeSort(flights)
    end_time = time.time()

    # print the sorted flights and execution time
    print("Flight sorted by departure time: ", flights)
    print(f"Execution time: {end_time - start_time: .6f} seconds")

import random
#Radix Sort LSD (Least Significant Digit) approach
# This code sorts a list of integers using the Radix Sort algorithm.

def counting_sort(arr: list[int], exp: int) -> None:
    n = len(arr)
    output = [0] * n 
    count = [0] * 10 

    # Count occurrences of each digit in the current place value
    for i in range(n):
        index = arr[i] // exp % 10 # Get the digit at the current place value
        count[index] += 1 # Increment the count for that digit

    # Update count[i] so that it contains the actual position of the output[]
    for i in range(1, 10):
        count[i] += count[i - 1]  

    # Build the output array by placing elements in their correct order
    for i in range(n - 1, -1, -1): # Traverse the input array in reverse order
        index = arr[i] // exp % 10 # Get the digit at the current place value
        output[count[index] - 1] = arr[i]
        count[index] -= 1 # decrement count to handle duplicates

    # Copy sorted output back to the original array
    for i in range(n):
        arr[i] = output[i] # overwrite the original array with the sorted values

def radix_sort(arr: list[int]) -> list[int]:
    # Least significant Digit approach (LSD)
    # Find the maximum number to determine the number of digits
    max_num = max(arr)
    exp = 1

    # Continue sorting for each digit place value
    while max_num // exp > 0:
        counting_sort(arr, exp) # Sort based on the current digit
        exp *= 10

    return arr

if __name__ == "__main__":
    # Generate random numbers
    random_list = [random.randint(10, 9999) for _ in range(10)]
    
    print("Orginal Array:", random_list)
    sorted_arr = radix_sort(random_list)
    print("Sorted Array:", sorted_arr)

#### Optimization ####
#Use greedy or dynamic programming approaches to prioritize scanning based on relevance.


# Hints:
# Utilize plain text files for document input.
# Generate sample documents with intentional overlaps for testing plagiarism detection.
# Visualize citation graphs to understand reference structures.
# Modularize code for each functionality to allow independent testing.

# Expected Outcomes:
# A system that inputs documents and outputs detected plagiarized sections with references.
# Compressed versions of documents using Huffman Coding.
# Visual representation of citation networks.
# Sorted document lists based on selected criteria.
# CSUF Document Scanner & Pattern Extractor

