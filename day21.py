from collections import deque
"""
029A
(r1 - numeric)  <A^A^^>AvvvA
(r2 - keypad) v<<A>>^A

000A

"""

def get_test_inputs(input):
    output = []
    lines = input.split('\n')
    for i, line in enumerate(lines):
        if line == '':
            continue
        output.append(line)

    return output


def get_input():
    with open('inputs/input21', 'r') as file:
        return get_test_inputs(file.read())

from pprint import pprint as print
def solve_day_21_part_1(codes,r):
    
    numeric_pad = [
        ['7','8','9'],
        ['4','5','6'],
        ['1','2','3'],
        [None,'0','A'],   
    ]
    
    num_pad_positions_to_letter = {
        '7' : (0,0), '8' : (0,1), '9' : (0,2),
        '4' : (1,0), '5' : (1,1), '6' : (1,2),
        '1' : (2,0), '2' : (2,1), '3' : (2,2),
        None : (3,0), '0' : (3,1), 'A' : (3,2)
    }
    
    arrow_pad = [
        [None, '^', 'A'],
        ['<','v','>'],
    ]
    
    key_pad_positions_to_symbol = {
        None : (0,0), '^' : (0,1), 'A' : (0,2),
        '<' : (1,0), 'v' : (1,1), '>' : (1,2)
    }
    
    def bound(position, matrix):
        assert len(position) == 2
        bound_x = 0 <= position[0] < len(matrix)
        bound_y = 0 <= position[1] < len(matrix[0])
        return bound_x and bound_y
    
    def get_candidate(position,matrix,r, keypad):
        ds = [
            ((0,-1),'<'),
            ((-1,0),'^'),
            ((1,0),'v'),
            ((0,1), '>'),
        ]  # ((0,1), '>'),((1,0),'v'),((-1,0),'^'),((0,-1),'<')
        print(keypad)
        if keypad:
            ds = [
                ((0,-1),'<'),
                ((-1,0),'^'),
                ((1,0),'v'),
                ((0,1), '>'),
            ]
        for d, sym in ds:
            new = (position[0] + d[0], position[1] + d[1])
            if bound(new, matrix): #and matrix[new[0]][new[1]] is not None:
                yield new, sym
    
    def bfs(start, matrix,r, keypad = False):
        
        queue = deque([(start, '')])
        seen = {start : ''}
        while queue:
            current, order = queue.popleft()
            
            for candidate, symbol in get_candidate(current, matrix,r, keypad):
                if candidate not in seen:
                    queue.append((candidate, order + symbol))
                    seen[candidate] = order + symbol
        return {k:v + 'A' for k,v in seen.items()}
        
    
    position_to_num_pad = {v:k for k,v in num_pad_positions_to_letter.items()}
    position_to_arrow_pad = {v:k for k,v in key_pad_positions_to_symbol.items()}
    
    best_numpad_transitions = {}
    for i in range(len(numeric_pad)):
        for j in range(len(numeric_pad[0])):
            if numeric_pad[i][j] == None:
                continue
            position = (i,j)
            current_letter = position_to_num_pad[position]
            for k,v in bfs(position, numeric_pad,r, True).items():
                best_numpad_transitions[current_letter + position_to_num_pad[k]] = v
    
    best_arrow_pad_transitions = {}
    for i in range(len(arrow_pad)):
        for j in range(len(arrow_pad[0])):
            if arrow_pad[i][j] == None:
                continue
            position = (i,j)
            current_symbol = position_to_arrow_pad[position]
            for k,v in bfs(position, arrow_pad,r).items():
                best_arrow_pad_transitions[current_symbol + position_to_arrow_pad[k]] = v
    
    print(best_arrow_pad_transitions)
    print(best_numpad_transitions)
    
    # Process now!
    
    # First robot typing onto the numpad
    code_to_numpad = []
    for code in codes:
        code = 'A' + code 
        sequence = ""
        for i in range(0, len(code)-1):
            sequence += best_numpad_transitions[code[i:i+2]]
        code_to_numpad.append(sequence)
    print(code_to_numpad[4])
    # Second robot typing into the numpad
    numpad_to_numpad1 = []
    for code in code_to_numpad:
        code = 'A' + code 
        sequence = ""
        for i in range(0, len(code)-1):
            sequence += best_arrow_pad_transitions[code[i:i+2]]
        numpad_to_numpad1.append(sequence)
        
    print(numpad_to_numpad1[4])
    # Second robot typing into the numpad
    numpad_to_numpad2 = []
    for code in numpad_to_numpad1:
        code = 'A' + code 
        sequence = ""
        for i in range(0, len(code)-1):
            sequence += best_arrow_pad_transitions[code[i:i+2]]
        numpad_to_numpad2.append(sequence)
    
    print(numpad_to_numpad2)
    
    print([len(code) for code in numpad_to_numpad2])

    total = 0
    for code, total_keypresses in zip(codes, numpad_to_numpad2):
        code = int(code.replace('A',''))
        total += code * len(total_keypresses) 
    
    return total


