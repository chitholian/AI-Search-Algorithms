#    Copyright 2019 Atikur Rahman Chitholian
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from queue import heappop, heappush
from math import inf

class Graph:
    def __init__(self, directed=True):
        self.edges = {}
        self.huristics = {}
        self.directed = directed

    def add_edge(self, node1, node2, cost = 1, __reversed=False):
        try: neighbors = self.edges[node1]
        except KeyError: neighbors = {}
        neighbors[node2] = cost
        self.edges[node1] = neighbors
        if not self.directed and not __reversed: self.add_edge(node2, node1, cost, True)

    def set_huristics(self, huristics={}):
        self.huristics = huristics

    def neighbors(self, node):
        try: return self.edges[node]
        except KeyError: return []

    def cost(self, node1, node2):
        try: return self.edges[node1][node2]
        except: return inf

    def iterative_deepening_astar_search(self, start, goal):
        prev_visited, depth = 0, 0
        while True:
            trace, cost, visited = self.dept_limited_astar_search(start, goal, depth)
            if trace or visited == prev_visited: return trace, cost
            prev_visited = visited
            depth += 1


    def dept_limited_astar_search(self, start, goal, limit=-1):
        print('Depth Limit =', limit)
        found, fringe, visited = False, [(self.huristics[start], start, 0)], set([start])
        came_from, cost_so_far = {start: None}, {start: 0}
        print('{:11s} | {}'.format('Expand Node', 'Fringe'))
        print('--------------------')
        print('{:11s} | {}'.format('-', str(fringe[0][:-1])))
        while not found and len(fringe):
            _, current, depth = heappop(fringe)
            print('{:11s}'.format(current), end=' | ')
            if current == goal: found = True; break
            if limit == -1 or depth < limit:
                for node in self.neighbors(current):
                    new_cost = cost_so_far[current] + self.cost(current, node)
                    if node not in visited or cost_so_far[node] > new_cost:
                        visited.add(node); came_from[node] = current; cost_so_far[node] = new_cost
                        heappush(fringe, (new_cost + self.huristics[node], node, depth + 1))
            print(', '.join([str(n[:-1]) for n in fringe]))
        if found: print(); return came_from, cost_so_far[goal], len(visited)
        else: print('No path from {} to {}'.format(start, goal)); return None, inf, len(visited)

    @staticmethod
    def print_path(came_from, goal):
        parent = came_from[goal]
        if parent:
            Graph.print_path(came_from, parent)
        else: print(goal, end='');return
        print(' =>', goal, end='')


    def __str__(self):
        return str(self.edges)

graph = Graph(directed=True)
graph.add_edge('A', 'B', 4)
graph.add_edge('A', 'C', 1)
graph.add_edge('B', 'D', 3)
graph.add_edge('B', 'E', 8)
graph.add_edge('C', 'C', 0)
graph.add_edge('C', 'D', 7)
graph.add_edge('C', 'F', 6)
graph.add_edge('D', 'C', 2)
graph.add_edge('D', 'E', 4)
graph.add_edge('E', 'G', 2)
graph.add_edge('F', 'G', 8)
graph.set_huristics({'A': 8, 'B': 8, 'C': 6, 'D': 5, 'E': 1, 'F': 4, 'G': 0})
start, goal, limit = 'A', 'G', 3
traced_path, cost = graph.iterative_deepening_astar_search(start, goal)
if (traced_path): print('Path:', end=' '); Graph.print_path(traced_path, goal); print('\nCost:', cost)
