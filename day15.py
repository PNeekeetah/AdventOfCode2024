import asyncio

test_input1 = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

test_input2 = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

test_input3 = """#################
#..O..O..O......#
#......O........#
#.OO..O..O......#
#..OO@..O.O.O.O.#
#O#..O..........#
#O..O..O........#
#.OO.O.OO.......#
#....O..........#
#################

>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>><<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>"""

test_input4 = """#############
#.....@......#
#.....O...#
#.....OO.....#
#....OOO.....#
#...........#
#############

<v>^>vvv
"""

def get_test_inputs(input):
    matrix = []
    moves = []
    lines = input.split('\n')
    start_pos = None
    for row, line in enumerate(lines):
        if line == '':
            continue
        
        if '@' in line:
            line = list(line)
            start_pos = (row, line.index('@'))
            line[start_pos[1]] = '.'
            matrix.append(line)
        elif '#' in line:
            matrix.append(list(line))
        elif '^' in line or 'v' in line or '>' in  line or '<' in line:
            moves.extend(list(line))
        
    return start_pos, matrix, moves

def get_input():
    with open('inputs/input15', 'r') as file:
        return get_test_inputs(file.read())

def expand(current):
    match current:
        case '#':
            return ['#','#']
        case '@':
            return ['@','.']
        case 'O':
            return ['[',']']
        case '.':
            return ['.','.']
        case default:
            return [current]
    

def get_greater_test_inputs(input):
    matrix = []
    moves = []
    lines = input.split('\n')
    start_pos = None
    for row, line in enumerate(lines):
        if line == '':
            continue
        
        new_line = []
        for c in line:
            new_line.extend(expand(c))
        
        if '@' in line:
            start_pos = (row, new_line.index('@'))
            new_line[start_pos[1]] = '.'
            matrix.append(new_line)
        elif '#' in line:
            matrix.append(new_line)
        elif '^' in line or 'v' in line or '>' in  line or '<' in line:
            moves.extend(new_line)
    
    copy = [''.join(line) for line in matrix]
    #from pprint import pprint as print
    #print(copy, width=100)
    return start_pos, matrix, moves

def get_greater_input():
    with open('inputs/input15', 'r') as file:
        return get_greater_test_inputs(file.read())


from pprint import pprint as print

def tests():
    start_pos, matrix, moves = get_test_inputs(test_input1)
    assert start_pos == (2,2)
    assert len(matrix) == 8
    assert len(matrix[0]) == 8
    assert isinstance(moves, list) and isinstance(moves[0], str)
    assert len(set(moves)) == 4
    
    greater_start_pos, greater_matrix, greater_moves = get_greater_test_inputs(test_input1)
    assert greater_start_pos == (start_pos[0],start_pos[1] * 2)
    assert len(greater_matrix) == len(matrix)
    assert len(greater_matrix[0]) == len(matrix[0]) * 2
    assert isinstance(greater_moves, list) and isinstance(moves[0], str)
    assert len(set(greater_moves)) == 4

    start_pos, matrix, moves = get_test_inputs(test_input2)
    assert start_pos == (4,4)
    assert len(matrix) == 10
    assert len(matrix[0]) == 10
    assert isinstance(moves, list) and isinstance(moves[0], str)
    assert len(set(moves)) == 4
    
    greater_start_pos, greater_matrix, greater_moves = get_greater_test_inputs(test_input2)
    assert greater_start_pos == (start_pos[0],start_pos[1] * 2)
    assert len(greater_matrix) == len(matrix)
    assert len(greater_matrix[0]) == len(matrix[0]) * 2
    assert isinstance(greater_moves, list) and isinstance(moves[0], str)
    assert len(set(greater_moves)) == 4
    

tests()

