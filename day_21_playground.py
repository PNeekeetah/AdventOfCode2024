def get_shortest_sequence(pos1, pos2, keypad = False):
        
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

opposites = {
    'v' : '^',
    '^' : 'v',
    '>' : '<',
    '<' : '>'
}
from collections import defaultdict
graph = defaultdict(list)
for c1 in ['A', 'v', '^', '>', '<']:
    for c2 in ['A', 'v', '^', '>', '<']:
        if opposites.get(c1) == c2:
            continue
        graph[c1+c2].append(get_shortest_sequence(*translate_to_position(c1+c2)))
        
        
print(graph)
