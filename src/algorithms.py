from node import Node
from graph import Graph
from typing import Set, List

def dfs(node: Node, visited: Set[Node], component: List[Node]) -> None:
  visited.add(node)
  component.append(node)
  for neighbor in node.edges:
    if neighbor not in visited:
      dfs(neighbor, visited, component)

def find_connected_components(graph: Graph) -> List[List[Node]]:
  visited = set()
  components = []
  for node in graph.nodes.values():
    if node not in visited:
      component = []
      dfs(node, visited, component)
      components.append(component)
  return components