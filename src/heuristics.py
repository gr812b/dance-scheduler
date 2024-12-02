from node import Node

def calculate_overlap(node1: Node, node2: Node):
    return len(node1.dancers & node2.dancers)

def weight_function(node1: Node, node2: Node):
    # Example weight: minimize overlap
    return calculate_overlap(node1, node2)