# Imports
import random
import time
from colorama import init
from colorama import Fore, Back, Style
from enum import Enum
from flask import Flask, request, jsonify
import copy
import json
from queue import PriorityQueue



def printMaze(maze):
    for i in range(0, height):
        for j in range(0, width):
            if (maze[i][j] == 'u'):
                print(Fore.WHITE + str(maze[i][j]), end=" ")
            elif (maze[i][j] == '*'):
                print(Fore.YELLOW + str(maze[i][j]), end=" ")
            elif (maze[i][j] == 'A'):
                print(Fore.CYAN + str(maze[i][j]), end=" ")
            elif (maze[i][j] == 'B'):
                print(Fore.CYAN + str(maze[i][j]), end=" ")
            else:
                print(Fore.LIGHTRED_EX + str(maze[i][j]), end=" ")

        print(Fore.RESET)
    print()


# Find number of surrounding cells
def surroundingCells(rand_wall):
    s_cells = 0
    if (maze[rand_wall[0] - 1][rand_wall[1]] == '*'):
        s_cells += 1
    if (maze[rand_wall[0] + 1][rand_wall[1]] == '*'):
        s_cells += 1
    if (maze[rand_wall[0]][rand_wall[1] - 1] == '*'):
        s_cells += 1
    if (maze[rand_wall[0]][rand_wall[1] + 1] == '*'):
        s_cells += 1

    return s_cells


def mark_right_cell(rand_wall, maze, walls):
    # Rightmost cell
    if rand_wall[1] != width - 1:
        if maze[rand_wall[0]][rand_wall[1] + 1] != '*':
            maze[rand_wall[0]][rand_wall[1] + 1] = '#'
        if [rand_wall[0], rand_wall[1] + 1] not in walls:
            walls.append([rand_wall[0], rand_wall[1] + 1])


def mark_left_cell(rand_wall, maze, walls):
    if (rand_wall[1] != 0):
        if (maze[rand_wall[0]][rand_wall[1] - 1] != '*'):
            maze[rand_wall[0]][rand_wall[1] - 1] = '#'
        if ([rand_wall[0], rand_wall[1] - 1] not in walls):
            walls.append([rand_wall[0], rand_wall[1] - 1])


def mark_upper_cell(rand_wall, maze, walls):
    if (rand_wall[0] != 0):
        if (maze[rand_wall[0] - 1][rand_wall[1]] != '*'):
            maze[rand_wall[0] - 1][rand_wall[1]] = '#'
        if ([rand_wall[0] - 1, rand_wall[1]] not in walls):
            walls.append([rand_wall[0] - 1, rand_wall[1]])


def mark_lower_cell(rand_wall, maze, walls):
    if (rand_wall[0] != height - 1):
        if (maze[rand_wall[0] + 1][rand_wall[1]] != '*'):
            maze[rand_wall[0] + 1][rand_wall[1]] = '#'
        if ([rand_wall[0] + 1, rand_wall[1]] not in walls):
            walls.append([rand_wall[0] + 1, rand_wall[1]])


## Main code
# Init variables
wall = '#'
cell = '*'
unvisited = 'u'
height = 6
width = 7
maze = []


