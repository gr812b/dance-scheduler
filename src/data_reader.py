import csv
import os
from graph import Graph
from node import Node
from typing import Dict, Optional, Set, Callable

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
  
def load_graph(filepath: str, weight_fcn: Callable[[Node, Node], float],
               k: Optional[int] = None, threshold: Optional[float] = None) -> Graph:
    dance_data = read_csv(filepath)
    graph = Graph()
    
    # Add all nodes.
    for dance in dance_data:
        graph.add_node(dance, dance_data[dance])
    
    # For each dance (node), compute and add only the best edges.
    for dance1 in dance_data:
        candidate_edges = []
        for dance2 in dance_data:
            if dance1 == dance2:
                continue
            weight = weight_fcn(graph.nodes[dance1], graph.nodes[dance2])
            candidate_edges.append((dance2, weight))
        
        # Apply threshold filtering if a threshold is given.
        if threshold is not None:
            candidate_edges = [(d, w) for d, w in candidate_edges if w < threshold]
        
        # Apply k-nearest filtering if k is given.
        if k is not None:
            candidate_edges.sort(key=lambda x: x[1])
            candidate_edges = candidate_edges[:k]
        
        # Add the selected edges for dance1.
        for dance2, weight in candidate_edges:
            graph.add_edge(dance1, dance_data[dance1], dance2, dance_data[dance2], weight)
    
    return graph

def update_dance_csv(csv_filename: str, dance_name: str, genre: str, dancer_list: list):
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
        header = ['Dance', 'Genre']
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
    new_row[1] = genre  # Set the genre
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
    csv_file = 'data/winter_dances_good.csv'

    # Input data
    dance_name = "INT CONTEMP"
    genre = "Contemporary"
    dancer_list_str = """
Emily Corturillo
Leshelle Tate
Abigail Altosaar
Agassi Iu
madi parsons
Heather Booth
Jamie Smith
Ava McConnell
Sami Poulsen
Kate Craig
Aryana Jebely
Kalia Rivera
Madison McGuire
Sara Thoeny
Nikol Pintea
Aspen Maciel
Olivia Alvey
bella verdugo
Cassy Brown
Hannah Dietrich
Jerome EBRARD
Olivia Furman
Carlie Stubbert
Emma Shapland
Abbey Jean
Léonie FELDMANN
    """
    # Clean and split the dancer list
    dancer_list = [name.strip().casefold() for name in dancer_list_str.strip().split('\n')]

    # Update the CSV
    update_dance_csv(csv_file, dance_name, genre, dancer_list)