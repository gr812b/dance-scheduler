from node import Node
from graph import Graph
from typing import Dict, Optional, Set, List, Tuple
import heapq
import random
import math
import time
import sys

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
        neighbors = tree[node][:]
        random.shuffle(neighbors)
        for neighbor in neighbors:
            if neighbor not in visited:
                dfs(neighbor)

    dfs(start_node)
    return order


def held_karp(graph: 'Graph', start: Optional['Node'] = None, randomize: bool = False, epsilon: float = 0.01) -> Tuple[float, List['Node']]:
    """
    Solve the Hamiltonian path problem using the Held-Karp algorithm.
    Returns a tuple (cost, path) where:
      - cost is the total (possibly perturbed) cost to cover all nodes,
      - path is the list of nodes (in order) achieving that cost.
      
    If randomize is True, a small random multiplier (±epsilon) is applied to each edge's weight.
    """
    # Create a list of nodes and ensure the start node is at index 0.
    nodes = list(graph.nodes.values())
    if start is None:
        start = nodes[0]
    else:
        if start not in nodes:
            raise ValueError("Start node is not in the graph.")
    # Reorder nodes so that start is at index 0.
    start_index = nodes.index(start)
    nodes[0], nodes[start_index] = nodes[start_index], nodes[0]
    n = len(nodes)

    # Build a distance matrix (using math.inf if an edge is missing).
    dist = [[math.inf] * n for _ in range(n)]
    for i, node in enumerate(nodes):
        for j, other in enumerate(nodes):
            if i == j:
                dist[i][j] = 0
            elif other in node.edges:
                dist[i][j] = node.edges[other]

    # dp[(mask, j)] = (cost, parent)
    dp: Dict[Tuple[int, int], Tuple[float, Optional[int]]] = {}
    dp[(1 << 0, 0)] = (0, None)

    total_masks = 1 << n  # Total number of subsets
    progress_interval = max(total_masks // 100, 1)  # update every ~1%

    start_time = time.time()

    # Iterate over all subsets (bitmask representations)
    for mask in range(1, total_masks):
        # Print progress every ~1%
        if mask % progress_interval == 0:
            progress = mask / total_masks * 100
            elapsed = time.time() - start_time
            sys.stdout.write(f"\rProgress: {progress:.2f}% (mask {mask} of {total_masks}, elapsed {elapsed:.1f}s)")
            sys.stdout.flush()

        # Skip masks that don't include the start node (bit 0)
        if not (mask & 1):
            continue

        for j in range(n):
            if not (mask & (1 << j)):
                continue
            if (mask, j) not in dp:
                continue
            current_cost, _ = dp[(mask, j)]
            # Try to extend the path to every node k not in mask.
            for k in range(n):
                if mask & (1 << k):
                    continue
                new_mask = mask | (1 << k)
                base_weight = dist[j][k]
                # Optionally perturb the edge weight.
                if randomize:
                    perturbed_weight = base_weight * (1 + random.uniform(-epsilon, epsilon))
                else:
                    perturbed_weight = base_weight
                new_cost = current_cost + perturbed_weight
                if (new_mask, k) not in dp or new_cost < dp[(new_mask, k)][0]:
                    dp[(new_mask, k)] = (new_cost, j)

    print("\nFinished processing DP states.")

    # Find the best cost path that visits all nodes.
    full_mask = (1 << n) - 1
    best_cost = math.inf
    best_end = None
    for j in range(n):
        if (full_mask, j) in dp and dp[(full_mask, j)][0] < best_cost:
            best_cost = dp[(full_mask, j)][0]
            best_end = j

    if best_end is None:
        raise Exception("No Hamiltonian path found.")

    # Reconstruct the optimal path by backtracking.
    path_indices = []
    mask = full_mask
    j = best_end
    while j is not None:
        path_indices.append(j)
        _, parent = dp[(mask, j)]
        mask = mask & ~(1 << j)
        j = parent
    path_indices.reverse()
    optimal_path = [nodes[i] for i in path_indices]
    return best_cost, optimal_path




def held_karp_top_k(graph: 'Graph', start: Optional['Node'] = None, top_k: int = 5, candidate_limit: int = 10) -> List[Tuple[float, List['Node']]]:
    """
    Solve the Hamiltonian path problem using a modified Held-Karp algorithm that keeps
    multiple candidate solutions per state. Returns a list of tuples (cost, path) for the top_k
    solutions (sorted by cost). In cases where many solutions are equivalent (e.g. all cost 0),
    this will return a sample of up to top_k different orderings.
    
    Parameters:
      - graph: The graph.
      - start: Optional start node (if not provided, an arbitrary node is used).
      - top_k: How many final paths to return.
      - candidate_limit: How many candidate solutions to store per DP state.
    """
    # Create a list of nodes and ensure the start node is at index 0.
    nodes = list(graph.nodes.values())
    if start is None:
        start = nodes[0]
    else:
        if start not in nodes:
            raise ValueError("Start node is not in the graph.")
    start_index = nodes.index(start)
    nodes[0], nodes[start_index] = nodes[start_index], nodes[0]
    n = len(nodes)
    
    # Build a distance matrix; if an edge is missing, use math.inf.
    dist = [[math.inf] * n for _ in range(n)]
    for i, node in enumerate(nodes):
        for j, other in enumerate(nodes):
            if i == j:
                dist[i][j] = 0
            elif other in node.edges:
                dist[i][j] = node.edges[other]
    
    # dp[(mask, j)] = list of (cost, parent) candidates reaching state (mask, j).
    dp: Dict[Tuple[int, int], List[Tuple[float, Optional[int]]]] = {}
    dp[(1 << 0, 0)] = [(0, None)]
    
    total_masks = 1 << n
    progress_interval = max(total_masks // 100, 1)
    start_time = time.time()
    
    # Iterate over all subsets (bitmask representations)
    for mask in range(1, total_masks):
        if mask % progress_interval == 0:
            progress = mask / total_masks * 100
            elapsed = time.time() - start_time
            sys.stdout.write(f"\rDP Progress: {progress:.2f}% (mask {mask} of {total_masks}, elapsed {elapsed:.1f}s)")
            sys.stdout.flush()
        # Only consider masks that include the start node.
        if not (mask & 1):
            continue
        for j in range(n):
            if not (mask & (1 << j)):
                continue
            state = (mask, j)
            if state not in dp:
                continue
            # For each candidate reaching this state...
            for (cost, parent) in dp[state]:
                # Try extending to every node not yet visited.
                for k in range(n):
                    if mask & (1 << k):
                        continue
                    new_mask = mask | (1 << k)
                    new_cost = cost + dist[j][k]
                    candidate = (new_cost, j)
                    new_state = (new_mask, k)
                    if new_state not in dp:
                        dp[new_state] = [candidate]
                    else:
                        dp[new_state].append(candidate)
                        # Sort and prune to candidate_limit best candidates.
                        dp[new_state] = sorted(dp[new_state], key=lambda x: x[0])[:candidate_limit]
    
    print("\nFinished processing DP states.")
    
    full_mask = (1 << n) - 1
    final_candidates = []
    for j in range(n):
        state = (full_mask, j)
        if state in dp:
            for cand in dp[state]:
                final_candidates.append((cand[0], j))
    final_candidates = sorted(final_candidates, key=lambda x: x[0])
    top_final = final_candidates[:top_k]
    
    # Backtracking: recursively reconstruct all candidate paths for a given state.
    # This function returns a list of paths (each path is a list of node indices).
    def reconstruct_paths(mask: int, j: int) -> List[List[int]]:
        # Base case: if mask contains only node j.
        if mask == (1 << j):
            if j == 0:
                return [[0]]
            else:
                return []  # should not happen because we always include start.
        paths = []
        prev_mask = mask & ~(1 << j)
        # Look at all candidates that led to (mask, j).
        for (cost, parent) in dp.get((mask, j), []):
            if parent is None:
                continue
            # Recursively reconstruct paths for the previous state.
            for subpath in reconstruct_paths(prev_mask, parent):
                paths.append(subpath + [j])
        return paths
    
    # Reconstruct full paths for the top final states.
    top_paths = []
    for final_cost, final_j in top_final:
        candidate_paths = reconstruct_paths(full_mask, final_j)
        for path_indices in candidate_paths:
            path = [nodes[i] for i in path_indices]
            top_paths.append((final_cost, path))
            if len(top_paths) >= top_k:
                break
        if len(top_paths) >= top_k:
            break
    
    return top_paths