class Node:
  def __init__(self, name, dancers):
    self.name = name
    self.dancers = dancers
    self.edges = []

  def add_edge(self, edge):
    if edge not in self.edges:
      self.edges.append(edge)

  def remove_edge(self, edge):
    if edge in self.edges:
      self.edges.remove(edge)

  def __str__(self):
    return self.name
  
  def __repr__(self):
    return self.name
  
  def __eq__(self, other):
    return self.name == other.name
  
  def __hash__(self):
    return hash(self.name)