#solve_day_21_part_1(get_test_inputs("""029A
#980A
#179A
#456A
#379A"""),0)
#solve_day_21_part_1(get_input())

# 2 hours in so far and I realised that this won't work as it is.
# The reason why this doesn't work is because from A to < there are 2 possible paths: <v< and v<<. At level 1, this doesn't cause a disturbance
# but 2 levels in, it might. Just shifting around the arrows order in the bfs seems to mess stuff up.
# 2h21 nvm lol
# 3 h 42 overall :)


from typing import List
def solve_day_21_part_1(codes):
    
    def get_shortest_sequence(pos1, pos2, keypad) -> List[str]:
        """
        returns the shortest sequence of arrows from pos1 to pos2
        
        I don't understand WHY this works nor do I care.
        I copied the transition from https://observablehq.com/@jwolondon/advent-of-code-2024-day-21
        PROUDLY.
        """        
        # keypads miss the to bottom left corner
        # arrow pad misses the top left corner
        
        vertical = (pos2[0] - pos1[0])
        horizontal = (pos2[1] - pos1[1])
        
        vertical_arrows = ['v'] * vertical if vertical > 0 else ['^'] * abs(vertical)
        horizontal_arrows = ['>'] * horizontal if horizontal > 0 else ['<'] * abs(horizontal)
        
        if horizontal >= 0 and  ((pos2[0], pos1[1]) != (3,0) and keypad or (pos2[0],pos1[1])!= (0,0) and not keypad) : # if we're on the last row and we want to move to the first column, vertical first for keypad
            arrows = vertical_arrows + horizontal_arrows
            return ''.join(arrows) + 'A'
        
        if ((pos1[0], pos2[1]) != (3,0) and keypad or (pos1[0],pos2[1])!= (0,0) and not keypad): # if we're on the first row and we want to move to the first column, vertical first for arrow pad
            arrows = horizontal_arrows + vertical_arrows
            return ''.join(arrows) + 'A'

        # General case
        arrows = vertical_arrows + horizontal_arrows
        return ''.join(arrows) + 'A'
    
    def  translate_to_position(sequence):
        pad = {}
        if set(sequence).intersection({'^','v','<','>'}):
            pad = {
                None : (0,0), '^' : (0,1), 'A' : (0,2),
                '<' : (1,0), 'v': (1,1), '>' : (1,2) 
            }
        else:
            pad = {
                '7' : (0,0), '8' : (0,1), '9' : (0,2),
                '4' : (1,0), '5' : (1,1), '6' : (1,2),
                '1' : (2,0), '2' : (2,1), '3' : (2,2),
                None : (3,0), '0'  : (3,1), 'A' : (3,2)
            }
        
        return pad[sequence[0]], pad[sequence[1]]
    
    MAX_STAGES = 3
    stage = 0
    current_codes = codes
    while stage < MAX_STAGES:
        new_codes = []
        for current in current_codes:
            current = 'A' + current
            new_code = ''
            for i in range(len(current) - 1):
                new_code += get_shortest_sequence(*translate_to_position(current[i:i+2]), stage == 0)
            new_codes.append(new_code)
        current_codes = list(new_codes)
        stage += 1
    
    total = 0
    for code, total_keypresses in zip(codes, current_codes):
        code = int(code.replace('A',''))
        #print(len(total_keypresses))
        total += code * len(total_keypresses) 
    
    return total

