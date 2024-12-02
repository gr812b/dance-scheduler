from graph import Graph
from data_reader import load_graph
from algorithms import find_connected_components

def main():
  filepath = "./data/dances2.csv"
  graph = load_graph(filepath)

  print(graph)

  components = find_connected_components(graph)
  print("Connected Components:", components)
  print("Minimum Back-to-Back Dances:", len(components) - 1)

if __name__ == "__main__":
  main()