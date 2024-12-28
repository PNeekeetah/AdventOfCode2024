test_input = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

def get_test_inputs(input):
    matrix = []

    lines = input.split('\n')
    for line in lines:
        line = line.replace('\n','')
        matrix.append(list(line))
    
    return matrix

def get_inputs():
    matrix = []

    with open("inputs/input6", 'r') as file:
    
        for line in file.readlines():
            line = line.replace('\n','')
            matrix.append(list(line))
        
    return matrix

def solve_day_6_part_1(matrix):
    start_pos = None
    for i,line in enumerate(matrix):
        if '^' in line:
            start_pos = (i, line.index('^'))
            matrix[start_pos[0]][start_pos[1]] = '.'
            break
    
    orientations = [(-1,0),(0,1),(1,0),(0,-1)]
    orientation = 0

    def bound(pos):
        assert len(pos) == 2
        bound_x = 0 <= pos[0] < len(matrix[0])
        bound_y = 0 <= pos[1] <= len(matrix)
        return bound_x and bound_y
    
    def get_next(pos, orientation):
        return (pos[0] + orientation[0], pos[1] + orientation[1])

    def transition_next(pos, orientation):
        start_pos = pos
        while start_pos == pos:
            potential = get_next(pos, orientations[orientation%4])
            if bound(potential) and matrix[potential[0]][potential[1]] == '.':
                return (potential, orientation)
            elif bound(potential) and  matrix[potential[0]][potential[1]] == '#':
                orientation += 1
            elif not bound(potential):
                return ((None, None), orientation)
            start_pos = pos
            

    seen = set()


    current_position = start_pos
    while True:
        seen.add(current_position)
        current_position, orientation = transition_next(current_position, orientation)
        if current_position == (None, None):
            break
    
    return len(seen)


def solve_day_6_part_2(matrix):
    start_pos = None
    for i,line in enumerate(matrix):
        if '^' in line:
            start_pos = (i, line.index('^'))
            matrix[start_pos[0]][start_pos[1]] = '.'
            break
    
    orientations = [(-1,0),(0,1),(1,0),(0,-1)]
    

    def bound(pos):
        assert len(pos) == 2
        bound_x = 0 <= pos[0] < len(matrix)
        bound_y = 0 <= pos[1] < len(matrix[0])
        return bound_x and bound_y
    
    def get_next(pos, orientation):
        return (pos[0] + orientation[0], pos[1] + orientation[1])
    
    def transition_next(pos, orientation):
        while True:
            potential = get_next(pos, orientations[orientation%4])
            if bound(potential) and matrix[potential[0]][potential[1]] == '.':
                return (potential, orientation)
            elif bound(potential) and matrix[potential[0]][potential[1]] == '#':
                orientation += 1
            elif not bound(potential):
                return ((None, None), orientation)

    total_ways_to_add_obstacles = 0
    total = 0
    overall = len(matrix) * len(matrix[0])
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            # No purpose in trying this for an obstacle or start pos
            total += 1
            print(total, overall)
            if (i,j) == start_pos or matrix[i][j] == '#':
                continue

            # Change to obstacle
            matrix[i][j] = '#'
            
            orientation = 0
            sentinel_orientation = 0
        
            current_position = start_pos
            sentinel = start_pos
            # Floyd's tortoise and hare
            # It can be a fluke that they meet up in the same place, so have them meet up
            # multiple times.
            total_meetups = 3
            while True:
                current_position, orientation = transition_next(current_position, orientation)
                if current_position == (None, None):
                    break
                
                sentinel, sentinel_orientation = transition_next(sentinel, sentinel_orientation)
                if sentinel == (None, None):
                    break

                sentinel, sentinel_orientation = transition_next(sentinel, sentinel_orientation)
                if sentinel == (None, None):
                    break
                
                # there must be a cycle since they met at the same point
                if sentinel == current_position:
                    total_meetups -= 1
                    if total_meetups == 0:
                        total_ways_to_add_obstacles += 1
                        break

            # Change back to path
            matrix[i][j] = '.'
                
    
    return total_ways_to_add_obstacles




print(solve_day_6_part_1(get_test_inputs(test_input)))
print(solve_day_6_part_1(get_inputs()))
# 18 m 08 to sort this out


print(solve_day_6_part_2(get_test_inputs(test_input)))
print(solve_day_6_part_2(get_inputs()))
# total 1h 21 m to solve both