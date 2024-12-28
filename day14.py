"""
import asyncio
from pprint import pprint as print
import os
matrix = [ ['.' for _ in range(11)] for _ in range(7) ]
    
def show(matrix):
    copy = [[num for num in line] for line in matrix]
    for line in copy:
        print(''.join(line))
    
async def animate(initial, velocity, duration, fast_forward):
    matrix[initial[0]][initial[1]] = '1'
    current = initial
    iters = 0
    while True:
        os.system("cls")
        print(f"After {iters*fast_forward}")
        show(matrix)
        await asyncio.sleep(duration)
        matrix[current[0]][current[1]] = '0'
        new_pos = ((current[0] + velocity[0]*fast_forward)%len(matrix), (current[1] + velocity[1]*fast_forward)%len(matrix[0]))
        matrix[new_pos[0]][new_pos[1]] = '1'
        current = new_pos
        iters += 1


        

asyncio.run(animate((4,2), (-3,2), 1, 77))
"""

test_input = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

def get_velocity(part_of_line):
    assert 'v=' in part_of_line
    part_of_line = part_of_line.replace('v=','')
    nums = part_of_line.split(',')
    vx = int(nums[1])
    vy = int(nums[0])
    return vx, vy

def get_position(part_of_line):
    assert 'p=' in part_of_line
    part_of_line = part_of_line.replace('p=','')
    nums = part_of_line.split(',')
    x = int(nums[1])
    y = int(nums[0])
    return x, y

def get_test_inputs(input):
    robots = []

    lines = input.split('\n')
    for line in lines:
        if line == '':
            continue
        
        line = line.split(' ')
        position = get_position(line[0])
        velocity = get_velocity(line[1])
        robots.append([position, velocity])
    return robots

def get_input():
    with open('inputs/input14', 'r') as file:
        return get_test_inputs(file.read())

def solve_day_14_part_1(width, height, robots):
    matrix = [[0 for _ in range(width)] for _ in range(height)]
    fast_forward = 100 # after 100 seconds
    for robot in robots:
        current = robot[0]
        velocity = robot[1]
        new_pos = (
            (current[0] + velocity[0]*fast_forward)%len(matrix), 
            (current[1] + velocity[1]*fast_forward)%len(matrix[0])
        )
        matrix[new_pos[0]][new_pos[1]] += 1
    
    # nulify middle
    mid_width = width//2
    mid_height = height//2
    
    for i in range(height):
        matrix[i][mid_width] = 0
    
    for i in range(width):
        matrix[mid_height][i] = 0
    
    total = 0
    #for line in matrix:
    #    total += sum(line)
    
    def count(start_row, start_col):
        for i in range(start_row, start_row + mid_height):
            for j in range(start_col, start_col + mid_width):
                yield matrix[i][j]
    
    total = (
        sum(count(0,0)) 
        * sum(count(0, mid_width + 1)) 
        * sum(count(mid_height + 1, 0)) 
        * sum(count(mid_height + 1, mid_width + 1))
    )
    
    return total

import asyncio

def show(matrix,iters):
    copy = [[str(num) if num > 0 else '.' for num in line] for line in matrix]
    with open("outputs/day_14_christmas_tree_hopefully", 'a+') as file:
        file.write(f"After {iters}\n")
        for line in copy:
            file.write((''.join(line)) + '\n')
        file.write('\n')
        
def get_state(matrix):
    return tuple([tuple(line) for line in matrix])

async def solve_day_14_part_2(width, height, robots):
    matrix = [[0 for _ in range(width)] for _ in range(height)]
    fast_forward = 1 # after 1 seconds
    
    for robot in robots:
        current = robot[0]
        matrix[current[0]][current[1]] += 1
    seconds = 0
    states = set()
    states.add(get_state(matrix))
    while True:
        seconds += 1

        for robot in robots:
            current = robot[0]
            velocity = robot[1]
            new_pos = (
                (current[0] + velocity[0]*fast_forward)%len(matrix), 
                (current[1] + velocity[1]*fast_forward)%len(matrix[0])
            )
            robot[0] = new_pos
            matrix[current[0]][current[1]] -= 1
            matrix[new_pos[0]][new_pos[1]] += 1
        
        current_state = get_state(matrix) 
        if current_state not in states:
            states.add(current_state)
        else:
            print(f"Broken out after {seconds}")
            break
        show(matrix, seconds)
        
    
    

print(solve_day_14_part_1(11,7,get_test_inputs(test_input)))
print(solve_day_14_part_1(101,103,get_input()))
# Took me 56 m to solve this one. Animation helped a bit :))

#asyncio.run(solve_day_14_part_2(11,7,get_test_inputs(test_input)))
asyncio.run(solve_day_14_part_2(101,103,get_input()))
# I had the idea to animate this from the start to understand better how it works. Took me 1h 43 overall, 
# including to comb through outputs/day_14_christmas tree
# I didn't really know what to expect from the Christmas tree (hollow outline? desnse christmas tree?) 
