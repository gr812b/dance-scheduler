from data_reader import load_graph
from algorithms import find_connected_components, prim_mst, extract_order_from_mst
from heuristics import weight_function


def main():
  filepath = "./data/winter_dances.csv"
  graph = load_graph(filepath, weight_function)

  print(graph)

  components = find_connected_components(graph)
  print("Connected Components:", components)
  print("Minimum Back-to-Back Dances:", len(components) - 1)

  # Build MST to connect components
  start_node = graph.nodes["FEEL THE BEAT"]
  mst_edges = prim_mst(graph, True, start_node)
  print("Minimum Spanning Tree to Connect Components:", mst_edges)
  print("Total Weight of MST:", sum(weight for _, _, weight in mst_edges))

  dance_order = extract_order_from_mst(mst_edges, start_node)
  print("Edges:", [(edge[0].name, edge[1].name, edge[2]) for edge in mst_edges])
  print("Dance Order:", [dance.name for dance in dance_order])
  

if __name__ == "__main__":
  main()