from collections import deque
test_input = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""

def get_test_inputs(input):
    start = None
    end = None
    matrix = []
    lines = input.split('\n')
    for i, line in enumerate(lines):
        if line == '':
            continue
        line = list(line.replace('\n', ''))
        if "S" in line:
            start = (i, line.index("S"))
            line[start[1]] = '.'
        if "E" in line:
            end = (i, line.index("E"))
            line[end[1]] = '.'
        
        matrix.append(line)

    return matrix, start, end


def get_input():
    with open('inputs/input20', 'r') as file:
        return get_test_inputs(file.read())

from utils import bfs, bfs_with_path, show_matrix
def solve_day_20_part_1(matrix, start, end):
    
    initial_time = bfs(matrix,start,end, obstacle='#')
    
    seen_obstacles = set()
    for i in range(1, len(matrix)-1):
        for j in range(1, len(matrix[0])-1):
            if matrix[i][j] == '#':
                seen_obstacles.add((i,j))
    
    
    saved = {}
    total_obstacles = len(seen_obstacles)
    percentage = total_obstacles // 20 # 5%
    for i, obstacle in enumerate(seen_obstacles):
        if i%percentage == 0:
            print(f"Finished {i} of {total_obstacles}")
        
        matrix[obstacle[0]][obstacle[1]] = '.'
        
        new_time = bfs(matrix,start,end, obstacle='#')
        
        saved[initial_time - new_time] = saved.get(initial_time - new_time,0) + 1

        matrix[obstacle[0]][obstacle[1]] = '#'
    
    print(saved)
    cheats_that_save_100 = 0
    for k in saved:
        if k < 100:
            continue
        cheats_that_save_100 += saved[k]
        
    return cheats_that_save_100

from pprint import pprint as print
#print(solve_day_20_part_1(*get_input()))
# 53:35 with a stupid approach (but it works hey !)

def bfs(matrix, start, obstacles, max_moves, visited):
    def bound(pos):
        assert len(pos) == 2
        bound_x = 0 <= pos[0] < len(matrix)
        bound_y = 0 <= pos[1] < len(matrix[0])
        return bound_x and bound_y

    def get_candidate(pos, obstacles):
        for d in [(0,1), (1,0), (0,-1), (-1,0)]:
            new_pos = (pos[0] + d[0], pos[1] + d[1])
            if bound(new_pos) and matrix[new_pos[0]][new_pos[1]] not in obstacles:
                yield new_pos

    cheats = {}
        
    queue = deque([(start, 0)])
    
    
    seen  = {start}
    while queue:
        current, moves = queue.popleft()
        
        if moves > max_moves:
            continue
        
        for cand in get_candidate(current, {}):
            if cand not in seen:
                queue.append((cand, moves + 1))
                seen.add(cand)
        
        for cand in get_candidate(current, {'#','V','O'}):
            if cand in visited:
                if moves + 1 > max_moves:
                    continue
                saved = visited[cand] - visited[start] - moves - 1
                if saved <= 0:
                    continue
                if start == cand:
                    continue
                if (start,cand) in cheats:
                    continue
                #matrix[cand[0]][cand[1]] = 'V'
                cheats[(start,cand)] = saved
        #matrix[current[0]][current[1]] = 'O'
        #show_matrix(matrix, 0)
                    
    return cheats


def solve_day_20_part_2(matrix, start, end):
    
    best_path, distances_to_all = bfs_with_path(matrix,start,end, obstacle='#')
    best_path = list(reversed(best_path))
    total = 0
    percentage = len(best_path) // 20
    for i,starting_point in enumerate(best_path):
        if i % percentage == 0:
            print(f"Ran {i} out of {len(best_path)}")
        cheats = bfs(matrix, starting_point, {'.','V','O'}, 20, dict(distances_to_all))
        for val in cheats.values():
            if val >= 100:
                total += 1
   
    return total

solve_day_20_part_2(*get_test_inputs(test_input))
print(solve_day_20_part_2(*get_input()))
# Took me 3 hours 28 overall because I messed up the search condition for my algorithm.