t_input = """029A
980A
179A
456A
379A"""
        
#print(solve_day_21_part_1(get_test_inputs(t_input)))
#print(solve_day_21_part_1(get_input()))


import numpy as np
def solve_day_21_part_2(codes):
    
    def get_shortest_sequence(pos1, pos2, keypad) -> List[str]:
        """
        returns the shortest sequence of arrows from pos1 to pos2
        
        I don't understand WHY this works nor do I care.
        I copied the transition from https://observablehq.com/@jwolondon/advent-of-code-2024-day-21
        PROUDLY.
        """        
        # keypads miss the to bottom left corner
        # arrow pad misses the top left corner
        
        vertical = (pos2[0] - pos1[0])
        horizontal = (pos2[1] - pos1[1])
        
        vertical_arrows = ['v'] * vertical if vertical > 0 else ['^'] * abs(vertical)
        horizontal_arrows = ['>'] * horizontal if horizontal > 0 else ['<'] * abs(horizontal)
        
        if horizontal >= 0 and  ((pos2[0], pos1[1]) != (3,0) and keypad or (pos2[0],pos1[1])!= (0,0) and not keypad) : # if we're on the last row and we want to move to the first column, vertical first for keypad
            arrows = vertical_arrows + horizontal_arrows
            return ''.join(arrows) + 'A'
        
        if ((pos1[0], pos2[1]) != (3,0) and keypad or (pos1[0],pos2[1])!= (0,0) and not keypad): # if we're on the first row and we want to move to the first column, vertical first for arrow pad
            arrows = horizontal_arrows + vertical_arrows
            return ''.join(arrows) + 'A'

        # General case
        arrows = vertical_arrows + horizontal_arrows
        return ''.join(arrows) + 'A'
    
   
    def  translate_to_position(sequence):
        pad = {}
        if set(sequence).intersection({'^','v','<','>'}):
            pad = {
                None : (0,0), '^' : (0,1), 'A' : (0,2),
                '<' : (1,0), 'v': (1,1), '>' : (1,2) 
            }
        else:
            pad = {
                '7' : (0,0), '8' : (0,1), '9' : (0,2),
                '4' : (1,0), '5' : (1,1), '6' : (1,2),
                '1' : (2,0), '2' : (2,1), '3' : (2,2),
                None : (3,0), '0'  : (3,1), 'A' : (3,2)
            }
        
        return pad[sequence[0]], pad[sequence[1]]
    
    def get_next_4_iters_shortest_sequence(sequence):
        current = sequence
        new_code = ''
        for _ in range(4):
            for i in range(len(current)-1):
                new_code += get_shortest_sequence(*translate_to_position(current[i:i+2]), False)
            current = new_code
        
        return new_code

    def calculate_steps(code):
        #ITERATIONS = 2
        MAX_STAGES = 9
        stage = 0
        current_codes = [code]
        code_lengths = []
        while stage < 1:
            new_codes = []
            for current in current_codes:
                current = 'A' + current
                new_code = ''
                for i in range(len(current) - 1):
                    new_code += get_shortest_sequence(*translate_to_position(current[i:i+2]), True)
                new_codes.append(new_code)
            current_codes = list(new_codes)
            print(len(current_codes[0]))
            stage += 1
        stage = 0     
        while stage < (MAX_STAGES-1)//4:
            new_codes = []
            for current in current_codes:
                current = 'A' + current
                new_code = ''
                for i in range(len(current) - 1):
                    new_code += get_next_4_iters_shortest_sequence(current[i:i+2])
                new_codes.append(new_code)
            current_codes = list(new_codes)
            print(len(new_codes[0]))
            stage += 1
        return 0 
    total = 0
    for code in codes:
        steps = calculate_steps(code)
        code = int(code.replace('A',''))
        total += code * steps 
    
    return total

