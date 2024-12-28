def get_test_inputs(input):
    output = []
    lines = input.split('\n')
    for i, line in enumerate(lines):
        if line == '':
            continue
        output.append(int(line))

    return output


def get_input():
    with open('inputs/input22', 'r') as file:
        return get_test_inputs(file.read())

def secret_function(secret):
    secret_copy = secret
    secret_copy <<= 6
    mixed = secret_copy ^ secret
    secret = mixed % 16777216
    
    secret_copy = secret
    secret_copy >>= 5
    mixed = secret ^ secret_copy
    secret = mixed % 16777216
    
    secret_copy = secret
    secret_copy <<= 11
    mixed = secret ^ secret_copy
    secret = mixed % 16777216
    
    return secret
    
def solve_day_22_part_1(inputs):
    total = 0
    for num in inputs:
        for i in range(2000):
            num = secret_function(num)
        
        total += num
    
    return total

#print(solve_day_22_part_1(get_input()))
# Solved in 30 minutes ( really easy first part this time )

#This is another impossible one :)
# No it's not, just keep track of the last numbers in a queue. 

from collections import deque, defaultdict
import numpy as np
def solve_day_22_part_2(inputs):
    total = 0
    seen_sequences = defaultdict(list)
    for seq_no, num in enumerate(inputs):
        sequences_this_round = set()
        queue = deque([]) # last 5 changes
        print(seq_no)                
        for i in range(2000):
            num = secret_function(num)
            queue.append(num%10)
            if len(queue) == 5:
                price_changes = tuple([int(num) for num in np.convolve(queue, [1,-1], mode = 'valid')])
                last_price = queue[-1]
                if price_changes not in sequences_this_round:
                    sequences_this_round.add(price_changes)
                    seen_sequences[price_changes].append(last_price)
                queue.popleft()
        
    
    max_total = defaultdict(int)
    for k, v in seen_sequences.items():
        max_total[k] = sum(v)
    
    
    return max(max_total.values())

from pprint import pprint as print
print(solve_day_22_part_2(get_input()))
# 48 m 19 - this was actually faster than I expected
