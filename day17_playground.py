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

PROGRAM = [
    2,2,
    1,1,
    7,6,
    5,5,
    0,3,
    3,0]
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


def minimized_function(reg_a):
    reg_b = 0
    reg_c = 0
    output = []
    while reg_a:
        # bst 4
        reg_b = reg_a & 7
        # bxl 1
        reg_b = reg_b ^ 1
        # cdv 5
        reg_c = reg_a >> reg_b
        # bxc 6
        reg_b = reg_b ^ reg_c
        # adv 3
        reg_a = reg_a >> 3
        # bxl 4
        reg_b = reg_b ^ 4
        # out 5
        output.append(reg_b & 7)
        # jnz 0
    
    return output

starting_points = {0}
all_starting_points = {}
mult = 1
BITS = 5
MAX_TO_FIND = 40
MULT_MULTIPLIER = 8
numbers = []
for j in range(17 - BITS):
    print(f"Starting bit {j}")
    new_starting_points = set()
    for starting_point in starting_points:
        for i in range(0, max(10**(BITS), 10**5)):
            
            output = playground(starting_point + i*mult, 0, 0, PROGRAM)
            if PROGRAM[j:j+BITS] == output[j:j+BITS]:
                #print(output)
                new_starting_points.add(starting_point + i*mult)
            
            if len(new_starting_points) == MAX_TO_FIND:
                break
        
    for nsp in new_starting_points:
    #    print(f"{nsp} yields digits [{j}:{j+BITS}] = [{PROGRAM[j:j+BITS]}]")
        all_starting_points[tuple(PROGRAM[j:j+BITS])] = all_starting_points.get(tuple(PROGRAM[j:j+BITS]), [])
        all_starting_points[tuple(PROGRAM[j:j+BITS])].append(nsp)
    mult = mult * MULT_MULTIPLIER
    numbers.extend(new_starting_points)
    #print(mult)
    starting_points = [nsp * MULT_MULTIPLIER for nsp in [0]] #new_starting_points]

##numbers = [
##    [10794, 10797, 10799], 
##    [535080], 
##    [6826496], 
##    [73934848, 73935360], 
##    [610803712, 745021440, 749518848, 879239168], 
##    [5174198272, 5174231040, 5174362112, 5174263808, 9200730112, 9200762880, 9200795648, 9200893952, 9469165568, 9469198336, 9469231104, 9469329408, 9603383296, 9603416064, 9603448832, 9603547136, 9607872512, 9608003584], 
##    [43560468480, 77920206848, 78322860032, 78327316480], 
##    [662035234816, 662043623424], 
##    [5882729463808, 6159587082240], 
##    [49040473456640, 51239496712192, 62234612989952, 53438519967744, 57836566478848], 
##    [404714768302080, 405264524115968, 414060617138176, 405281703985152, 413510861324288, 414077797007360, 418458663649280, 418475843518464, 431103047368704, 431652803182592, 431669983051776, 432202558996480, 432423749812224, 434367222513664, 434401582252032, 434435941990400, 456838491406336, 483879605501952, 484429361315840, 484446541185024, 487143780646912, 487178140385280, 487212500123648, 519613733404672, 524011779915776, 488827407826944, 491576186896384, 456391814807552, 456419732094976, 456426174545920, 449262169096192, 449244989227008, 448695233413120, 451959408558080, 451993768296448, 452028128034816, 453643035738112, 453660215607296, 456351012618240, 456357455069184, 488844587696128, 519630913273856, 491610546634752, 492022863495168, 456832048955392, 491535384707072, 491604104183808, 492016421044224, 519063977590784, 491541827158016], 
##    [4706004256161792, 4706554011975680, 4772541889511424, 4706571191844864, 4772524709642240, 4775823244525568, 4775840424394752, 4775849014329344, 4776192611713024, 4776373000339456, 4776922756153344, 4776939936022528, 4780221291036672, 4780238470905856, 4987479232872448, 4988028988686336, 4995622490865664, 4995210174005248, 4995596721061888, 4995613900931072, 4990777767755776, 4990743408017408, 4988046168555520, 4990812127494144, 4992427035197440, 4992444215066624, 4995132864593920, 4995141454528512, 4995175814266880, 4995201584070656]
##]
#print(numbers)
all_nums = sorted([n for n in numbers])
print(all_nums)
#all_nums = [10794, 10797, 10799, 535080, 6826496, 73934848, 73935360, 610803712, 745021440, 749518848, 879239168, 5174198272, 5174231040, 5174263808, 5174362112, 9200730112, 9200762880, 9200795648, 9200893952, 9469165568, 9469198336, 9469231104, 9469329408, 9603383296, 9603416064, 9603448832, 9603547136, 9607872512, 9608003584, 43560468480, 77920206848, 78322860032, 78327316480, 662035234816, 662043623424, 5882729463808, 6159587082240, 49040473456640, 51239496712192, 53438519967744, 57836566478848, 62234612989952, 404714768302080, 405264524115968, 405281703985152, 413510861324288, 414060617138176, 414077797007360, 418458663649280, 418475843518464, 431103047368704, 431652803182592, 431669983051776, 432202558996480, 432423749812224, 434367222513664, 434401582252032, 434435941990400, 448695233413120, 449244989227008, 449262169096192, 451959408558080, 451993768296448, 452028128034816, 453643035738112, 453660215607296, 456351012618240, 456357455069184, 456391814807552, 456419732094976, 456426174545920, 456832048955392, 456838491406336, 483879605501952, 484429361315840, 484446541185024, 487143780646912, 487178140385280, 487212500123648, 488827407826944, 488844587696128, 491535384707072, 491541827158016, 491576186896384, 491604104183808, 491610546634752, 492016421044224, 492022863495168, 519063977590784, 519613733404672, 519630913273856, 524011779915776, 524028959784960, 554248349679616, 554798105493504, 554815285362688, 558096640376832, 558113820246016, 559196152004608, 559213331873792, 562494686887936, 562511866757120, 562522604175360, 562934921035776, 4706004256161792, 4706554011975680, 4706571191844864, 4772524709642240, 4772541889511424, 4775823244525568, 4775840424394752, 4775849014329344, 4776192611713024, 4776373000339456, 4776922756153344, 4776939936022528, 4780221291036672, 4780238470905856, 4987479232872448, 4988028988686336, 4988046168555520, 4990743408017408, 4990777767755776, 4990812127494144, 4992427035197440, 4992444215066624, 4995132864593920, 4995141454528512, 4995175814266880, 4995201584070656, 4995210174005248, 4995596721061888, 4995613900931072, 4995622490865664, 5057847977050112, 5058397732864000, 5058414912733184, 5061696267747328, 5061713447616512, 5062795779375104, 5062812959244288, 5066094314258432, 5066111494127616, 5066120084062208, 5066532400922624, 5335474663063552, 5335491842932736, 5338773197946880, 5338790377816064, 5338798967750656, 5339142565134336]


