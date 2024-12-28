test_input = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

def get_test_inputs(input):
    towels = []
    patterns = []
    lines = input.split('\n')
    for line in lines:
        if line == '':
            continue
        
        if ',' in line:
            towels.extend(line.split(', '))
        else:
            patterns.append(line)
            
    return towels, patterns

def get_input():
    with open('inputs/input19', 'r') as file:
        return get_test_inputs(file.read())
    

def solve_day_19_part_1(towels, patterns):
    
    def backtrack(pattern, index):
        possible = False
        
        if index == len(pattern):
            return True
        
        for towel in towels:
            possible_matches = len(towel)
            if pattern[index:index+possible_matches] == towel:
                possible = possible or backtrack(pattern, index + possible_matches)
            if possible:
                return True
        
        return possible
    total_possibilities = 0
    for pattern in patterns:
        if backtrack(pattern, 0):
            total_possibilities += 1
            print(pattern)
    
    return total_possibilities


#print(solve_day_19_part_1(*get_input()))
# This must be the quickest backtracking problem I've solved. Took me 12 minutes to implement it.


def solve_day_19_part_2(towels, patterns):
    
    def backtrack(pattern, index):
        possible = False
        
        if index == len(pattern):
            return True
        
        for towel in towels:
            possible_matches = len(towel)
            if pattern[index:index+possible_matches] == towel:
                possible = possible or backtrack(pattern, index + possible_matches)
            if possible:
                return True
            
    def count_posibilities(pattern, index, state = None):
        if state is None:
            state = {}

        number = 0
        
        if index == len(pattern):
            return 1
        
        for towel in towels:
            possible_matches = len(towel)
            if pattern[index:index+possible_matches] == towel:
                if index + possible_matches in state:
                    number += state[index + possible_matches]
                else:
                    added = count_posibilities(pattern, index + possible_matches, state)
                    state[index + possible_matches] = added
                    number += added
                

        return number                

    
    total_possibilities = 0
    for pattern in patterns:
        if backtrack(pattern, 0):
            total_possibilities += count_posibilities(pattern, 0)
            
    
    return total_possibilities

print(solve_day_19_part_2(*get_input()))
# Sorted everything out in 30 minutes. Weee
