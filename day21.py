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


solve_day_21_part_1(get_test_inputs("""029A
980A
179A
456A
379A"""),0)
#solve_day_21_part_1(get_input())

# 2 hours in so far and I realised that this won't work as it is.
# The reason why this doesn't work is because from A to < there are 2 possible paths: <v< and v<<. At level 1, this doesn't cause a disturbance
# but 2 levels in, it might. Just shifting around the arrows order in the bfs seems to mess stuff up.
# 2h21 nvm lol
# 3 h 42 overall :)
