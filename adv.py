from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

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

# Creates the path needed to traverse the maze
def createPath(start):

    # This is an array but it'll be treated as a stack to hold the rooms
    roomStack = [start]

    # Dictionary to keep track of the rooms visited
    visited = {}
    prev = None

    # The path that must be taken to traverse the maze
    path = []

    # While the stack isn't empty
    while len(roomStack) > 0:

        # Set the room equal to the top of the stack
        room = roomStack[-1]
        visited[room.name] = True

        # If there's a room that was previous visited, add the related rooms to the path.
        if prev:
            path.append(prev.relationships(room))

        exits = []
        # Track the exits that a room has
        for exitDir in room.get_exits():
            exits.append(room.get_room_in_direction(exitDir))

        newRooms = []
        # Append each exit to the list of newRooms to be traveled to
        for exit in exits:
            if exit.name not in visited:
                newRooms.append(exit)

        # If there's no new rooms, move down the stack.
        if len(newRooms) == 0:
            roomStack = roomStack[:-1]
        # If there are new rooms, add it to the stack.
        else:
            roomStack.append(newRooms[0])

        prev = room

    # The path taken to traverse the maze.
    return path

traversal_path = createPath(player.current_room)

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
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
