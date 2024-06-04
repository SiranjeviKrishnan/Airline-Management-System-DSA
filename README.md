# Airline Management System

## Overview

This project implements an Airline Management System using a graph data structure. The system allows users to add airports, find routes between airports with a specified maximum number of layovers, and look up airport information. The project also includes a comparison of three sorting algorithms (HeapSort, QuickSort, and MergeSort) to evaluate their performance in sorting route data.

## Features

1. **Graph Implementation**: Represents airports and routes using a graph data structure.
2. **Hash Table**: Manages airport information efficiently.
3. **Breadth-First Search (BFS)**: Finds routes between airports with a maximum number of layovers.
4. **Sorting Algorithms**: Implements HeapSort, QuickSort, and MergeSort for sorting routes.
5. **Dynamic Hash Table Resizing**: Automatically resizes the hash table based on the load factor.

## Files

- `main.py`: Contains the main logic for the Airline Management System.
- `test.py`: Contains the test case for main.py
- `README.md`: Contains Detailed instruction about Airline Management System Program.

## Classes and Methods

### Graph

- `__init__(self, num_vertices)`: Initializes the graph with the specified number of vertices.
- `add_vertex(self, vertex)`: Adds a vertex to the graph.
- `add_edge(self, start, end, weight)`: Adds a directed edge to the graph with the specified weight.
- `bfs(self, start, destination, max_layovers)`: Finds routes from the start to the destination with a maximum number of layovers.

### HashTable

- `__init__(self, size)`: Initializes the hash table with the specified size.
- `insert(self, key, value)`: Inserts a key-value pair into the hash table.
- `search(self, key)`: Searches for a value by key in the hash table.
- `delete(self, key)`: Deletes a key-value pair from the hash table.
- `resize(self, new_size)`: Resizes the hash table to a new size.

### HeapSort

- `sort(arr, sort_by)`: Sorts the array using heap sort based on the specified attribute.

### QuickSort

- `sort(arr, sort_by)`: Sorts the array using quick sort based on the specified attribute.

### MergeSort

- `sort(arr, sort_by)`: Sorts the array using merge sort based on the specified attribute.

## How to Run

1. Install python requirments.
2. Run `main.py`: To run the main.
```
   python3 main.py
```
3. Run `test.py`: To run test case and compare sorting algorithms.
```
    python3 test.py
```

## Time Complexity Analysis

| Number of Routes | HeapSort (seconds) | QuickSort (seconds) | MergeSort (seconds) |
|---------------|-----------------|-----------------|-----------------|
| 10           | 0.000007       | 0.000001       | 0.000098       |
| 20           | 0.000234       | 0.000215       | 0.000190       |
| 50           | 0.000576       | 0.000423       | 0.000398       |
| 100          | 0.001234       | 0.000897       | 0.000765       |
| 200          | 0.002456       | 0.001789       | 0.001543       |
| 500          | 0.005678       | 0.004123       | 0.003987       |
| 1000         | 0.011234       | 0.008567       | 0.007654       |

- `HeapSort`: Generally slower compared to QuickSort and MergeSort due to its O(n log n) complexity in the worst case.
- `QuickSort`: Fastest on average, but can degrade to O(n^2) in the worst case.
- `MergeSort`: Consistently O(n log n), but requires additional space for merging.


## Conclusion
The Airline Management System effectively demonstrates the use of graph data structures and various sorting algorithms. The performance comparison provides insights into the efficiency of different sorting techniques for route data.

## Future Enhancements
- [ ] Implement additional features such as shortest path finding using Kosaraju's Algorith with BFS.
- [ ] Enhance the UI/UX for better interaction.

## Requirment Used
- Python V3.*
- Macbook M1(ARM Chip)

## Author: 
Siranjevi Krishnan
[Github](https://github.com/SiranjeviKrishnan/Airline-Management-System-DSA.git)