from utils import show_matrix
async def solve_day_15_part_1(start_pos, matrix, moves):


    def get_new_position(pos, direction):
        return (pos[0] + direction[0], pos[1] + direction[1])

    def move(pos, orientation):                
        """
        >.#...
        >#....
        >O#...
        >O.#..
        >OOOO.#
        >OOOO#
        test cases
        """
        stop_symbols = {'#', '.'}
        directions = {
            '^' : (-1,0),
            '>' : (0,1),
            '<' : (0,-1),
            'v' : (1,0)
        }
        direction = directions[orientation]
        new_pos = get_new_position(pos, direction)
        while matrix[new_pos[0]][new_pos[1]] not in stop_symbols:
            new_pos = get_new_position(new_pos, direction)
        next_pos = get_new_position(pos, direction)

        
        if matrix[new_pos[0]][new_pos[1]] == '#':
            # cannot move because a wall is in the way:
            return pos
        elif matrix[new_pos[0]][new_pos[1]] == '.':
            matrix[new_pos[0]][new_pos[1]], matrix[next_pos[0]][next_pos[1]] = matrix[next_pos[0]][next_pos[1]], matrix[new_pos[0]][new_pos[1]]
            matrix[pos[0]][pos[1]] = '.'
            matrix[next_pos[0]][next_pos[1]] = orientation
            return next_pos
    
    current = start_pos
    
    for i, m in enumerate(moves):
        #print(m)
        current = move(current, m)
        #show_matrix(matrix, i)
        #await asyncio.sleep(0.5)
    total = 0
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 'O':
                total += i * 100 + j
    
    return total

async def solve_day_15_part_1(start_pos, matrix, moves):


    def get_new_position(pos, direction):
        return (pos[0] + direction[0], pos[1] + direction[1])

    def move(pos, orientation):                
        """
        >.#...
        >#....
        >O#...
        >O.#..
        >OOOO.#
        >OOOO#
        test cases
        """
        stop_symbols = {'#', '.'}
        directions = {
            '^' : (-1,0),
            '>' : (0,1),
            '<' : (0,-1),
            'v' : (1,0)
        }
        direction = directions[orientation]
        new_pos = get_new_position(pos, direction)
        while matrix[new_pos[0]][new_pos[1]] not in stop_symbols:
            new_pos = get_new_position(new_pos, direction)
        next_pos = get_new_position(pos, direction)

        
        if matrix[new_pos[0]][new_pos[1]] == '#':
            # cannot move because a wall is in the way:
            return pos
        elif matrix[new_pos[0]][new_pos[1]] == '.':
            matrix[new_pos[0]][new_pos[1]], matrix[next_pos[0]][next_pos[1]] = matrix[next_pos[0]][next_pos[1]], matrix[new_pos[0]][new_pos[1]]
            matrix[pos[0]][pos[1]] = '.'
            matrix[next_pos[0]][next_pos[1]] = orientation
            return next_pos
    
    current = start_pos
    
    for i, m in enumerate(moves):
        #print(m)
        current = move(current, m)
        #show_matrix(matrix, i)
        #await asyncio.sleep(0.5)
    total = 0
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 'O':
                total += i * 100 + j
    
    return total
        
#print(asyncio.run(solve_day_15_part_1(*get_test_inputs(test_input1))))
#print(asyncio.run(solve_day_15_part_1(*get_test_inputs(test_input2))))
        
#print(asyncio.run(solve_day_15_part_1(*get_input())))

