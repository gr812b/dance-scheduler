from data_reader import load_graph
from algorithms import find_connected_components, prim_mst
from heuristics import weight_function


def main():
  filepath = "./data/dance_performances.csv"
  graph = load_graph(filepath, weight_function)

  print(graph)

  components = find_connected_components(graph)
  print("Connected Components:", components)
  print("Minimum Back-to-Back Dances:", len(components) - 1)

  # Build MST to connect components
  mst = prim_mst(graph, True)
  print("Minimum Spanning Tree to Connect Components:", mst)
  print("Total Weight of MST:", sum(weight for _, _, weight in mst))

if __name__ == "__main__":
  main()