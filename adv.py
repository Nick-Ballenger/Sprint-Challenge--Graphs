from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Queue:
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

# Fill this out with dirss to walk
def traverse(player, moves_cue):
    q = Queue()
    visited = set()
    q.enqueue([player.current_room.id])
    while q.size() > 0:
        path = q.dequeue()
        last_room = path[-1]
        if last_room not in visited:
            visited.add(last_room)
            for exit in graph[last_room]:
                if graph[last_room][exit] == "?":
                    return path
                else:
                    lost = list(path)
                    lost.append(graph[last_room][exit])
                    q.enqueue(lost)
    return []


def q_moves(player, moves_q):
    possible_moves = graph[player.current_room.id]
    fresh_moves = []


    for dirs in possible_moves:
        if possible_moves[dirs] == "?":
            fresh_moves.append(dirs)
    if len(fresh_moves) == 0:
        new_rooms = traverse(player, moves_q)
        room_num = player.current_room.id
        for next in new_rooms:
            for dirs in graph[room_num]:
                if graph[room_num][dirs] == next:
                    moves_q.enqueue(dirs)
                    room_num = next
                    break


    else:
        moves_q.enqueue(fresh_moves[random.randint(0, len(fresh_moves) - 1)])


num_of_tries = 200
optimum_length = 977
optimum_path = []


for i in range(num_of_tries):
    player = Player(world.starting_room)
    graph = {}




    new_room = {}
    for dirs in player.current_room.get_exits():
        new_room[dirs] = "?"
    graph[world.starting_room.id] = new_room


    

    moves_q = Queue()
    total_moves = []
    q_moves(player, moves_q)

    backward_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}

    while moves_q.size() > 0:
        start = player.current_room.id
        go = moves_q.dequeue()
        player.travel(go)
        total_moves.append(go)
        end = player.current_room.id
        graph[start][go] = end
        if end not in graph:
            graph[end] = {}
            for exit in player.current_room.get_exits():
                graph[end][exit] = "?"
        graph[end][backward_dirs[go]] = start
        if moves_q.size() == 0:
            q_moves(player, moves_q)
    if len(total_moves) < optimum_length:
        optimum_path= total_moves
        optimum_length = len(total_moves)


traversal_path = optimum_path

# TRAVERSAL TEST
spent_rooms = set()
player.current_room = world.starting_room
spent_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    spent_rooms.add(player.current_room)

if len(spent_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(spent_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(spent_rooms)} unvisited rooms")

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
