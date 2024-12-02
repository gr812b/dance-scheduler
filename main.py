from Graph import Graph
from Node import Node
from Read_Csv import read_csv

def main():
  # Read in the csv file
  dance_data = read_csv("dances2.csv")
  
  # Create a graph
  graph = Graph()
  
  # Add nodes to the graph
  for dance in dance_data:
    graph.add_node(dance, dance_data[dance])
  
  # Add edges to graph that connect dances that have no dancers in common
  for dance1 in dance_data:
    for dance2 in dance_data:
      if dance1 != dance2 and not set(dance_data[dance1]).intersection(dance_data[dance2]):
        graph.add_edge(dance1, dance_data[dance1], dance2, dance_data[dance2])
  
  # Print the graph
  for node in graph.nodes:
    print(node, graph.nodes[node].edges)

  components = graph.connected_components()
  print("Connected Components:", components)
  print("Minimum Back-to-Back Dances:", len(components) - 1)

if __name__ == "__main__":
  main()