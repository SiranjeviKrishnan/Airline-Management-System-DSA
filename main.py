import numpy as np

class Graph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.vertices = np.full((num_vertices,), fill_value='', dtype='U3')
        self.adj_list = np.empty((num_vertices,), dtype=object)
        for i in range(num_vertices):
            self.adj_list[i] = np.array([], dtype=np.dtype([('dest', 'U3'), ('weight', int)]))
        self.vertex_count = 0

    def add_vertex(self, vertex):
        if self.vertex_count < self.num_vertices:
            self.vertices[self.vertex_count] = vertex
            self.vertex_count += 1
        else:
            print("Graph is full.")

    def _get_vertex_index(self, vertex):
        index = np.where(self.vertices == vertex)[0]
        if index.size > 0:
            return int(index[0])
        return -1

    def load_csv(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    start, end, weight = line.strip().split(',')
                    self.add_edge(start, end, int(weight))
        except Exception as e:
            print(f"Error reading file {filename}: {e}")

    def add_edge(self, start, end, weight):
        start_index = self._get_vertex_index(start)
        end_index = self._get_vertex_index(end)
        if start_index != -1 and end_index != -1:
            self.adj_list[start_index] = np.append(self.adj_list[start_index], np.array([(end, weight)], dtype=np.dtype([('dest', 'U3'), ('weight', int)])))

    def bfs(self, start, destination, max_layovers):
        start_index = self._get_vertex_index(start)
        destination_index = self._get_vertex_index(destination)
        if start_index == -1 or destination_index == -1:
            return np.array([], dtype=np.dtype([('path', 'O'), ('layovers', int), ('distance', int)]))
        
        queue = np.array([(start_index, np.array([start_index], dtype=int), 0)], dtype=np.dtype([('airport', int), ('path', 'O'), ('distance', int)]))
        routes = np.array([], dtype=np.dtype([('path', 'O'), ('layovers', int), ('distance', int)]))

        while queue.size > 0:
            current_airport, path, distance = queue[0]
            queue = np.delete(queue, 0)

            if current_airport == destination_index:
                route_path = self.vertices[path]
                routes = np.append(routes, np.array([(route_path, path.size - 1, distance)], dtype=np.dtype([('path', 'O'), ('layovers', int), ('distance', int)])))

            if path.size <= max_layovers + 1:
                for neighbor in self.adj_list[current_airport]:
                    neighbor_index = self._get_vertex_index(neighbor['dest'])
                    if neighbor_index != -1 and neighbor_index not in path:
                        new_path = np.append(path, neighbor_index)
                        new_distance = distance + neighbor['weight']
                        queue = np.append(queue, np.array([(neighbor_index, new_path, new_distance)], dtype=np.dtype([('airport', int), ('path', 'O'), ('distance', int)])))
        return routes

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = np.empty((size,), dtype=object)
        self.item_count = 0

    def hash_function(self, key):
        sum_ascii = np.sum(np.frombuffer(key.encode(), dtype=np.uint8))
        return int(sum_ascii % self.size)
    
    def linear_probe(self, index, probe_count):
        return int((index + probe_count) % self.size)

    def insert(self, key, value):
        if self.item_count + 1 > 0.75 * self.size:
            self.resize(self.size * 2)

        index = self.hash_function(key)
        probe_count = 0
        while self.table[index] is not None and self.table[index][0] != key:
            probe_count += 1
            index = self.linear_probe(index, probe_count)
        if self.table[index] is None:
            self.item_count += 1
        self.table[index] = (key, value)

    def search(self, key):
        index = self.hash_function(key)
        probe_count = 0
        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]
            probe_count += 1
            index = self.linear_probe(index, probe_count)
        return None

    def delete(self, key):
        index = self.hash_function(key)
        probe_count = 0
        while self.table[index] is not None:
            if self.table[index][0] == key:
                self.table[index] = None
                self.item_count -= 1
                if self.item_count < 0.5 * self.size and self.size > 1:
                    self.resize(max(1, self.size // 2))
                return
            probe_count += 1
            index = self.linear_probe(index, probe_count)

    def resize(self, new_size):
        old_table = self.table
        self.size = new_size
        self.table = np.empty((new_size,), dtype=object)
        self.item_count = 0
        
        for item in old_table:
            if item is not None:
                key, value = item
                self.insert(key, value)

class HeapSort:
    @staticmethod
    def heapify(arr, n, i, sort_by):
        smallest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and arr[left][sort_by] < arr[smallest][sort_by]:
            smallest = left

        if right < n and arr[right][sort_by] < arr[smallest][sort_by]:
            smallest = right

        if smallest != i:
            arr[i], arr[smallest] = arr[smallest].copy(), arr[i].copy()
            HeapSort.heapify(arr, n, smallest, sort_by)

    @staticmethod
    def sort(arr, sort_by):
        n = arr.size
        for i in np.arange(n // 2 - 1, -1, -1):
            HeapSort.heapify(arr, n, i, sort_by)

        for i in np.arange(n - 1, 0, -1):
            arr[i], arr[0] = arr[0].copy(), arr[i].copy()
            HeapSort.heapify(arr, i, 0, sort_by)

        return arr

def main():
    num_vertices = 5
    airline_graph = Graph(num_vertices)

    try:
        airline_graph.add_vertex("MEL")
        airline_graph.add_vertex("JFK")
        airline_graph.add_vertex("LAX")
        airline_graph.add_vertex("LHR")
        airline_graph.add_vertex("BKK")

        airport_table = HashTable(6)
        airport_table.insert("MEL", "Melbourne Tullamarine (MEL)")
        airport_table.insert("JFK", "John F. Kennedy International Airport")
        airport_table.insert("LAX", "Los Angeles International Airport")
        airport_table.insert("LHR", "London Heathrow Airport")
        airport_table.insert("BKK", "Bangkok Suvarnabhumi Airport")
    except Exception as e:
        print(f"Error initializing data: {e}")

    while True:
        try:
            print("""
            Airline Management System
            1. Find Routes
            2. Lookup Airport Information
            3. Import Data from CSV
            4. Add Airport
            5. Delete Airport
            6. Display Hash Table
            7. Display Graph
            8. Search Airport
            9. Hash Size
            0. Exit
            """)
            choice = input("Enter your choice (0-9): ")

            if choice == "1":
                origin = input("Enter origin airport code: ")
                destination = input("Enter destination airport code: ")
                max_layovers = int(input("Enter maximum number of layovers: "))

                routes = airline_graph.bfs(origin, destination, max_layovers)

                if routes.size == 0:
                    print("No routes found.")
                else:
                    print("\nAvailable Routes:")
                    sort_preference = input("Sort by (1) Travel Distance or (2) Number of Layovers: ")
                    if sort_preference == "1":
                        routes = HeapSort.sort(routes, 2)
                    else:
                        routes = HeapSort.sort(routes, 1)

                    for route in routes:
                        print(f"Route: {'->'.join(route['path'])}, Layovers: {route['layovers']}, Distance: {route['distance']}")

            elif choice == "2":
                airport_code = input("Enter airport code: ")
                airport_info = airport_table.search(airport_code)
                if airport_info:
                    print(f"Airport Information: {airport_info}")
                else:
                    print("Airport not found.")
            
            elif choice == "3":
                filename = input("Enter filename: ")
                airline_graph.load_csv(filename)

            elif choice == "4":
                airport_code = input("Enter airport code: ")
                airport_name = input("Enter airport name: ")
                airline_graph.add_vertex(airport_code)
                airport_table.insert(airport_code, airport_name)

            elif choice == "5":
                airport_code = input("Enter airport code: ")
                airport_index = airline_graph._get_vertex_index(airport_code)
                if airport_index != -1:
                    airline_graph.vertices[airport_index] = ''
                    airport_table.delete(airport_code)
                else:
                    print("Airport not found.")

            elif choice == "6":
                print("Hash Table:")
                for i, item in enumerate(airport_table.table):
                    if item is not None:
                        print(f"{item[0]} - {item[1]}")

            elif choice == "7":
                print("Graph:")
                for i, vertex in enumerate(airline_graph.vertices):
                    print(f"Vertex {i}: {vertex}")
                    for edge in airline_graph.adj_list[i]:
                        print(f"-> {edge['dest']} ({edge['weight']})")

            elif choice == "8":
                airport_code = input("Enter airport code: ")
                airport_info = airport_table.search(airport_code)
                if airport_info:
                    print(f"Airport Information: {airport_info}")
                else:
                    print("Airport not found.")

            elif choice == "9":
                print(f"Hash Table Size: {airport_table.size}")

            elif choice == "0":
                break

            else:
                print("Invalid choice. Please try again.")
                
        except ValueError as ve:
            print(f"Value error occurred: {ve}")
        except KeyError as ke:
            print(f"Key error occurred: {ke}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()







