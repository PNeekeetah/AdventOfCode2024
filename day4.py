from collections import deque 

test_input = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

def get_inputs():
    matrix = []
    with open("inputs/input4", "r") as file:
        for line in file.readlines():
            matrix.append(list(line.replace('\n','')))
    
    return matrix

def get_test_input(input):
    matrix = []
    for line in input.split('\n'):
        matrix.append(list(line))
    
    print(matrix)
    
    return matrix

def solve_part_1(input):

    def bound(position):
        assert len(position) == 2
        bound_x = 0 <= position[0] < len(input[0])
        bound_y = 0 <= position[1] < len(input)
        return bound_x and bound_y

    def get_candidate(position, letter, ds = None):
        directions = [
            (0,1),(1,0),(-1,0),(0,-1),
            (1,1),(-1,-1),(1,-1),(-1,1)
        ] if ds is None else ds
        for d in directions:
            new_pos = (position[0] + d[0], position[1] + d[1])
            if bound(new_pos) and input[new_pos[0]][new_pos[1]] == letter:
                yield new_pos, d

    to_explore = []
    for y in range(len(input)):
        for x in range(len(input[0])):
            if input[y][x] == 'X':
                to_explore.append(((y,x),None))
                input[y][x] = '_'

    for letter in ['M', 'A', 'S']:
        next_step = []
        for pos_d in to_explore:
            pos, d = pos_d
            for candidate, new_d in get_candidate(pos, letter, d):
                next_step.append((candidate,[new_d]))
        
        to_explore = next_step

    return len(to_explore)

def solve_part_2(input):

    def bound(position):
        assert len(position) == 2
        bound_x = 0 <= position[0] < len(input[0])
        bound_y = 0 <= position[1] < len(input)
        return bound_x and bound_y

    def x_mas(position):
        diags = [
            ((1,1),(-1,-1)),((1,-1),(-1,1))
        ]
        found = 0
        for d in diags:
            bottom, top = d
            new_bottom = (position[0] + bottom[0], position[1] + bottom[1])
            new_top = (position[0] + top[0], position[1] + top[1])
            if bound(new_bottom) and bound(new_top):
                found += int(
                    input[new_top[0]][new_top[1]] == "M" and input[new_bottom[0]][new_bottom[1]] == "S"
                    or input[new_top[0]][new_top[1]] == "S" and input[new_bottom[0]][new_bottom[1]] == "M"
                )
        
        if found == 2:
            return 1
        return 0

    to_explore = []
    for y in range(len(input)):
        for x in range(len(input[0])):
            if input[y][x] == 'A':
                to_explore.append((y,x))
    
    total_x_mas = 0
    for candidate in to_explore:
        total_x_mas += x_mas(candidate)

    return total_x_mas

print(solve_part_1(get_test_input(test_input)))

print(solve_part_1(get_inputs()))

print(solve_part_2(get_test_input(test_input)))

print(solve_part_2(get_inputs()))