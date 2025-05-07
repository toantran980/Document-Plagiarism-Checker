# Graph Traversal: Model words in text files as a graph
# Use BFS/DFS to analyze connections.
# Visual representation of word networks using Matplotlib.

from collections import deque
import matplotlib.pyplot as plt
from math import cos, sin, pi
import os

def extract_words_from_file(file):

    #if not os.path.exists(file):
        #print(f"Error: File does not exist.")
        #return []

    with open(file, 'r') as file:
        text = file.read() # Convert to lowercase for consistency
        words = text.split()  # Split text into words
    return words

def build_word_graph(words):
    """
    Build a graph where nodes are words and edges represent consecutive word relationships.
    @return: A dictionary representing the graph.
    """
    graph = {}
    for i in range(len(words) - 1):
        word1, word2 = words[i], words[i + 1]
        if word1 not in graph:
            graph[word1] = []
        if word2 not in graph:
            graph[word2] = []
        graph[word1].append(word2)  # Add a directed edge from word1 to word2
    return graph

def visualize_word_graph(graph):
    """
    Visualize the word network using Matplotlib with a circular layout.
    :param graph: Dictionary representing the word graph.
    """
    # Extract unique nodes
    nodes = list(graph.keys())

    # Assign positions to nodes in a circular layout
    num_nodes = len(nodes)
    angle_step = 360 / num_nodes
    node_positions = {}
    node_radius = 0.5 # Radius of each node bubble, ensuring arrows touch the edge without overlap
    for i, node in enumerate(nodes):
        angle = i * angle_step
        x = 10 * cos(angle * pi / 180)  # Convert angle to radians
        y = 10 * sin(angle * pi / 180)
        node_positions[node] = (x, y)

    # Plot the nodes
    plt.figure(figsize=(12, 10))
    for node, (x, y) in node_positions.items():
        plt.scatter(x, y, s=500, color="skyblue", zorder=2)
        plt.text(x, y, node, fontsize=8, ha="center", va="center", zorder=3)

    # Plot the edges
    for source, targets in graph.items():
        x1, y1 = node_positions[source]
        for target in targets:
            x2, y2 = node_positions[target]
            dx, dy = x2 - x1, y2 - y1
            distance = (dx**2 + dy**2)**0.5

            # Adjust arrow length to touch the edge of the target node bubble
            arrow_length = distance - node_radius
            dx_scaled = dx * (arrow_length / distance)
            dy_scaled = dy * (arrow_length / distance)
            plt.arrow( x1, y1, dx_scaled, dy_scaled, head_width=0.3, head_length=0.5, fc="black", ec="black",length_includes_head=True, zorder=1
            )

    plt.title("Citation Network")
    plt.axis("off")
    plt.show()

def bfs(graph, start):
    # Breadth-First Search to traverse the graph.
    visited = set()  # Set to track visited nodes
    queue = deque([start])  # Queue for BFS starting from the given node
    traversal_order = []  # List to store the traversal order

    print("\nBFS Traversal Order:")
    while queue:
        node = queue.popleft()  # Dequeue a node
        if node not in visited:
            print(node, end=" ")  # Print visited node
            traversal_order.append(node)
            visited.add(node)  # Mark as visited
            for neighbor in graph.get(node, []):  # Traverse neighbors
                if neighbor not in visited:
                    queue.append(neighbor)
    print()
    return traversal_order

def dfs(graph, start, visited=None, traversal_order=None):
    # Depth-First Search to traverse the graph.
    if visited is None:
        visited = set()  # Set to track visited nodes
    if traversal_order is None:
        traversal_order = []  # List to store the traversal order

    visited.add(start)  # Mark the current node as visited
    traversal_order.append(start)
    print(start, end=" ")  # Print visited node

    for neighbor in graph.get(start, []):  # Traverse neighbors
        if neighbor not in visited:
            dfs(graph, neighbor, visited, traversal_order)

    return traversal_order

if __name__ == "__main__":
    # Example text files
    file1 = "file1.txt"  # Content: "The cat's name is Tom"
    file2 = "file2.txt"  # Content: "The mouse's name is Jerry"

    # Extract words from files
    words1 = extract_words_from_file(file1)
    words2 = extract_words_from_file(file2)

    # Combine words from both files
    all_words = words1 + words2

    # Build the word graph
    word_graph = build_word_graph(all_words)
    '''print("Word Graph:")
    for node, neighbors in word_graph.items():
        print(f"{node}: {', '.join(neighbors)}")

    # Perform BFS
    print("\nPerforming BFS from 'the':")
    bfs_traversal = bfs(word_graph, "the")
    print("BFS Traversal Order:", bfs_traversal)

    # Perform DFS
    print("\nPerforming DFS from 'the':")
    dfs_traversal = dfs(word_graph, "the")
    print("\nDFS Traversal Order:", dfs_traversal)'''

    # Visualize the word network
    visualize_word_graph(word_graph)