from utils import show_matrix
from collections import deque
async def solve_day_15_part_2(start_pos, matrix, moves):


    def get_new_position(pos, direction):
        return (pos[0] + direction[0], pos[1] + direction[1])

    def get_candidates(pos, orientation):
        if orientation == '^':
            directions = [(-1,-1), (-1,0), (-1,1)] # topleft, up, topright
        else:
            directions = [(1,-1), (1,0), (1,1)] # bottomleft, down, bottomright


        allowed = ['[',']']
        
        for i,d in enumerate(directions):
            
            new_pos = (pos[0] + d[0], pos[1] + d[1])
            ob2 = matrix[new_pos[0]][new_pos[1]]
            if ob2 not in allowed:
                continue

            
            if i != 1:
                ob1 = matrix[pos[0]][pos[1]]
                if ob1 != ob2:
                    continue
            yield new_pos
        
        left = (0,-1)
        right = (0,1)
        left = (pos[0], pos[1] - 1)
        right = (pos[0], pos[1] + 1)
        
        if matrix[pos[0]][pos[1]] == ']' and matrix[left[0]][left[1]] == '[':
            yield left
        
        if matrix[pos[0]][pos[1]] == '[' and matrix[right[0]][right[1]] == ']':
            yield right
        

            
            
    def get_all_objects(pos,orientation):
        queue = deque([pos])
        seen = set()
        while queue:
            current = queue.popleft()
            for candidate in get_candidates(current, orientation):
                if candidate not in seen:
                    seen.add(candidate)
                    queue.append(candidate)
        
        return sorted(list(seen), key = lambda x: (-x[0],x[1]) if orientation == 'v' else (x[0],x[1]) )
        
    def check_for_obstacle(pos, orientation):
        d = (1,0) if orientation == 'v' else (-1,0)
        new = get_new_position(pos, d)
        if matrix[new[0]][new[1]] == '#':
            return True

        return False
    
    def shift_objects(object_positions, orientation):        
        d = (1,0) if orientation == 'v' else (-1,0)
        for object_pos in object_positions:
            new_pos = get_new_position(object_pos, d)
            matrix[object_pos[0]][object_pos[1]], matrix[new_pos[0]][new_pos[1]] = matrix[new_pos[0]][new_pos[1]], matrix[object_pos[0]][object_pos[1]]
        

    def move_up_down(pos, orientation):
        directions = {
            '^' : (-1,0),
            'v' : (1,0)
        }

        
        direction = directions[orientation]
        new_pos = get_new_position(pos, direction)
        # Trivial case
        if matrix[new_pos[0]][new_pos[1]] == '.':
            matrix[pos[0]][pos[1]], matrix[new_pos[0]][new_pos[1]] = matrix[new_pos[0]][new_pos[1]], matrix[pos[0]][pos[1]]
            matrix[pos[0]][pos[1]] = '.'
            matrix[new_pos[0]][new_pos[1]] = orientation
            return new_pos
        elif matrix[new_pos[0]][new_pos[1]] in ['[',']']:
            object_positions = get_all_objects(new_pos,orientation)
            print(object_positions)
            for object_pos in object_positions:

                if check_for_obstacle(object_pos, orientation):
                    return pos
            shift_objects(object_positions, orientation)
            
            matrix[pos[0]][pos[1]], matrix[new_pos[0]][new_pos[1]] = matrix[new_pos[0]][new_pos[1]], matrix[pos[0]][pos[1]]
            matrix[pos[0]][pos[1]] = '.'
            matrix[new_pos[0]][new_pos[1]] = orientation
            return new_pos
        # Cannot got through walls
        elif matrix[new_pos[0]][new_pos[1]] == '#':
            return pos

        return pos
    
    def move_left_right(pos, orientation):
        stop_symbols = {'#', '.'}
        directions = {
            '>' : (0,1),
            '<' : (0,-1),
        }
        inverses = {
            '>' : '<',
            '<' : '>'
        }
        direction = directions[orientation]
        new_pos = get_new_position(pos, direction)
        
        direction = directions[orientation]
        new_pos = get_new_position(pos, direction)
        while matrix[new_pos[0]][new_pos[1]] not in stop_symbols:
            new_pos = get_new_position(new_pos, direction)
        next_pos = get_new_position(pos, direction)

        
        if matrix[new_pos[0]][new_pos[1]] == '#':
            # cannot move because a wall is in the way:
            return pos
        elif matrix[new_pos[0]][new_pos[1]] == '.':
            while new_pos != pos:
                back = get_new_position(new_pos, directions[inverses[orientation]])
                matrix[back[0]][back[1]], matrix[new_pos[0]][new_pos[1]] = matrix[new_pos[0]][new_pos[1]], matrix[back[0]][back[1]]
                new_pos = back
            matrix[pos[0]][pos[1]] == '.'
            matrix[next_pos[0]][next_pos[1]] = orientation
            return next_pos

    def move(pos, orientation):                

        if orientation in ['<','>']:
            return move_left_right(pos, orientation)
        else:
            return move_up_down(pos, orientation)
        
    
    current = start_pos
    
    for i, m in enumerate(moves):
        #print(m)
        current = move(current, m)
        #show_matrix(matrix, i)
        #print('')
        #await asyncio.sleep(0.1)
    
    total = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == '[':
                total += i * 100 + j
                
    return total


# It probably took me around 40-50 m to implement (forgot to start the stopwatch and it shows only 27 m)

#print(asyncio.run(solve_day_15_part_2(*get_greater_test_inputs(test_input2))))
print(asyncio.run(solve_day_15_part_2(*get_greater_input())))

# the timer shows 2h 51m 28, , so overall it likely took me between 3h and 3h 10 to solve everything.
# this one was fairly brutal