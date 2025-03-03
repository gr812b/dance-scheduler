from node import Node

def calculate_overlap(node1: Node, node2: Node):
    return len(node1.dancers & node2.dancers)

def calculate_similar_genre(node1: Node, node2: Node):
    if node1.genre == node2.genre:
        return 1
    return 0

def weight_function(node1: Node, node2: Node):
    # Example weight: minimize overlap
    return calculate_overlap(node1, node2) + 2*calculate_similar_genre(node1, node2)

# Intructor dance first
# Feel the beat MUST BE SECOND
# Last must be advanced dance
# After Feel the beat, must be advanced

# Remember intermission is a break

# No stalls - 85
# Same genre - 92
# Same level (no level = intermediate) - 65
# Even distribution (suuure) - 40