def generate_one_path_maze():
    maze.clear()

    # Denote all cells as unvisited
    for i in range(0, height):
        line = []
        for j in range(0, width):
            line.append(unvisited)
        maze.append(line)

    # Randomize starting point and set it a cell
    starting_height = 0
    starting_width = 5
    if (starting_height == 0):
        starting_height += 1
    if (starting_height == height - 1):
        starting_height -= 1
    if (starting_width == 0):
        starting_width += 1
    if (starting_width == width - 1):
        starting_width -= 1

    # Mark it as cell and add surrounding walls to the list
    maze[starting_height][starting_width] = cell
    walls = []
    walls.append([starting_height - 1, starting_width])
    walls.append([starting_height, starting_width - 1])
    walls.append([starting_height, starting_width + 1])
    walls.append([starting_height + 1, starting_width])

    # Denote walls in maze
    maze[starting_height - 1][starting_width] = '#'
    maze[starting_height][starting_width - 1] = '#'
    maze[starting_height][starting_width + 1] = '#'
    maze[starting_height + 1][starting_width] = '#'

    while (walls):
        # Pick a random wall
        rand_wall = walls[int(random.random() * len(walls)) - 1]

        # Check if it is a left wall
        if (rand_wall[1] != 0):
            if (maze[rand_wall[0]][rand_wall[1] - 1] == 'u' and maze[rand_wall[0]][rand_wall[1] + 1] == '*'):
                # Find the number of surrounding cells
                s_cells = surroundingCells(rand_wall)

                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = '*'

                    # Mark the new walls
                    mark_upper_cell(rand_wall, maze, walls)
                    mark_lower_cell(rand_wall, maze, walls)
                    mark_left_cell(rand_wall, maze, walls)

                # Delete wall
                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)

                continue

        # Check if it is an upper wall
        if (rand_wall[0] != 0):
            if (maze[rand_wall[0] - 1][rand_wall[1]] == 'u' and maze[rand_wall[0] + 1][rand_wall[1]] == '*'):

                s_cells = surroundingCells(rand_wall)
                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = '*'

                    mark_upper_cell(rand_wall, maze, walls)
                    mark_left_cell(rand_wall, maze, walls)
                    mark_right_cell(rand_wall, maze, walls)

                # Delete wall
                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)

                continue

        # Check the bottom wall
        if (rand_wall[0] != height - 1):
            if (maze[rand_wall[0] + 1][rand_wall[1]] == 'u' and maze[rand_wall[0] - 1][rand_wall[1]] == '*'):

                s_cells = surroundingCells(rand_wall)
                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = '*'

                    # Mark the new walls
                    if (rand_wall[0] != height - 1):
                        if (maze[rand_wall[0] + 1][rand_wall[1]] != '*'):
                            maze[rand_wall[0] + 1][rand_wall[1]] = '#'
                        if ([rand_wall[0] + 1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0] + 1, rand_wall[1]])
                    if (rand_wall[1] != 0):
                        if (maze[rand_wall[0]][rand_wall[1] - 1] != '*'):
                            maze[rand_wall[0]][rand_wall[1] - 1] = '#'
                        if ([rand_wall[0], rand_wall[1] - 1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1] - 1])
                    mark_right_cell(rand_wall, maze, walls)

                # Delete wall
                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)

                continue

        # Check the right wall
        if (rand_wall[1] != width - 1):
            if (maze[rand_wall[0]][rand_wall[1] + 1] == 'u' and maze[rand_wall[0]][rand_wall[1] - 1] == '*'):

                s_cells = surroundingCells(rand_wall)
                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = '*'

                    # Mark the new walls
                    mark_right_cell(rand_wall, maze, walls)
                    if (rand_wall[0] != height - 1):
                        if (maze[rand_wall[0] + 1][rand_wall[1]] != '*'):
                            maze[rand_wall[0] + 1][rand_wall[1]] = '#'
                        if ([rand_wall[0] + 1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0] + 1, rand_wall[1]])
                    if (rand_wall[0] != 0):
                        if (maze[rand_wall[0] - 1][rand_wall[1]] != '*'):
                            maze[rand_wall[0] - 1][rand_wall[1]] = '#'
                        if ([rand_wall[0] - 1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0] - 1, rand_wall[1]])

                # Delete wall
                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)

                continue

        # Delete the wall from the list anyway
        for wall in walls:
            if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                walls.remove(wall)

    # Mark the remaining unvisited cells as walls
    for i in range(0, height):
        for j in range(0, width):
            if maze[i][j] == 'u':
                maze[i][j] = '#'

    # Print final maze
    printMaze(maze)


class Coordinate:
    y = -1
    x = -1

    # def f(self):
    #     return 'hello world'


start = "A"
end = "B"
start_point = Coordinate()
end_point = Coordinate()
current_position = Coordinate()


def create_start_point():
    x, y = get_random_corridor()
    start_point.y = y
    start_point.x = x
    maze[y][x] = start


def create_end_point():
    x, y = get_random_corridor()
    end_point.y = y
    end_point.x = x
    maze[y][x] = end


def set_current_position(c):
    current_position.y = c.y
    current_position.x = c.x


def get_random_corridor():
    random_x = random.randint(0, width - 1)
    random_y = random.randint(0, height - 1)

    while maze[random_y][random_x] is not cell:
        random_x = random.randint(0, width - 1)
        random_y = random.randint(0, height - 1)

    return random_x, random_y


def main():
    # Initialize colorama
    init()

    # Generate the maze
    print('Generated maze:')
    generate_one_path_maze()

    # Create start and end
    print('Set random start and end points:')

    create_start_point()
    create_end_point()
    set_current_position(start_point)
    printMaze(maze)

    # Generate Path
    print('Generating path:')
    maze_solver = MazeSolver(start_point, end_point)
    print("THE ANSWER IS", maze_solver.solve())


def distance_from_objective(s, e):
    hor_distance = abs(s.x - e.x)
    ver_distance = abs(s.y - e.y)
    return hor_distance + ver_distance


