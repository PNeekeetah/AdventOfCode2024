test_input = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
r...........
........A...
.........A..
............
............"""
from collections import deque

def get_test_inputs(input):
    matrix = []

    lines = input.split('\n')
    for line in lines:
        if line == '':
            continue
        matrix.append(list(line))
    
    return matrix

def get_input():
    with open('inputs/input8', 'r') as file:
        return get_test_inputs(file.read())
    

def solve_day_8_part_1(matrix):

    # Preprocessing. Find location of all the various nodes.

    nodes = {} # lowercase/ uppercase / digit : list of positions
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == '.':
                continue
            symbol = matrix[i][j]
            nodes[symbol] = nodes.get(symbol, [])
            nodes[symbol].append((i,j))
    
    # I think sorting these might help. Worth trying without as well
    # Sorting doesn't seem to affect the result
    for k in nodes.keys():
        nodes[k].sort()

    antinodes = set()

    def bound(pos):
        assert len(pos) == 2
        bound_x = 0 <= pos[0] < len(matrix)
        bound_y = 0 <= pos[1] < len(matrix[0])
        return bound_x and bound_y

    def x_y_distance(cur, other):
        return (other[0] - cur[0], other[1] - cur[1])
    
    for same_frequency_nodes in nodes.values():
        same_frequency_nodes = deque(same_frequency_nodes)
        while len(same_frequency_nodes) > 1:
            current = same_frequency_nodes.popleft()
            for other in same_frequency_nodes:
                dx, dy = x_y_distance(current, other)
                antinode_current = (current[0] - dx, current[1] - dy)
                antinode_other = (other[0] + dx, other[1] + dy)
                if bound(antinode_current):
                    antinodes.add(antinode_current)
                if bound(antinode_other):
                    antinodes.add(antinode_other)
    
    return len(antinodes)



def solve_day_8_part_2(matrix):

    # Preprocessing. Find location of all the various nodes.

    nodes = {} # lowercase/ uppercase / digit : list of positions
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == '.':
                continue
            symbol = matrix[i][j]
            nodes[symbol] = nodes.get(symbol, [])
            nodes[symbol].append((i,j))
    
    # I think sorting these might help. Worth trying without as well
    # Sorting doesn't seem to affect the result
    for k in nodes.keys():
        nodes[k].sort()

    antinodes = set()

    def bound(pos):
        assert len(pos) == 2
        bound_x = 0 <= pos[0] < len(matrix)
        bound_y = 0 <= pos[1] < len(matrix[0])
        return bound_x and bound_y

    def x_y_distance(cur, other):
        return (other[0] - cur[0], other[1] - cur[1])
    
    for same_frequency_nodes in nodes.values():
        same_frequency_nodes = deque(same_frequency_nodes)
        while len(same_frequency_nodes) > 1:
            current = same_frequency_nodes.popleft()
            for other in same_frequency_nodes:
                dx, dy = x_y_distance(current, other)
                back = (other[0] - dx, other[1] - dy)
                while bound(back):
                    antinodes.add(back)
                    back = (back[0] - dx, back[1] - dy)
                forth = (other[0] + dx, other[1] + dy)
                while bound(forth):
                    antinodes.add(forth)
                    forth = (forth[0] + dx, forth[1] + dy)
                antinodes.add(other)
                
    
    return len(antinodes)


     

print(solve_day_8_part_1(get_test_inputs(test_input)))
print(solve_day_8_part_1(get_input()))
# Took about 31 minutes to get here

print(solve_day_8_part_2(get_test_inputs(test_input)))
print(solve_day_8_part_2(get_input()))
# Overall 37 minutes to sort everything out