
test_input = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

test_input_2 = """Register A: 117440
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""

def get_test_inputs(input):
    reg_a = None
    reg_b  = None
    reg_c = None
    program = []
    lines = input.split('\n')
    for i, line in enumerate(lines):
        if line == '':
            continue
        
        if "Register A:" in line:
            line = line.replace("Register A:", '')
            reg_a = int(line)
        elif "Register B:" in line:
            line = line.replace("Register B:", '')
            reg_b = int(line)
        elif "Register C:" in line:
            line = line.replace("Register C:", '')
            reg_c = int(line)
        elif "Program:" in line:
            line = line.replace("Program:", '')
            program.extend([int(num) for num in line.split(',')])

    return reg_a, reg_b, reg_c, program


def get_input():
    with open('inputs/input17', 'r') as file:
        return get_test_inputs(file.read())

#print(get_test_inputs(test_input))
#print(get_input())

def solve_day_17_part_1(reg_a, reg_b, reg_c, program):
    """
    0 - adv - combo 
    1 - bxl - literal
    2 - bst - combo
    3 - jnz - literal
    4 - bxc - operand ignored
    5 - out - combo
    6 - bdv - combo
    7 - cdv - combo
    
    Values :
    0 - 3 literals
    
    if combo:
    4 - 6 - registers A through C
    7 - reserved
    
    if not combo:
    4 - 7  literals
    """
    tape_head = 0
    output = []    
    
    def get_literal(operand):
        return operand
    
    def get_combo(operand):
        nonlocal reg_a, reg_b, reg_c
        if operand == 4:
            return reg_a
        elif operand == 5:
            return reg_b
        elif operand == 6:
            return reg_c
        elif operand == 7:
            raise Exception("This shouldn't occur.")
        
        return operand
    
    def adv(operand):
        nonlocal reg_a, tape_head
        numerator = reg_a
        denominator = 2 ** get_combo(operand)
        reg_a = numerator // denominator
        tape_head += 2
        
    def bxl(operand):
        nonlocal reg_b, tape_head
        reg_b = reg_b ^ get_literal(operand)
        tape_head += 2
        
    def bst(operand):
        nonlocal reg_b, tape_head
        reg_b = get_combo(operand) % 8
        tape_head += 2
        
    def jnz(operand):
        nonlocal reg_a, tape_head
        if reg_a == 0:
            tape_head += 2
            return
        
        tape_head = get_literal(operand)
        
    def bxc(operand):
        nonlocal reg_b, reg_c, tape_head
        reg_b = reg_b ^ reg_c
        tape_head += 2
        
    def out(operand):
        nonlocal output, tape_head
        value = get_combo(operand) % 8
        output.append(value)
        tape_head += 2
    
    def bdv(operand):
        nonlocal reg_a, reg_b, tape_head
        numerator = reg_a
        denominator = 2 ** get_combo(operand)
        reg_b = numerator // denominator
        tape_head += 2

    def cdv(operand):
        nonlocal reg_a, reg_c, tape_head
        numerator = reg_a
        denominator = 2 ** get_combo(operand)
        reg_c = numerator // denominator
        tape_head += 2
    
    opcodes = {
        0 : adv,
        1 : bxl,
        2 : bst,
        3 : jnz,
        4 : bxc,
        5 : out,
        6 : bdv,
        7 : cdv,
    }
        
    while tape_head < len(program):
        opcodes[program[tape_head]](program[tape_head+1])
 
    return ','.join([str(num) for num in output])

#print(solve_day_17_part_1(*get_test_inputs(test_input)))
#print(solve_day_17_part_1(*get_input()))
# Done after 50 minutes. Not hard at all to solve the first part, just took me a while to copy it down.





def solve_day_17_part_2(reg_a, reg_b, reg_c, program):

    tape_head = 0
    output = []    
    
    def get_literal(operand):
        return operand
    
    def get_combo(operand):
        nonlocal reg_a, reg_b, reg_c
        if operand == 4:
            return reg_a
        elif operand == 5:
            return reg_b
        elif operand == 6:
            return reg_c
        elif operand == 7:
            raise Exception("This shouldn't occur")
        
        return operand
    
        
    def adv(_):
        nonlocal reg_a, tape_head
        reg_a = reg_a // 8
        tape_head += 2
        
    def bxl(operand):
        nonlocal reg_a, reg_b, tape_head
        reg_b = reg_b ^ (1 if operand == 1 else 4)
        tape_head += 2
        
    def bst(_):
        nonlocal reg_b, tape_head
        reg_b = reg_a % 8
        tape_head += 2
        
    def jnz(operand):
        nonlocal reg_a, tape_head
        if reg_a == 0:
            tape_head += 2
            return
        
        tape_head = get_literal(operand)
        
    def bxc(_):
        nonlocal reg_b, reg_c, tape_head
        reg_b = reg_b ^ reg_c
        tape_head += 2
        
    def out(operand):
        nonlocal output, tape_head
        output.append(reg_b % 8)
        tape_head += 2
    

    def cdv(_):
        nonlocal reg_a, reg_c, tape_head
        reg_c = reg_a // 2 ** reg_b
        tape_head += 2
    
    opcodes = {
        0 : adv,
        1 : bxl,
        2 : bst,
        3 : jnz,
        4 : bxc,
        5 : out,
        7 : cdv,
    }
    left = 0
    right = 2**64
    def get_number(input):
        return int(''.join([str(num) for num in input]))
    
    while tape_head < len(program):
        print(opcodes.get(program[tape_head]).__name__)
        opcodes.get(program[tape_head])(program[tape_head+1])
    
    return output



#print(solve_day_17_part_2(*get_test_inputs(test_input_2)))
#print(solve_day_17_part_2(*get_input()))
#print(*get_test_inputs(test_input_2))

"""
2,4,1,1,7,5,4,6,0,3,1,4,5,5,3,0
adv - a number such that // 8 and then % 8 I get 2
out - a number such that % 8 i get 2
jnz - I should be at the end with this one.

