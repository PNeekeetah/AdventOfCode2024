import numpy as np
import asyncio
import itertools
test_input = """0 1 10 99 999"""

def get_test_inputs(input):
    stones = []

    lines = input.split('\n')
    for line in lines:
        line = line.split()
        if line == '':
            continue
        stones.extend([int(num) for num in line])
    return stones

def get_input():
    with open('inputs/input11', 'r') as file:
        return get_test_inputs(file.read())
    
def solve_day_11_part_1(stones):
    for _ in range(25):
        new_stones = []
        
        for stone in stones:
            
            if stone == 0:
                new_stones.append(1)
            elif len(str(stone)) % 2 == 0:
                stone = str(stone)
                length = len(stone)
                new_stones.append(int(stone[0:length//2]))
                new_stones.append(int(stone[length//2:]))
            else:
                new_stones.append(2024*stone)
            
        stones = new_stones
    return len(stones)

def solve_day_11_part_2(stones):
    seen = set()
    for _ in range(25):
        new_stones = []
        
        for stone in stones:
            
            if stone == 0:
                new_stones.append(1)
            elif len(str(stone)) % 2 == 0:
                stone = str(stone)
                length = len(stone)
                new_stones.append(int(stone[0:length//2]))
                new_stones.append(int(stone[length//2:]))
            else:
                new_stones.append(2024*stone)
            seen.add(int(stone))
        
        stones = new_stones

    return seen




#print(solve_day_11_part_1(get_test_inputs(test_input)))
#print(solve_day_11_part_1(get_input()))

# took about 13 minutes to write the simulation

#seen_3998391 = solve_day_11_part_2(get_test_inputs("3998391"))

#print(seen_3998391)
#x = [773,79858,0,71,2937,1,3998391]
#y = [0,1,71,2937]
#z = [79858,3998391]
#common = None
#for num in sorted(z):
#    if common is None:
#        common = solve_day_11_part_2([num])
#    else:
#        new = solve_day_11_part_2([num])
#        print(num, sorted(new - common))
#        print(len(common), len(new - common))
#        common = common.intersection(new)
#
#print(sorted(common))
    


#print(solve_day_11_part_2(get_test_inputs("100")))
#
#def spawns_per_generation(number):
#    number = [number]
#    lengths = [len(number)]
#    for i in range(51):
#        print(i)
#        new_stones = []
#        for stone in number:
#            if stone == 0:
#                new_stones.append(1)
#            elif len(str(stone)) % 2 == 0:
#                stone = str(stone)
#                length = len(stone)
#                new_stones.append(int(stone[0:length//2]))
#                new_stones.append(int(stone[length//2:]))
#            else:
#                new_stones.append(2024*stone)
#        lengths.append(len(new_stones))
#        print(lengths)
#        number = new_stones
#    
#    return lengths
#
#print(0, spawns_per_generation(0))        


"""

async def calculate(stones):
    new_stones = []
    for stone in stones:
            
        if stone == 0:
            new_stones.append(1)
        elif len(str(stone)) % 2 == 0:
            stone = str(stone)
            length = len(stone)
            new_stones.append(int(stone[0:length//2]))
            new_stones.append(int(stone[length//2:]))
        else:
            new_stones.append(2024*stone)
        
    return new_stones

async def calculate_async(stones):
    split_arrays = np.array_split(stones, 100)
    ops = []
    for array in split_arrays:
        ops.append(calculate(array))
    
    result = await asyncio.gather(*ops)
    return  list(itertools.chain(*result))

async def stone_calc(stones):
    new_stones = stones
    for i in range(50):
        print(i)
        new_stones = await calculate_async(new_stones)
    
    return len(new_stones)
    
"""


"""
gen(31) a lui 10 = gen(30) a lui 0  + gen(30) a lui 1
"""
from collections import Counter
from functools import cache

@cache
def calculate_stones(number):
    new_stones = []
    stones = [number]
    
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        elif len(str(stone)) % 2 == 0:
            stone = str(stone)
            length = len(stone)
            new_stones.append(int(stone[0:length//2]))
            new_stones.append(int(stone[length//2:]))
        else:
            new_stones.append(2024*stone)
    

    return new_stones

@cache
def calculate_stones_25_iter(number):
    stones = [number]
    for i in range(25):
        new_stones = []
        
        for stone in stones:
            new_stones.extend(calculate_stones(stone))
        stones = new_stones
    
    return Counter(new_stones)


def calc_stones(stones):
    all_counter = Counter(stones)
    for i in range(3):
        new_counter = Counter()
        for stone in all_counter:
            counter = calculate_stones_25_iter(stone)
            for k in counter:
                if k in new_counter:
                    new_counter[k] += counter[k] * all_counter[stone]
                else:
                    new_counter[k] = counter[k] * all_counter[stone]
        all_counter = new_counter
    return sum(all_counter.values())

print(calc_stones(get_input()))

# Easily took me 4 or 5 hours to get here. I had a look at a discussion online and I found somebody who mentioned 
# caching it in a map. I guess I'm really stupid since I didn't think of that :))
