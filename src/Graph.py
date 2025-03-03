from node import Node
from typing import Dict

class Graph:
  def __init__(self):
    self.nodes: Dict[str, Node] = {}

  def add_node(self, name: str, genre: str, dancers: set):
    if name not in self.nodes:
      self.nodes[name] = Node(name, genre, dancers)
    return self.nodes[name]

  def add_edge(self, name1: str, dancers1: set, name2: str, dancers2: set, weight: float):
    if name1 not in self.nodes:
      self.add_node(name1, dancers1)
    if name2 not in self.nodes:
      self.add_node(name2, dancers2)
    
    node1 = self.nodes[name1]
    node2 = self.nodes[name2]
    node1.add_edge(node2, weight)
    node2.add_edge(node1, weight)

  def __repr__(self):
    string = ""
    for node in self.nodes.values():
      string += f"{node.name}: {[(neighbor.name, weight) for neighbor, weight in node.edges.items()]}\n"
    return string