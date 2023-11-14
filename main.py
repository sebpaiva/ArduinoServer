from flask import Flask, jsonify
from random import randrange, random
from colorama import init, Fore

app = Flask(__name__)


class Maze:
    map = []
    mapMaxX = 5
    mapMaxY = 5
    startPointX = 0
    startPointY = 0
    destinationY = 0
    destinationX = 0

    def hasSameStartAndEnd(self):
        return self.destinationY == self.startPointY and self.destinationX == self.startPointX

    def randomize_destination(self):
        self.destinationX = randrange(0, self.mapMaxX)
        self.destinationY = randrange(0, self.mapMaxY)


global maze


def init_maze():
    width = maze.mapMaxX
    height = maze.mapMaxY
    maze.map = []
    for i in range(0, height):
        line = []
        for j in range(0, width):
            line.append('u')
        maze.map.append(line)


def generate_map():
    maze.randomize_destination()

    # Do not randomize solution in the same position as start
    while maze.randomize_destination():
        maze.randomize_destination()

    init_maze()
    print_maze()

    cell = 'c'
    wall = 'w'
    unvisited = 'u'
    height = maze.mapMaxY
    width = maze.mapMaxX

    # Pick a random spot to set as a free spot
    starting_height = int(random() * height)
    starting_width = int(random() * width)

    # Do not start on a block on the edge of the maze
    if starting_height == 0:
        starting_height += 1
    if starting_height == height - 1:
        starting_height -= 1
    if starting_width == 0:
        starting_width += 1
    if starting_width == width - 1:
        starting_width -= 1

    maze.map[starting_height][starting_width] = cell
    walls = []
    walls.append([starting_height - 1, starting_width])
    walls.append([starting_height, starting_width - 1])
    walls.append([starting_height, starting_width + 1])
    walls.append([starting_height + 1, starting_width])

    maze.map[starting_height - 1][starting_width] = wall
    maze.map[starting_height][starting_width - 1] = wall
    maze.map[starting_height][starting_width + 1] = wall
    maze.map[starting_height + 1][starting_width] = wall
    print_maze()

    while walls:
        # Pick a random wall
        rand_wall = walls[int(random() * len(walls)) - 1]

        # Check if it is a left wall
        if (rand_wall[1] != 0):
            if (maze.map[rand_wall[0]][rand_wall[1] - 1] == 'u' and maze.map[rand_wall[0]][rand_wall[1] + 1] == 'c'):
                # Find the number of surrounding cells
                s_cells = surroundingCells(rand_wall)

                if (s_cells < 2):
                    # Denote the new path
                    maze.map[rand_wall[0]][rand_wall[1]] = 'c'

                    # Mark the new walls
                    # Upper cell
                    if (rand_wall[0] != 0):
                        if (maze.map[rand_wall[0] - 1][rand_wall[1]] != 'c'):
                            maze.map[rand_wall[0] - 1][rand_wall[1]] = 'w'
                        if ([rand_wall[0] - 1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0] - 1, rand_wall[1]])

                    # Bottom cell
                    if (rand_wall[0] != height - 1):
                        if (maze.map[rand_wall[0] + 1][rand_wall[1]] != 'c'):
                            maze.map[rand_wall[0] + 1][rand_wall[1]] = 'w'
                        if ([rand_wall[0] + 1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0] + 1, rand_wall[1]])

                    # Leftmost cell
                    if (rand_wall[1] != 0):
                        if (maze.map[rand_wall[0]][rand_wall[1] - 1] != 'c'):
                            maze.map[rand_wall[0]][rand_wall[1] - 1] = 'w'
                        if ([rand_wall[0], rand_wall[1] - 1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1] - 1])

                # Delete wall
                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)

                continue

        # Check if it is an upper wall
        if rand_wall[0] != 0:
            if maze.map[rand_wall[0] - 1][rand_wall[1]] == 'u' and maze.map[rand_wall[0] + 1][rand_wall[1]] == 'c':

                s_cells = surroundingCells(rand_wall)
                if s_cells < 2:
                    # Denote the new path
                    maze.map[rand_wall[0]][rand_wall[1]] = 'c'

                    # Mark the new walls
                    # Upper cell
                    if (rand_wall[0] != 0):
                        if (maze.map[rand_wall[0] - 1][rand_wall[1]] != 'c'):
                            maze.map[rand_wall[0] - 1][rand_wall[1]] = 'w'
                        if ([rand_wall[0] - 1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0] - 1, rand_wall[1]])

                    # Leftmost cell
                    if (rand_wall[1] != 0):
                        if (maze.map[rand_wall[0]][rand_wall[1] - 1] != 'c'):
                            maze.map[rand_wall[0]][rand_wall[1] - 1] = 'w'
                        if ([rand_wall[0], rand_wall[1] - 1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1] - 1])

                    # Rightmost cell
                    if (rand_wall[1] != width - 1):
                        if (maze.map[rand_wall[0]][rand_wall[1] + 1] != 'c'):
                            maze.map[rand_wall[0]][rand_wall[1] + 1] = 'w'
                        if ([rand_wall[0], rand_wall[1] + 1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1] + 1])

                # Delete wall
                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)

                continue

        # Check the bottom wall
        if (rand_wall[0] != height - 1):
            if (maze.map[rand_wall[0] + 1][rand_wall[1]] == 'u' and maze.map[rand_wall[0] - 1][rand_wall[1]] == 'c'):

                s_cells = surroundingCells(rand_wall)
                if (s_cells < 2):
                    # Denote the new path
                    maze.map[rand_wall[0]][rand_wall[1]] = 'c'

                    # Mark the new walls
                    if (rand_wall[0] != height - 1):
                        if (maze.map[rand_wall[0] + 1][rand_wall[1]] != 'c'):
                            maze.map[rand_wall[0] + 1][rand_wall[1]] = 'w'
                        if ([rand_wall[0] + 1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0] + 1, rand_wall[1]])
                    if (rand_wall[1] != 0):
                        if (maze.map[rand_wall[0]][rand_wall[1] - 1] != 'c'):
                            maze.map[rand_wall[0]][rand_wall[1] - 1] = 'w'
                        if ([rand_wall[0], rand_wall[1] - 1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1] - 1])
                    if (rand_wall[1] != width - 1):
                        if (maze.map[rand_wall[0]][rand_wall[1] + 1] != 'c'):
                            maze.map[rand_wall[0]][rand_wall[1] + 1] = 'w'
                        if ([rand_wall[0], rand_wall[1] + 1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1] + 1])

                # Delete wall
                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)

                continue

        # Check the right wall
        if (rand_wall[1] != width - 1):
            if (maze.map[rand_wall[0]][rand_wall[1] + 1] == 'u' and maze.map[rand_wall[0]][rand_wall[1] - 1] == 'c'):

                s_cells = surroundingCells(rand_wall)
                if (s_cells < 2):
                    # Denote the new path
                    maze.map[rand_wall[0]][rand_wall[1]] = 'c'

                    # Mark the new walls
                    if (rand_wall[1] != width - 1):
                        if (maze.map[rand_wall[0]][rand_wall[1] + 1] != 'c'):
                            maze.map[rand_wall[0]][rand_wall[1] + 1] = 'w'
                        if ([rand_wall[0], rand_wall[1] + 1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1] + 1])
                    if (rand_wall[0] != height - 1):
                        if (maze.map[rand_wall[0] + 1][rand_wall[1]] != 'c'):
                            maze.map[rand_wall[0] + 1][rand_wall[1]] = 'w'
                        if ([rand_wall[0] + 1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0] + 1, rand_wall[1]])
                    if (rand_wall[0] != 0):
                        if (maze.map[rand_wall[0] - 1][rand_wall[1]] != 'c'):
                            maze.map[rand_wall[0] - 1][rand_wall[1]] = 'w'
                        if ([rand_wall[0] - 1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0] - 1, rand_wall[1]])

                # Delete wall
                for wall in walls:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        walls.remove(wall)

                continue

        # Delete the wall from the list anyway
        for wall in walls:
            if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                walls.remove(wall)

    # Mark the remaining unvisited cells as walls
    for i in range(0, height):
        for j in range(0, width):
            if maze.map[i][j] == 'u':
                maze.map[i][j] = 'w'

    # Set entrance and exit
    for i in range(0, width):
        if maze.map[1][i] == 'c':
            maze.map[0][i] = 'c'
            break

    for i in range(width - 1, 0, -1):
        if maze.map[height - 2][i] == 'c':
            maze.map[height - 1][i] = 'c'
            break

    # Print final maze
    print_maze()

    def delete_wall(rand_wall):
        for wall in walls:
            if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                walls.remove(wall)

    def make_walls(width, height):
        for i in range(0, height):
            for j in range(0, width):
                if maze.map[i][j] == 'u':
                    maze.map[i][j] = 'w'

    def surrounding_cells(rand_wall):
        s_cells = 0
        if maze.map[rand_wall[0] - 1][rand_wall[1]] == 'c':
            s_cells += 1
        if maze.map[rand_wall[0] + 1][rand_wall[1]] == 'c':
            s_cells += 1
        if maze.map[rand_wall[0]][rand_wall[1] - 1] == 'c':
            s_cells += 1
        if maze.map[rand_wall[0]][rand_wall[1] + 1] == 'c':
            s_cells += 1
        return s_cells


def surroundingCells(rand_wall):
    s_cells = 0
    if maze.map[rand_wall[0] - 1][rand_wall[1]] == 'c':
        s_cells += 1
    if maze.map[rand_wall[0] + 1][rand_wall[1]] == 'c':
        s_cells += 1
    if maze.map[rand_wall[0]][rand_wall[1] - 1] == 'c':
        s_cells += 1
    if maze.map[rand_wall[0]][rand_wall[1] + 1] == 'c':
        s_cells += 1

    return s_cells


@app.route('/api/get_data', methods=['GET'])
def get_data():
    data = {'message': 'Hello, this is your GET endpoint!'}
    return jsonify(data)


def print_maze():
    for i in range(0, len(maze.map)):
        for j in range(0, len(maze.map[0])):
            if maze.map[i][j] == 'u':
                print(Fore.WHITE, f'{maze.map[i][j]}', end="")
            elif maze.map[i][j] == 'c':
                print(Fore.GREEN, f'{maze.map[i][j]}', end="")
            else:
                print(Fore.RED, f'{maze.map[i][j]}', end="")
        print('\n')


if __name__ == '__main__':
    init()
    maze = Maze()
    generate_map()
    # app.run(debug=True)
