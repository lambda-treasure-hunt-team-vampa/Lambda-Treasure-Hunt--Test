from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

import json

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

movement_dict = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}

class Traversal_Graph:
    def __init__(self):
        self.vertices = {}
    def add_vertex(self, room):
        self.vertices[room.id] = {exit: '?' for exit in room.get_exits()}
    def add_edge(self, starting_room, destination_room, move):
        if (starting_room.id in self.vertices) and (
            destination_room.id in self.vertices):
            self.vertices[starting_room.id][move] = destination_room.id
            self.vertices[destination_room.id][
                movement_dict[move]] = starting_room.id
        else:
            raise IndexError("That room does not exist!")
    def get_neighbors(self, room_id):
        return set(self.vertices[room_id].values())
    def bfs_to_unexplored(self, starting_room):
        # Create a queue/stack as appropriate
        queue = Queue()
        # Put the starting point in that
        # Enstack a list to use as our path
        queue.enqueue([starting_room.id])
        # Make a set to keep track of where we've been
        visited = set()
        # While there is stuff in the queue/stack
        while queue.size() > 0:
        #   Pop the first item
            path = queue.dequeue()
            vertex = path[-1]
        #   If not visited
            if vertex not in visited:
                if vertex == '?':
                    # Do the thing!
                    directions = []
                    for i in range(1, len(path[:-1])):
                        for option in traversal_graph.vertices[path[i - 1]]:
                            if traversal_graph.vertices[path[i - 1]][
                                option] == path[i]:
                                directions.append(option)
                    return directions
                visited.add(vertex)
        #       For each edge in the item
                for next_vert in self.get_neighbors(vertex):
                # Copy path to avoid pass by reference bug
                    new_path = list(path) # Make a copy of path rather than reference
                    new_path.append(next_vert)
                    queue.enqueue(new_path)

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

# best_score = 956
# while best_score > 0:
# best_score = 1000
# while best_score > 985:
#     player = Player(world.starting_room)

#     # Fill this out with directions to walk
#     # traversal_path = ['n', 'n']
#     traversal_path = []

#     traversal_graph = Traversal_Graph()
#     traversal_graph.add_vertex(player.current_room)

#     while len(traversal_graph.vertices) < 500:
#         pre_move_room = player.current_room
#         exits = pre_move_room.get_exits()
#         unexplored = [option for option in exits if (
#             traversal_graph.vertices[pre_move_room.id][option] == '?')]
#         if len(unexplored) > 0:
#             move = random.choice(unexplored)
#             player.travel(move)
#             traversal_path.append(move)
#             post_move_room = player.current_room
#             if post_move_room.id not in traversal_graph.vertices:
#                 traversal_graph.add_vertex(post_move_room)
#             traversal_graph.add_edge(pre_move_room, post_move_room, move)
#         else:
#             to_unexplored = traversal_graph.bfs_to_unexplored(player.current_room)
#             for move in to_unexplored:
#                 player.travel(move)
#                 traversal_path.append(move)

#     if len(traversal_path) < best_score:
#         best_score = len(traversal_path)
        # with open(f'traversal_in_{len(traversal_path)}_moves.txt', 'w') as file:
        #     json.dump(traversal_path, file)

with open(f'traversal_in_956_moves.txt') as file:
    traversal_path = json.load(file)
player = Player(world.starting_room)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
