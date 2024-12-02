# CSV input will have a names column on the left for the name of the dance, and then a column for each dancer.
# ex: name, alice, bob, charlie
#     waltz, 1, 1, 1
#     tango, 0, 0, 1
# Goal is to read this in to a dictionary with the name of the dance as the key, and a list of the dancers as the value.
# ex: {"waltz": [alice, bob, charlie], "tango": [charlie]}

import csv

def read_csv(file):
  with open(file, newline='') as csvfile:
    reader = csv.reader(csvfile)
    data = list(reader)

    header = data[0]
    data = data[1:]

    dance_data = {}

    for row in data:
      dance_name = row[0]

      dancers = []
      for i in range(1, len(row)):
        if row[i] == "1":
          dancers.append(header[i])

      dance_data[dance_name] = dancers

    return dance_data