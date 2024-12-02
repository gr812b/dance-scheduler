
# The problem
In dance competitions or performances, ensuring a smooth schedule is crucial for both performers and event organizers. One common challenge is arranging the order of dances so that no performer is required to participate in consecutive or "back-to-back" performances. This scheduling constraint helps dancers avoid fatigue and allows them adequate time for costume changes, preparation, or rest.

## Reducing to a graph problem
The problem can be represented as an undirected graph where:

- Each node represents a dance, which tracks a list of participating dancers.
- An edge that exists between two nodes indicates that they may be scheduled consecutively.

This then allows one to traverse the graph. If it is fully connected, then there exists an optimal solution where no back-to-back conflicts occur. Further, the number of components indicates the number of required back-to-back dances.

## Optimizing the order
While knowing that an optimal solution exists, or how many back-to-back dances are required may be helpful, generating an optimal path is far more ideal. Here, we define heuristics for both cases.

### Case 1 - Fully Connected
When the graph is fully connected, an optimal solution can be found using Depth-First Search (DFS) or Breadth-First Search (BFS) to traverse the graph. However, to generate a schedule that maximizes the overall experience, the following heuristics can be considered:

- Genre Diversity: Avoid scheduling consecutive dances of the same genre (e.g., Jazz, Heels, Contemporary).
- Performance Dynamics: Alternate between high-energy and low-energy performances to create a balanced flow for the audience.
- Dancer Workload: Minimize consecutive performances for dancers appearing frequently across multiple dances.
- Transition Time: Prioritize pairings of dances that require minimal stage setup changes.

These heuristics can further be applied independently to each connected component of the graph.

### Case 2 - Two (or more) components
If the graph has two or more disconnected components, additional "back-to-back" edges must be introduced to connect these components and form a schedule. The key is to minimize the impact of these back-to-back dances by using the following strategies:

- Minimize Overlapping Dancers: Choose nodes from different components to connect, ensuring that the overlap of dancers is as small as possible.
- Consider Genre Transitions: Select dances with complementary genres or themes to create a natural flow despite the back-to-back nature.
- Spread Workload Equally: Distribute the additional burden of back-to-back scheduling across the least-frequent performers.

By carefully selecting these connecting edges, the overall quality of the schedule can be preserved while meeting the constraints.


### Implementing the Solution
With the heuristics defined, the optimal schedule can be generated by running a Minimum Spanning Tree (MST) algorithm on the graph. Here's how the process works:

1. Weight Assignment: Assign weights to edges based on the defined heuristics, where lower weights represent better pairings.
2. MST Calculation: Use algorithms such as Kruskal's or Prim's to find the MST of the graph, ensuring an optimal set of connections.
3. Schedule Traversal: Perform a DFS or BFS traversal of the resulting MST to generate the dance sequence.