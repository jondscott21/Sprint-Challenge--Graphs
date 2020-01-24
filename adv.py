from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from util import Queue, Stack

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

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

def find_shortest_path(starting_room, visited):
    queue = Queue()
    queue.enqueue([(starting_room.id, "")])
    visited_set = set()
    while queue.size() > 0:
        path = queue.dequeue()
        vertex = path[-1][0]
        for k, v in visited[vertex].items():
            if v == '?':
                return path
        if vertex not in visited_set:
            visited_set.add(vertex)
            for direction, neighbor in visited[vertex].items():
                if neighbor not in visited_set:
                    new_path = list(path)
                    new_path.append((neighbor, direction))
                    queue.enqueue(new_path)

def traverse_map():
    stack = Stack()
    stack.push(player.current_room)
    visited = {}
    random_direction = None
    prev_room = None
    while len(visited) <= len(room_graph):
        cur = stack.pop()
        # Add current room to our adjacency list if it's not there
        if cur.id not in visited:
            visited[cur.id] = {}
            for d in cur.get_exits():
                visited[cur.id][d] = '?'
        # Starts traversing a random direction
        if random_direction is None:
            available = ''
            for d in visited[cur.id]:
                if visited[cur.id][d] == '?':
                    available += d
                random_direction = random.choice(available)
        # Add a 'step' to our traversal list
        # Updates our adjacency list edges based on the previous move (excludes adding on start up)
        if prev_room is not None:
            prev_dir = ''
            if random_direction == 'n': prev_dir = 's'
            elif random_direction == 's': prev_dir = 'n'
            elif random_direction == 'e': prev_dir = 'w'
            elif random_direction == 'w': prev_dir = 'e'
            # Checks to make sure the directions being added are valid
            if random_direction in visited[prev_room.id] and prev_dir in visited[cur.id]:
                visited[prev_room.id][random_direction] = cur.id
                visited[cur.id][prev_dir] = prev_room.id
        # If we hit a end point for our current direction
        if random_direction not in visited[cur.id]:
            unexplored = ''
            for k, v in visited[cur.id].items():
                if v == '?':
                    unexplored += k
            if len(unexplored) == 0:
                path = find_shortest_path(cur, visited)
                if path is None:
                    return
                new_room = path[-1][0]
                for move in path[1:]:
                    traversal_path.append(move[1])
                    player.travel(move[1])
                unexplored = ''
                for k, v in visited[new_room].items():
                    if v == '?':
                        unexplored += k
            random_direction = random.choice(unexplored)
        # Updates our previous room
        traversal_path.append(random_direction)
        prev_room = player.current_room
        # Moves our current room in 'x' direction
        player.travel(random_direction)
        # Adds it to our Stack for new interation cycle
        stack.push(player.current_room)
traverse_map()

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

