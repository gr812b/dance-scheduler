from Node import Node

class Graph:
  def __init__(self):
    self.nodes = {}

  def add_node(self, name, dancers):
    if name not in self.nodes:
      self.nodes[name] = Node(name, dancers)
    return self.nodes[name]

  def add_edge(self, name1, dancers1, name2, dancers2):
    if name1 not in self.nodes:
      self.add_node(name1, dancers1)
    if name2 not in self.nodes:
      self.add_node(name2, dancers2)
    
    node1 = self.nodes[name1]
    node2 = self.nodes[name2]
    node1.add_edge(node2)
    node2.add_edge(node1)

  def connected_components(self):
    visited = set()
    components = []

    def dfs(node, component):
      visited.add(node)
      component.append(node)
      for neighbor in node.edges:
        if neighbor not in visited:
          dfs(neighbor, component)

    for node in self.nodes.values():
      if node not in visited:
        component = []
        dfs(node, component)
        components.append(component)

    return components

  def __str__(self):
    return str(self.nodes)