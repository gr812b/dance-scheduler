from typing import Dict

class Node:
  def __init__(self, name: str, dancers: set):
    self.name = name
    self.dancers = dancers
    self.edges: Dict[Node, float] = {}

  def add_edge(self, neighbor, weight):
    self.edges[neighbor] = weight

  def remove_edge(self, neighbor):
    if neighbor in self.edges:
      del self.edges[neighbor]
  
  def __repr__(self):
    return self.name
  
  def __eq__(self, other):
    return self.name == other.name
  
  def __hash__(self):
    return hash(self.name)

  def __lt__(self, other):
    return self.name < other.name