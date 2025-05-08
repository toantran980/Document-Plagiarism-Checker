# Graph Traversal: Model words in text files as a graph
# Use BFS/DFS to analyze connections.
# Visual representation of word networks using Matplotlib.

from collections import deque
import matplotlib.pyplot as plt
from math import cos, sin, pi
import os

def extract_words_from_file(file):
    """
    Extract words from a text file.
    :param file: Path to the text file.
    :return: List of words in the file.
    """
    with open(file, 'r') as f:
        text = f.read().lower()  # Convert to lowercase for consistency
        return text.split()  # Split text into words

def build_word_graph(words, matched_words):
    """
    Build a graph where nodes are words and edges represent consecutive word relationships.
    Only include words that are in the matched_words set.
    :param words: List of words.
    :param matched_words: Set of matched words to include in the graph.
    :return: A dictionary representing the filtered graph.
    """
    graph = {}
    for i in range(len(words) - 1):
        word1, word2 = words[i], words[i + 1]
        if word1 in matched_words and word2 in matched_words:
            graph.setdefault(word1, []).append(word2)
            graph.setdefault(word2, [])
    return graph

def visualize_word_graph_with_traversal(graph, traversal_order, stop_flag):
    """
    Visualize the word network using Matplotlib with traversal visualization.
    :param graph: Dictionary representing the word graph.
    :param traversal_order: List of nodes in the order they are visited during traversal.
    :param stop_flag: A flag to stop the traversal.
    """
    nodes = list(graph.keys())
    num_nodes = len(nodes)
    angle_step = 360 / num_nodes
    node_positions = {
        node: (10 * cos(i * angle_step * pi / 180), 10 * sin(i * angle_step * pi / 180)) # convert to radians
        for i, node in enumerate(nodes)
    }
    node_radius = 0.5

    plt.figure(figsize=(12, 10))
    for i, current_node in enumerate(traversal_order):
        if stop_flag():  # Check if the stop button was pressed
            print("Traversal stopped.")
            break

        plt.clf()  # Clear the figure for dynamic updates

        for node, (x, y) in node_positions.items():
            color = "red" if node == current_node else "skyblue"
            plt.scatter(x, y, s=1100, color=color, zorder=2)
            plt.text(x, y, node, fontsize=8, ha="center", va="center", zorder=3)

        for source, targets in graph.items():
            x1, y1 = node_positions[source]
            for target in targets:
                x2, y2 = node_positions[target]
                dx, dy = x2 - x1, y2 - y1
                distance = (dx**2 + dy**2)**0.5
                arrow_length = distance - node_radius
                dx_scaled = dx * (arrow_length / distance)
                dy_scaled = dy * (arrow_length / distance)
                plt.arrow(
                    x1, y1, dx_scaled, dy_scaled,
                    head_width=0.3, head_length=0.5, fc="black", ec="black",
                    length_includes_head=True, zorder=1
                )

        plt.title(f"Traversal Visualization: Step {i + 1}/{len(traversal_order)}")
        plt.axis("off")
        plt.pause(1)

    plt.show()

def bfs(graph, start):
    """
    Breadth-First Search to traverse the graph.
    :param graph: Dictionary representing the word graph.
    :param start: Starting node for BFS.
    :return: List of nodes in the order they are visited.
    """
    visited = set()
    queue = deque([start])
    traversal_order = []  # List to store the traversal order

    while queue:
        node = queue.popleft()
        if node not in visited:
            traversal_order.append(node)  # Add node to traversal order
            visited.add(node)
            queue.extend(neighbor for neighbor in graph.get(node, []) if neighbor not in visited)

    return traversal_order

def dfs(graph, node, visited=None, traversal_order=None):
    """
    Depth-First Search to traverse the graph.
    :param graph: Dictionary representing the word graph.
    :param node: Starting node for DFS.
    :param visited: Set of visited nodes (used for recursion).
    :param traversal_order: List of nodes in the order they are visited.
    :return: List of nodes in the order they are visited.
    """
    if visited is None:
        visited = set()
    if traversal_order is None:
        traversal_order = []

    if node not in visited:
        visited.add(node)  # Mark the node as visited
        traversal_order.append(node)  # Add node to traversal order

        # Recursively visit each unvisited neighbor
        for neighbor in graph.get(node, []):
            dfs(graph, neighbor, visited, traversal_order)

    return traversal_order