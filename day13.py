# System of linear equations.
"""

Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

This is equivalent to

x * 94 + y * 22 = 8400
x * 34 + y * 67 = 5400
Solutions are x = 80 , y = 40

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Equivalent to 
x * 26 + y * 67 = 12748
x * 66 + y * 21 = 12176

There exists a solution for this system, but the solution is 
2 floats

d = 26 * 21 - 67 * 66
dx = 12748 * 21 - 67 * 12176
dy = 26 * 12176 - 66 * 12748

more generally, 

d = x1 y2 - x2 y1
dy = x1 Y - x 2X
dx = X y2 - y1 Y  
dx/d int, dy/d int

3 * dx + dy = total tokens.
Parsing is the biggest hassle.
"""

from collections import deque
test_input = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

from itertools import zip_longest
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


class CoordsAndPrize:
    def __init__(self, lines):
        buttonA = lines[0].split(',')
        self.x1 = int(buttonA[0].replace('X+', ''))
        self.y1 = int(buttonA[1].replace('Y+', ''))
        
        buttonB = lines[1].split(',')
        self.x2 = int(buttonB[0].replace('X+', ''))
        self.y2 = int(buttonB[1].replace('Y+', ''))
        
        prize = lines[2].split(',')
        self.X =  int(prize[0].replace('X=', ''))
        self.Y =  int(prize[1].replace('Y=', ''))
    
    def __repr__(self):
        return f"(x1={self.x1}, y1={self.y1}, x2={self.x2}, y2={self.y2}, X={self.X}, Y={self.Y})"

def get_test_inputs(input):
    matrix = []
    buttons_and_prize_objects = []

    lines = input.split('\n')
    for line in lines:
        if line == '':
            continue
        
        if "Button A: " in line:
            line = line.replace("Button A: ", "")
            matrix.append(line)
        elif "Button B: " in line:
            line = line.replace("Button B: ", "")
            matrix.append(line)
        elif "Prize: ":
            line = line.replace("Prize: ", "")
            matrix.append(line)
        
    
    buttons_and_prizes = list(grouper(matrix, 3))
    
    for buttons_and_prize in buttons_and_prizes:
        buttons_and_prize_objects.append(CoordsAndPrize(buttons_and_prize))
        
    return buttons_and_prize_objects

def get_input():
    with open('inputs/input13', 'r') as file:
        return get_test_inputs(file.read())

def calculate_solutions(coords_and_prize):
    """
        d = x1 y2 - x2 y1
        dy = x1 Y - x 2X
        dx = X y2 - y1 Y  
        dx/d int, dy/d int
        
        x1 x2 = X
        y1 y2 = Y
    """
    
    c_p = coords_and_prize
    determinant = c_p.x1 * c_p.y2 - c_p.x2 * c_p.y1
    determinant_x = c_p.X * c_p.y2 - c_p.Y * c_p.x2
    determinant_y = c_p.x1 * c_p.Y - c_p.y1 * c_p.X
    
    return determinant_x/determinant, determinant_y/determinant
    

def solve_day_13_part_1(inputs):
    
    total_money_needed = 0
    
    for input in inputs:
        x, y = calculate_solutions(input)

        if x.is_integer() and y.is_integer():
            total_money_needed += 3*x + y
    
    return int(total_money_needed)


def solve_day_13_part_2(inputs):
    
    total_money_needed = 0
    
    for i,input in enumerate(inputs):
        input.X += 10000000000000
        input.Y += 10000000000000
        
        x, y = calculate_solutions(input)
        
        if x.is_integer() and y.is_integer():
            total_money_needed += 3*x + y
    
    return int(total_money_needed)

print(solve_day_13_part_1(get_test_inputs(test_input)))
print(solve_day_13_part_1(get_input()))
# Took me 1h 05m to think about it and implement it. Got set back 20 minutes because
# I didn't pay attention to how I arranged my system.

print(solve_day_13_part_2(get_test_inputs(test_input)))
print(solve_day_13_part_2(get_input()))
# Took me 1h 10m overall since I already implemented the optimal solution.
