import csv
import os
from graph import Graph
from node import Node
from typing import Dict, Set, Callable

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
  
def load_graph(filepath: str, weight_fcn: Callable[[Node, Node], float]) -> Graph:
  dance_data = read_csv(filepath)
  
  graph = Graph()
  
  # Add all nodes
  for dance in dance_data:
    graph.add_node(dance, dance_data[dance])
  
  # Add initial edges with weight 0
  for dance1 in dance_data:
    for dance2 in dance_data:
      if dance1 != dance2:
        weight = weight_fcn(graph.nodes[dance1], graph.nodes[dance2])
        graph.add_edge(dance1, dance_data[dance1], dance2, dance_data[dance2], weight)
  
  return graph

def update_dance_csv(csv_filename, dance_name, dancer_list):
    # Check if the CSV file exists
    if os.path.exists(csv_filename):
        # Read existing data
        with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            header = data[0]
            rows = data[1:]
    else:
        # Initialize header and rows
        header = ['Dance']
        rows = []

    # Update the list of dancers in the header
    for dancer in dancer_list:
        if dancer not in header:
            header.append(dancer)
            # Add '0' to existing rows for the new dancer
            for row in rows:
                row.append('0')

    # Create a new row for the current dance
    new_row = ['0'] * len(header)
    new_row[0] = dance_name  # Set the dance name
    for dancer in dancer_list:
        index = header.index(dancer)
        new_row[index] = '1'  # Mark dancer as present in this dance

    # Append the new row to the rows
    rows.append(new_row)

    # Write the updated data back to the CSV
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(rows)

if __name__ == "__main__":
    csv_file = 'dance_performances.csv'

    # Input data
    dance_name = "ALTER EGO - Advanced Heels"
    dancer_list_str = """
Abby Altosaar, Aryana Jebely, Aspen Maciel, Brooke Pocock, Chloe Poulter, Elizabeth Estabrooks, Emily Corturillo, Isabelle Hatzimalis, Jaidyn Smith, Jamie Smith, Jennifer Gibson, Kalia Rivera, Kay Lavery, Kayla Burton, Kealey Parliament, Lauren Conrod, Leshelle Tate, Lexis Vincent, Mariah Gribowski, Marissa Laird, Mikayla Weagle, Natalie Reaume, Noa Mortensen, Priya Sharma, Quiana Fernandes, Sarah Elmugamar, Tiffany Locsin, Tori Reay"""
    # Clean and split the dancer list
    dancer_list = [name.strip() for name in dancer_list_str.strip().split(',')]

    # Update the CSV
    update_dance_csv(csv_file, dance_name, dancer_list)