def count_trailing_zeros(num):
    trailing_zeros = 0
    while num % 2 != 1 :
        num = num // 2
        trailing_zeros += 1
    return trailing_zeros

from collections import deque

#for num in all_nums:
#    zeros = count_trailing_zeros(num) 
#    if zeros <= 3:
#        queue.append((num, zeros))    


def overlapping(num1, num2, overlapping_num):
    
    potential_overlap = num1 & num2
    copy = potential_overlap
    while copy > 0 and copy % 2 != 1:
        copy //= 2
    
    if copy == 0 or len(bin(copy)[2:]) >= overlapping_num :
        return False # likely same, too much overlap OR no overlap
    
    binary_rep_of_overlap = list(bin(potential_overlap)[2:])
    
    left = 0
    right = len(binary_rep_of_overlap) - 1
    
    
    while binary_rep_of_overlap[left] == '0':
        left += 1
    
    while binary_rep_of_overlap[right] == '0':
        right -= 1
    
    while left < right:
        binary_rep_of_overlap[left] = '1'
        left +=1 
    
    mask = int(''.join(binary_rep_of_overlap),2)
    
    n1 = num1 & mask
    n2 = num2 & mask
    
    if (n1 ^ n2) & potential_overlap == 0:
        return True
    
    return False
    
    
    
    

queue = deque(all_nums[0:3])
cands = []
seen = set()
while queue:
    current = queue.popleft()
    for num in all_nums:
        if num < current:
            continue    
        if overlapping(current, num, 20) and num | current not in seen:
            queue.append(num | current)
            seen.add(num | current)
    if len(minimized_function(current)) >= len(PROGRAM):
        cands.append(current) 

highest = 0
nums = []
for cand in cands:
    h = 0
    if minimized_function(cand) == PROGRAM:
        nums.append(cand)
print(highest, nums)
print("Fin")

#spaces_reqed = 0
#acc = 0
#for num in all_nums:
#    trailing_zeros = count_trailing_zeros(num)
#    if trailing_zeros >= spaces_reqed:
#        acc ^= num
#        spaces_reqed = len(bin(acc)[2:])
#
#print(acc)
#
#print(minimized_function(404715517831722))