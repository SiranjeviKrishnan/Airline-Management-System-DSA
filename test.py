import numpy as np
import timeit
import random

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

class QuickSort:
    @staticmethod
    def partition(arr, low, high, sort_by):
        i = low - 1
        pivot = arr[high]

        for j in np.arange(low, high):
            if arr[j][sort_by] < pivot[sort_by]:
                i += 1
                arr[i], arr[j] = arr[j].copy(), arr[i].copy()
        
        arr[i + 1], arr[high] = arr[high].copy(), arr[i + 1].copy()
        return i + 1

    @staticmethod
    def quicksort(arr, low, high, sort_by):
        if low < high:
            pi = QuickSort.partition(arr, low, high, sort_by)
            QuickSort.quicksort(arr, low, pi - 1, sort_by)
            QuickSort.quicksort(arr, pi + 1, high, sort_by)

    @staticmethod
    def sort(arr, sort_by):
        QuickSort.quicksort(arr, 0, arr.size - 1, sort_by)
        return arr
    
class MergeSort:
    @staticmethod
    def merge(arr, l, m, r, sort_by):
        n1 = m - l + 1
        n2 = r - m

        L = np.empty((n1,), dtype=arr.dtype)
        R = np.empty((n2,), dtype=arr.dtype)

        for i in np.arange(n1):
            L[i] = arr[l + i]

        for j in np.arange(n2):
            R[j] = arr[m + 1 + j]

        i = 0
        j = 0
        k = l

        while i < n1 and j < n2:
            if L[i][sort_by] <= R[j][sort_by]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1

        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1

    @staticmethod
    def mergesort(arr, l, r, sort_by):
        if l < r:
            m = (l + r) // 2
            MergeSort.mergesort(arr, l, m, sort_by)
            MergeSort.mergesort(arr, m + 1, r, sort_by)
            MergeSort.merge(arr, l, m, r, sort_by)

    @staticmethod
    def sort(arr, sort_by):
        MergeSort.mergesort(arr, 0, arr.size - 1, sort_by)
        return arr
    
def generate_test_case(num_vertices, num_routes):
    graph = Graph(num_vertices)
    for i in range(num_vertices):
        graph.add_vertex(str(i))
    
    for _ in range(num_routes):
        start = str(random.randint(0, num_vertices - 1))
        end = str(random.randint(0, num_vertices - 1))
        weight = random.randint(1, 10)
        graph.add_edge(start, end, weight)
    
    return graph

def compare_sorts_time_complexity(num_vertices, num_routes):
    graph = generate_test_case(num_vertices, num_routes)
    routes = graph.bfs('0', str(num_vertices - 1), 0)
    
    routes_heap = routes.copy()
    routes_quick = routes.copy()
    routes_merge = routes.copy()
    
    time_heap = timeit.timeit(lambda: HeapSort.sort(routes_heap, 'distance'), number=1)
    time_quick = timeit.timeit(lambda: QuickSort.sort(routes_quick, 'distance'), number=1)
    time_merge = timeit.timeit(lambda: MergeSort.sort(routes_merge, 'distance'), number=1)
    
    return time_heap, time_quick, time_merge

num_vertices = 10
num_routes = 20
time_heap, time_quick, time_merge = compare_sorts_time_complexity(num_vertices, num_routes)
print(f"Time taken by HeapSort: {time_heap} seconds")
print(f"Time taken by QuickSort: {time_quick} seconds")
print(f"Time taken by MergeSort: {time_merge} seconds")

def main():
    num_vertices = 10
    max_routes = 1000
    step = 10

    num_routes_list = list(range(10, max_routes + 1, step))

    print("Number of Routes\tHeapSort\tQuickSort\tMergeSort")
    for num_routes in num_routes_list:
        time_heap, time_quick, time_merge = compare_sorts_time_complexity(num_vertices, num_routes)
        print(f"{num_routes}\t\t\t{time_heap:.6f}\t\t{time_quick:.6f}\t\t{time_merge:.6f}")

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()