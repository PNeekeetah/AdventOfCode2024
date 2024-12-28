test_input = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""

from collections import defaultdict
def get_test_inputs(input):
    connections = defaultdict(list)
    lines = input.split('\n')
    for line in lines:
        if line == '':
            continue
        line = line.split('-')
        connections[line[0]].append(line[1])
        connections[line[1]].append(line[0])

    return connections


def get_input():
    with open('inputs/input23', 'r') as file:
        return get_test_inputs(file.read())
    
from collections import deque
def solve_day_23_part_1(connections):
    
    three_vertex_graphs = set()
    for connection_key in connections:
        if connection_key[0] != 't':
            continue
        #seen_connections = {connection_key}
        queue = deque([([connection_key],2)])
        #seen_connections.add(connection_key)
        while queue:
            current_list, remaining = queue.popleft()
            
            if remaining == 0:
                if current_list[0] in connections[current_list[-1]]:
                    current_tuple = tuple(sorted(current_list))
                    three_vertex_graphs.add(current_tuple)
                continue
            
            for neighbour in connections[current_list[-1]]:
                #if neighbour not in seen_connections:
                new_list = current_list[:]
                new_list.append(neighbour)
                queue.append((new_list, remaining - 1))
                #seen_connections.add(neighbour)
            
    #print(three_vertex_graphs)

    return len(three_vertex_graphs)

#print(solve_day_23_part_1(get_input()))

# Took me 22 m 36 to solve this one.

# This is a ktuple finding problem :) 3 tuples are easy enough, it might be hard to find 4 tuples.
# Oh, I think there is a way. We already have all the 3 tuples. A 4 tuple is a 3 tuple + 1

def solve_day_23_part_2(connections):
    
    three_vertex_graphs = set()
    for connection_key in connections:
        #seen_connections = {connection_key}
        queue = deque([([connection_key],2)])
        #seen_connections.add(connection_key)
        while queue:
            current_list, remaining = queue.popleft()
            
            if remaining == 0:
                if current_list[0] in connections[current_list[-1]]:
                    current_tuple = tuple(sorted(current_list))
                    three_vertex_graphs.add(current_tuple)
                continue
            
            for neighbour in connections[current_list[-1]]:
                #if neighbour not in seen_connections:
                new_list = current_list[:]
                new_list.append(neighbour)
                queue.append((new_list, remaining - 1))
                #seen_connections.add(neighbour)
    
    tuples = three_vertex_graphs       
    
    all_connection_sets = {k : set(v) for k, v in connections.items()}
    
    while len(tuples) != 1:
        print(f"Current iteration has {len(tuples)} of lengt") # The algorithm finished running before I could decide on what I wanted to write here.
        new_tuples = set()
        
        for tup in tuples:
            set_from_tuple = set(tup)
            for connection_key, all_connections in all_connection_sets.items():
                if set_from_tuple.intersection(all_connections) == set_from_tuple:
                    sorted_tuples = tuple(sorted(list((*tup, connection_key))))
                    new_tuples.add(sorted_tuples)
        tuples = new_tuples
    
    return ','.join(list(tuples.pop()))

print(solve_day_23_part_2(get_input()))
## Took me 37 m 13 s to finish everything.