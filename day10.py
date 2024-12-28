test_input = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

def get_test_inputs(input):
    matrix = []

    lines = input.split('\n')
    for line in lines:
        if line == '':
            continue
        matrix.append([int(num) for num in line])
    
    return matrix

def get_input():
    with open('inputs/input10', 'r') as file:
        return get_test_inputs(file.read())
    
def solve_day_10_part_1(matrix):

    def bound(pos):
        assert len(pos) == 2
        bound_x = 0 <= pos[0] < len(matrix)
        bound_y = 0 <= pos[1] < len(matrix[0])
        return bound_x and bound_y
    
    def get_next(pos, next_number):
        assert len(pos) == 2
        for d in [(0,1),(1,0),(-1,0),(0,-1)]:
            new_pos = (pos[0] + d[0], pos[1] + d[1])
            if bound(new_pos) and matrix[new_pos[0]][new_pos[1]] == next_number:
                yield new_pos
    
    locations = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 0:
                locations.append([((i,j),1), ((i,j),1)])
    
    for _ in range(1,10):
        next_locations = []
        for trail in locations:
            loc, number = trail[-1]
            for candidate in get_next(loc, number):
                new_trail = list(trail)
                new_trail.pop()
                new_trail.append((candidate, number + 1))
                next_locations.append(new_trail)
        locations = next_locations
    trails = []
    for location in locations:
        trails.append(tuple([l[0] for l in location]))
    
    return len(set(trails))

def solve_day_10_part_2(matrix):

    def bound(pos):
        assert len(pos) == 2
        bound_x = 0 <= pos[0] < len(matrix)
        bound_y = 0 <= pos[1] < len(matrix[0])
        return bound_x and bound_y
    
    def get_next(pos, next_number):
        assert len(pos) == 2
        for d in [(0,1),(1,0),(-1,0),(0,-1)]:
            new_pos = (pos[0] + d[0], pos[1] + d[1])
            if bound(new_pos) and matrix[new_pos[0]][new_pos[1]] == next_number:
                yield new_pos
    
    locations = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 0:
                locations.append([((i,j),1)])
    
    for _ in range(1,10):
        next_locations = []
        for trail in locations:
            loc, number = trail[-1]
            for candidate in get_next(loc, number):
                new_trail = list(trail)
                new_trail.append((candidate, number + 1))
                next_locations.append(new_trail)
        locations = next_locations
    trails = []
    for location in locations:
        trails.append(tuple([l[0] for l in location]))
    
    return len(set(trails))

print(solve_day_10_part_1(get_test_inputs(test_input)))
print(solve_day_10_part_1(get_input()))

# This took me 55 m 44s 

print(solve_day_10_part_2(get_test_inputs(test_input)))
print(solve_day_10_part_2(get_input()))

# Overall, this took em 57m 17s.
# The reason why it took me only 2 minutes to change it was because I have been solving the second part all along :)) 