x // 8 % 8 = 2
x // 8 = 18, 26, 34, 42... 

Say 18.

In my case, commands are

2 - bst 
1 - bxl 
7 - cdv
4 - bxc
0 - adv
1 - bxl
5 - out
3 - jnz

2,4,1,1,7,5,4,6,0,3,1,4,5,5,3,0

reg_a = 0 at the end
reg_b = 0 at the end

"""

#print(solve_day_17_part_2(*get_input()))

""" 
35184372089089

"""


"""
1 3 2 5 3 6 0 2 3 2 1 5 2 4 0 2 3 2 5 1 



6 4 1 0 3 5 2 5 

"""

#print(solve_day_17_part_1(*get_test_inputs(f"""Register A: {8*8*8*8*8*8*8*8*8*8*8*8*8*8*8*7 + 2**44 + 2**43 + 2**42 + 2**41 + 2**40 + 2**39 + 2**38 + 2**37 + 2*sum([2**i for i in range(36)]) }
#Register B: 0
#Register C: 0
#
#Program: 2,4,1,1,7,5,4,6,0,3,1,4,5,5,3,0""")))

"""
bst 4 
bxl 1
cdv 5
bxc 6
adv 3
bxl 4
out 5
jnz 0 

2,4,
1,1,
7,5,
4,6,
0,3,
1,4,
5,5,
3,0
"""

from numpy import convolve
numbers = []

for i in range(10000):
    result = solve_day_17_part_1(*get_test_inputs(f"""Register A: {i}
Register B: 0
Register C: 0

Program: 2,4,1,1,7,5,4,6,0,3,1,4,5,5,3,0""")) 
    result = int(''.join(result.split(',')))
    numbers.append(result)
    

print(list(filter(lambda x : x != None,[int(num) for num in convolve(numbers, [1], mode='valid')])))

### It took me 5 hours 42 overall. Another 4 hours 42 spent to NOT find a solution :)
### Extra 1 hour and 4 spent today <3 no solution still
### I think I spent an extra 7-8 hours on this one to solve it (passively tried other ideas until I came up with the right one)
### Overall, I spent likely around 14-15 hours to solve this one