#print(solve_day_21_part_2(get_test_inputs("029A")))

from collections import defaultdict
def solve_day_21_part_2(codes):
    
    def get_shortest_sequence(pos1, pos2, keypad = False) -> List[str]:
        """
        returns the shortest sequence of arrows from pos1 to pos2
        
        I don't understand WHY this works nor do I care.
        I copied the transition from https://observablehq.com/@jwolondon/advent-of-code-2024-day-21
        PROUDLY.
        """        
        # keypads miss the to bottom left corner
        # arrow pad misses the top left corner
        
        vertical = (pos2[0] - pos1[0])
        horizontal = (pos2[1] - pos1[1])
        
        vertical_arrows = ['v'] * vertical if vertical > 0 else ['^'] * abs(vertical)
        horizontal_arrows = ['>'] * horizontal if horizontal > 0 else ['<'] * abs(horizontal)
        
        if horizontal >= 0 and  ((pos2[0], pos1[1]) != (3,0) and keypad or (pos2[0],pos1[1])!= (0,0) and not keypad) : # if we're on the last row and we want to move to the first column, vertical first for keypad
            arrows = vertical_arrows + horizontal_arrows
            return ''.join(arrows) + 'A'
        
        if ((pos1[0], pos2[1]) != (3,0) and keypad or (pos1[0],pos2[1])!= (0,0) and not keypad): # if we're on the first row and we want to move to the first column, vertical first for arrow pad
            arrows = horizontal_arrows + vertical_arrows
            return ''.join(arrows) + 'A'

        # General case
        arrows = vertical_arrows + horizontal_arrows
        return ''.join(arrows) + 'A'
    
    def  translate_to_position(sequence):
        pad = {}
        if set(sequence).intersection({'^','v','<','>'}):
            pad = {
                None : (0,0), '^' : (0,1), 'A' : (0,2),
                '<' : (1,0), 'v': (1,1), '>' : (1,2) 
            }
        else:
            pad = {
                '7' : (0,0), '8' : (0,1), '9' : (0,2),
                '4' : (1,0), '5' : (1,1), '6' : (1,2),
                '1' : (2,0), '2' : (2,1), '3' : (2,2),
                None : (3,0), '0'  : (3,1), 'A' : (3,2)
            }
        
        return pad[sequence[0]], pad[sequence[1]]
    
    # Arrowpad to numpad
    new_codes = []
    for current in codes:
        current = 'A' + current
        new_code = ''
        for i in range(len(current) - 1):
            new_code += get_shortest_sequence(*translate_to_position(current[i:i+2]), True)
        new_codes.append(new_code)
    current_codes = list(new_codes)
    
    
    total = 0
    for code_no,current in enumerate(current_codes):
        sequences = defaultdict(int)
        current = 'A' + current
                
        for i in range(len(current) - 1):
            sequences[current[i:i+2]] += 1

        MAX_STAGES = 25
        
        for _ in range(MAX_STAGES):
            new_sequences = defaultdict(int)
            for k in sequences:
                new_seq = 'A' + get_shortest_sequence(*translate_to_position(k), False)
                for i in range(len(new_seq) - 1):
                    new_sequences[new_seq[i:i+2]] += sequences[k]
            sequences = new_sequences
            
        total += sum(sequences.values()) * int(codes[code_no].replace('A',''))
        
    
    return total

print(solve_day_21_part_2(get_input()))

# This took me an extra 7 or 8 hours to solve.
# I used the addvice from  https://observablehq.com/@jwolondon/advent-of-code-2024-day-21