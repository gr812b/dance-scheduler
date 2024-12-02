import csv
from graph import Graph
from typing import Dict, Set

# CSV input will have a names column on the left for the name of the dance, and then a column for each dancer.
# ex: name, alice, bob, charlie
#     waltz, 1, 1, 1
#     tango, 0, 0, 1
# Goal is to read this in to a dictionary with the name of the dance as the key, and a list of the dancers as the value.
# ex: {"waltz": [alice, bob, charlie], "tango": [charlie]}

def read_csv(filepath: str) -> Dict[str, Set[str]]:
  with open(filepath, newline='') as csvfile:
    reader = csv.reader(csvfile)
    data = list(reader)

    header = data[0]
    data = data[1:]

    dance_data = {}

    for row in data:
      dance_name = row[0]

      dancers = set()
      for i in range(1, len(row)):
        if row[i] == "1":
          dancers.add(header[i])

      dance_data[dance_name] = dancers

    return dance_data
  
def load_graph(filepath: str) -> Graph:
  dance_data = read_csv(filepath)
  
  graph = Graph()
  
  # Add all nodes
  for dance in dance_data:
    graph.add_node(dance, dance_data[dance])
  
  # Add valid edges
  for dance1 in dance_data:
    for dance2 in dance_data:
      if dance1 != dance2 and not dance_data[dance1].intersection(dance_data[dance2]):
        graph.add_edge(dance1, dance_data[dance1], dance2, dance_data[dance2])
  
  return graph