class MazeSolver:
    start_coordinate = Coordinate()
    end_coordinate = Coordinate()
    # Should be a priority queue
    maze_move_possibilities = PriorityQueue()

    def __init__(self, s, e):
        self.start_coordinate = s
        self.end_coordinate = e

    def solve(self):
        # Create the first move
        move = MazeMovePossibility(self.start_coordinate, 0, [])
        move.cost_to_end_estimate = distance_from_objective(move.current_coordinate, self.end_coordinate)
        # print("Putting item in queue:", move.cost_from_origin+move.cost_to_end_estimate, move.moves_from_origin)
        self.maze_move_possibilities.put(move)

        while not self.maze_move_possibilities.empty():
            current_move = self.maze_move_possibilities.get()
            if current_move.current_coordinate.y == end_point.y and current_move.current_coordinate.x == end_point.x:
                return current_move.moves_from_origin

            new_moves = current_move.generate_moves()

            for new_move in new_moves:
                new_move.cost_to_end_estimate = distance_from_objective(new_move.current_coordinate, self.end_coordinate)
                # print("Putting item in queue:", new_move.cost_from_origin + new_move.cost_to_end_estimate, new_move.moves_from_origin)
                self.maze_move_possibilities.put(new_move)


class MazeMovePossibility:
    moves_from_origin = []
    current_coordinate = Coordinate()
    cost_from_origin = 0
    cost_to_end_estimate = 0

    def __gt__(self, other):
        self_cost = self.cost_from_origin + self.cost_to_end_estimate
        other_cost = other.cost_from_origin + other.cost_to_end_estimate
        return self_cost > other_cost

    def __lt__(self, other):
        self_cost = self.cost_from_origin + self.cost_to_end_estimate
        other_cost = other.cost_from_origin + other.cost_to_end_estimate
        return self_cost < other_cost

    def __init__(self, c, cost_or, m):
        self.current_coordinate = c
        self.cost_from_origin = cost_or
        self.moves_from_origin = m

    def generate_moves(self):
        new_moves = []
        new_cost = self.cost_from_origin + 1
        if is_coordinate_in_bounds(self.current_coordinate.y - 1, self.current_coordinate.x):
            new_coord = Coordinate()
            new_coord.y = self.current_coordinate.y - 1
            new_coord.x = self.current_coordinate.x

            m = copy.deepcopy(self.moves_from_origin)
            m.append(Move.UP)
            new_moves.append(MazeMovePossibility(new_coord, new_cost, m))
        if is_coordinate_in_bounds(self.current_coordinate.y + 1, self.current_coordinate.x):
            new_coord = Coordinate()
            new_coord.y = self.current_coordinate.y + 1
            new_coord.x = self.current_coordinate.x

            m = copy.deepcopy(self.moves_from_origin)
            m.append(Move.DOWN)
            new_moves.append(MazeMovePossibility(new_coord, new_cost, m))
        if is_coordinate_in_bounds(self.current_coordinate.y, self.current_coordinate.x + 1):
            new_coord = Coordinate()
            new_coord.y = self.current_coordinate.y
            new_coord.x = self.current_coordinate.x + 1

            m = copy.deepcopy(self.moves_from_origin)
            m.append(Move.RIGHT)
            new_moves.append(MazeMovePossibility(new_coord, new_cost, m))
        if is_coordinate_in_bounds(self.current_coordinate.y, self.current_coordinate.x - 1):
            new_coord = Coordinate()
            new_coord.y = self.current_coordinate.y
            new_coord.x = self.current_coordinate.x - 1

            m = copy.deepcopy(self.moves_from_origin)
            m.append(Move.LEFT)
            new_moves.append(MazeMovePossibility(new_coord, new_cost, m))

        return new_moves


def is_coordinate_in_bounds(y, x):
    return 0 <= x <= (width - 1) and 0 <= y <= (height - 1) and maze[y][x] != '#'


class Move(Enum):
    DOWN = 1
    UP = 2
    LEFT = 3
    RIGHT = 4


if __name__ == "__main__":
    main()

app = Flask(__name__)


if __name__ == "__app__":
    # Initialize colorama
    init()


@app.route("/generateMaze", methods=['GET'])
def generateMaze():
    # Generate the maze
    print('Generated maze:')
    generate_one_path_maze()

    # Create start and end
    print('Set random start and end points:')

    create_start_point()
    create_end_point()
    set_current_position(start_point)
    printMaze(maze)

    # Generate Path
    print('The original found path is:')
    maze_solver = MazeSolver(start_point, end_point)
    print("THE ANSWER IS", maze_solver.solve())
    return json.dumps(maze, separators=(', ', ', \n')), 200


@app.route("/findPath", methods=['GET'])
def findPath():
    # Generate Path
    print('Generating path:')
    maze_solver = MazeSolver(start_point, end_point)
    directions = maze_solver.solve()
    print("THE ANSWER IS", directions)
    return json.dumps([direction.name for direction in directions]), 200


is_ready = False


@app.route("/ready", methods=['GET'])
def setReady():
    global is_ready
    is_ready = True
    return json.dumps(is_ready), 200


@app.route("/isReadyToRescue", methods=['GET'])
def isReady():
    global is_ready
    return json.dumps(is_ready), 200