test_input = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""

def get_test_inputs(input):
    keys = []
    locks = []

    current_key = []
    current_lock = []
    is_key = False
    is_lock = False
    lines = input.split('\n')
    for line in lines:
        if line == '':
            if is_key:
                keys.append(current_key)
            else:
                locks.append(current_lock)

            is_key = False
            is_lock = False
            current_key = []
            current_lock = []
            continue

        line = list(line)
        if not is_key and not is_lock:
            is_lock = all([slot == '#' for slot in line ])
            is_key = not is_lock
        if is_key:
            current_key.append(line)
        else:
            current_lock.append(line)

    
    return keys, locks

def get_input():
    with open('inputs/input25', 'r') as file:
        return get_test_inputs(file.read())


from pprint import pprint as print
def solve_day_25_part_1(keys, locks):

    key_tuple_reps = []
    lock_tuple_reps = []
    
    def get_tuple_reps(entities):
        tuple_reps = []
        for entity in entities:
            transposed_entity = list(zip(*entity))
            tuple_rep = tuple(line.count('#') - 1 for line in transposed_entity)
            tuple_reps.append(tuple_rep)
        return tuple_reps

    key_tuple_reps = get_tuple_reps(keys)
    lock_tuple_reps = get_tuple_reps(locks)
    
    def sum_tuples(tup1, tup2):
        tup3 = []
        for t1, t2 in zip(tup1, tup2):
            tup3.append(t1+t2)
        
        return tuple(tup3)
    max_lock_height = 5
    lock_key_pairs = []
    for lock in lock_tuple_reps:
        for key in key_tuple_reps:
            combo = sum_tuples(key, lock)
            if any([num > max_lock_height for num in combo]):
                continue
            lock_key_pairs.append(tuple([lock,key]))
    
    return len(set(lock_key_pairs))

print(solve_day_25_part_1(*get_test_inputs(test_input)))
print(solve_day_25_part_1(*get_input()))
# Took me 52 minutes because I cannot parse for the life of me

