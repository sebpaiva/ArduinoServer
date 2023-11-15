# Maze generator -- Randomized Prim Algorithm

## Imports
import random
import time
from colorama import init
from colorama import Fore, Back, Style


## Functions
def printMaze(maze):
    for i in range(0, height):
        for j in range(0, width):
            if (maze[i][j] == 'u'):
                print(Fore.WHITE + str(maze[i][j]), end=" ")
            elif (maze[i][j] == '*'):
                print(Fore.GREEN + str(maze[i][j]), end=" ")
            else:
                print(Fore.RED + str(maze[i][j]), end=" ")

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

# Initialize colorama
init()

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


