test_input = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""
def get_test_inputs(input):
    positions = []

    lines = input.split('\n')
    for line in lines:
        if line == '':
            continue
        line = line.split(',')
        positions.append(
            (
                int(line[1]), 
                int(line[0])
            )
        )
    
    return positions

def get_input():
    with open('inputs/input18', 'r') as file:
        return get_test_inputs(file.read())

from utils import bfs

def solve_day_18_part_1(input, matrix_x, matrix_y, start, end, to_use):
    matrix = [['.' for _ in range(matrix_y)] for _ in range(matrix_x)]
    for inp in input[:to_use]:
        matrix[inp[0]][inp[1]] = '#'
        
    return bfs(matrix, start, end, '#')

print(solve_day_18_part_1(get_test_inputs(test_input), 7, 7, (0,0), (6,6), 12))
print(solve_day_18_part_1(get_input(), 71, 71, (0,0), (70,70), 1024))

## Took me 25 minutes

def solve_day_18_part_2(input, matrix_x, matrix_y, start, end, to_use):
    matrix = [['.' for _ in range(matrix_y)] for _ in range(matrix_x)]
    for inp in input[:to_use]:
        matrix[inp[0]][inp[1]] = '#'
    
    result = bfs(matrix, start, end, '#')
    last = to_use - 1
    # This can be done with a binary search.
    # However, since it runs fast enough, I didn't care to optimize it :))
    while result != -1:
        last += 1
        block = input[last]
        matrix[block[0]][block[1]] = '#'
        result = bfs(matrix, start, end, '#')
    
    return last, input[last][::-1]

print(solve_day_18_part_1(get_test_inputs(test_input), 7, 7, (0,0), (6,6), 12))
print(solve_day_18_part_1(get_input(), 71, 71, (0,0), (70,70), 1024))

print(solve_day_18_part_2(get_test_inputs(test_input), 7, 7, (0,0), (6,6), 12))
print(solve_day_18_part_2(get_input(), 71, 71, (0,0), (70,70), 1024))
# Took me 32 minutes overall. After the last one, I needed a break :))