def playground(reg_a, reg_b, reg_c, program):

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
            raise Exception("Hello")
        
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
        reg_b = get_combo(operand) & 7
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
        value = get_combo(operand) & 7
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
    
    return output

"""
PROGRAM = [2,4,1,1,7,5,4,6,0,3,1,4,5,5,3,0]

def vary_a(a):
    return playground(a, 0, 0, PROGRAM, a) 

"""
105_734_774_294_938 
"""

from concurrent.futures import ThreadPoolExecutor , as_completed
def worker(i):
    return vary_a(i)
correct = []
def check_parallel_cpu_bound():
    # Define a function to be executed by each process
    

    # Use ProcessPoolExecutor for parallelism
    with ThreadPoolExecutor () as executor:
        # Submit tasks for all values of i in range(1000)
        for j in range(100):

            futures = {executor.submit(worker, i): i for i in range(j*1000,(j+1)*1000)}
            
            # Process results as they complete
            for future in as_completed(futures):
                result = future.result()
                if result[0] == 2411754603145530:
                    correct.append(result[1])

from time import time

#start = time()
#for i in range(100000):
#    vary_a(i)
#print(time() - start, "seq")

#if __name__ == "__main__":
#    start = time()
#    check_parallel_cpu_bound()
#    print(time() - start, "parallel")

def minimized_function(reg_a):
    reg_b = 0
    reg_c = 0
    output = 0
    while reg_a:
        # bst 4
        reg_b = reg_a % 8
        # bxl 1
        reg_b = reg_b ^ 1
        # cdv 5
        reg_c = reg_a //  2 ** reg_b
        # bxc 6
        reg_b = reg_b ^ reg_c
        # adv 3
        reg_a = reg_a // 8
        # bxl 4
        reg_b = reg_b ^ 4
        # out 5
        output = output * 10 + reg_b % 8
        # jnz 0
    
    return output
start = time()
correct = []
for i in range(100_000_000_000_000, 100_000_010_000_000):
    if 2411754603145530 == minimized_function(i):
        correct.append(i)
print(correct)
print(time() - start, "seq")"""

PROGRAM = [2,4,1,1,7,5,4,6,0,3,1,4,5,5,3,0]
# 10794, 10797, 10799 : digits 0:5
# 86352 digits 1:6
# 690816 digits 2:7
# 5526528 digits 3:7
start = 10794 * 8 * 8 * 8

#all_nos = []
#out_len = 0
#changed_size = []
#for i in range(start,start + 100_000 ):
#    output = playground(i, 0, 0, [2,4,1,1,7,5,4,6,0,3,1,4,5,5,3,0])
#    if len(output) > out_len:
#        out_len = len(output)
#        changed_size.append(i)
#    elif len(output) < out_len:
#        out_len = len(output)
#        changed_size.append(i)
#    if PROGRAM[3:8] == output:
#        all_nos.append(i)


starting_points = [0]
for j in range(12):
    new_starting_points = []    
    mult = 1
    for starting_point in starting_points:
        for i in range(0, 100_000):
            
            output = playground(starting_point + i*mult, 0, 0, [2,4,1,1,7,5,4,6,0,3,1,4,5,5,3,0])
            if PROGRAM[j:j+5] == output[0:5]:
                print(output)
                new_starting_points.append(starting_point + i*mult)
        
    for nsp in new_starting_points:
        print(f"{nsp} yields digits [{j}:{j+5}] = [{PROGRAM[j:j+5]}]")
    print()
    mult = mult * 8
    starting_points = [nsp * 8 for nsp in new_starting_points]