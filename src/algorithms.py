from node import Node
from graph import Graph
from typing import Optional, Set, List, Tuple
import heapq
import random

def dfs(node: Node, visited: Set[Node], component: List[Node]) -> None:
  visited.add(node)
  component.append(node)
  
  for neighbor, weight in node.edges.items():
    if weight == 0 and neighbor not in visited:  # Only traverse edges with weight 0
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

def prim_mst(graph: Graph, enableRandom = False, startNode: Optional[Node] = None) -> List[Tuple[Node, Node, float]]:
  mst_edges: List[Tuple[Node, Node, float]] = []
  visited: Set[Node] = set()
  edge_heap: List[Tuple[float, Node, Node]] = []

  # Start with an arbitrary node
  start_node = startNode if startNode else (random.choice(list(graph.nodes.values())) if enableRandom else next(iter(graph.nodes.values())))
  visited.add(start_node)

  # Add all edges from the start node to the heap
  for neighbor, weight in start_node.edges.items():
    heapq.heappush(edge_heap, (weight, start_node, neighbor))

  # Grow the MST
  while edge_heap and len(visited) < len(graph.nodes):
    # Pop the smallest edge
    weight, node1, node2 = heapq.heappop(edge_heap)

    # If the edge connects to a new node, add it to the MST
    if node2 not in visited:
      visited.add(node2)
      mst_edges.append((node1, node2, weight))

      # Push all edges from the newly added node
      for neighbor, weight in node2.edges.items():
        if neighbor not in visited:
          heapq.heappush(edge_heap, (weight, node2, neighbor))

  return mst_edges

def extract_order_from_mst(mst_edges: List[Tuple[Node, Node, float]], start_node: Node) -> List[Node]:
    # Build an adjacency list for the tree
    tree = {node: [] for node in [start_node] + [n for edge in mst_edges for n in edge[:2]]}
    for u, v, weight in mst_edges:
        tree.setdefault(u, []).append(v)
        tree.setdefault(v, []).append(u)

    order = []
    visited = set()

    def dfs(node: Node):
        visited.add(node)
        order.append(node)
        for neighbor in tree[node]:
            if neighbor not in visited:
                dfs(neighbor)

    dfs(start_node)
    return order

