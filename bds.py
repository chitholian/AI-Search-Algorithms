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

from collections import deque

class Graph:
    def __init__(self, directed=True):
        self.edges = {}
        self.directed = directed

    def add_edge(self, node1, node2, __reversed=False):
        try: neighbors = self.edges[node1]
        except KeyError: neighbors = set()
        neighbors.add(node2)
        self.edges[node1] = neighbors
        if not self.directed and not __reversed: self.add_edge(node2, node1, True)

    def neighbors(self, node):
        try: return self.edges[node]
        except KeyError: return []

    def bi_directional_search(self, start, goal):
        found, fringe1, visited1, came_from1 = False, deque([start]), set([start]), {start: None}
        meet, fringe2, visited2, came_from2 = None, deque([goal]), set([goal]), {goal: None}
        while not found and (len(fringe1) or len(fringe2)):
            print('FringeStart: {:30s} | FringeGoal: {}'.format(str(fringe1), str(fringe2)))
            if len(fringe1):
                current1 = fringe1.pop()
                if current1 in visited2: meet = current1; found = True; break
                for node in self.neighbors(current1):
                    if node not in visited1: visited1.add(node); fringe1.appendleft(node); came_from1[node] = current1
            if len(fringe2):
                current2 = fringe2.pop()
                if current2 in visited1: meet = current2; found = True; break
                for node in self.neighbors(current2):
                    if node not in visited2: visited2.add(node); fringe2.appendleft(node); came_from2[node] = current2
        if found: print(); return came_from1, came_from2, meet
        else: print('No path between {} and {}'.format(start, goal)); return None, None, None

    @staticmethod
    def print_path(came_from, goal):
        parent = came_from[goal]
        if parent:
            Graph.print_path(came_from, parent)
        else: print(goal, end='');return
        print(' =>', goal, end='')

    def __str__(self):
        return str(self.edges)


graph = Graph(directed=False)
graph.add_edge('A', 'B'); graph.add_edge('A', 'S'); graph.add_edge('S', 'G')
graph.add_edge('S', 'C'); graph.add_edge('C', 'F'); graph.add_edge('G', 'F')
graph.add_edge('C', 'D'); graph.add_edge('C', 'E'); graph.add_edge('E', 'H')
graph.add_edge('G', 'H')
start, goal = 'A', 'H'
traced_path1, traced_path2, meet = graph.bi_directional_search(start, goal)
if meet:
    print('Meeting Node:', meet)
    print('Path From Start:', end=' '); Graph.print_path(traced_path1, meet); print()
    print('Path From Goal:', end=' '); Graph.print_path(traced_path2, meet); print()
