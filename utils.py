
def write_to_file_string(matrix, iters ,file_path ):
    copy = [[sym for sym in line] for line in matrix]
    with open(file_path, 'a+') as file:
        file.write(f"After {iters}\n")
        for line in copy:
            file.write((''.join(line)) + '\n')
        file.write('\n')

def write_to_file(matrix, iters ,file_path ):
    copy = [[str(num) if num > 0 else '.' for num in line] for line in matrix]
    with open(file_path, 'a+') as file:
        file.write(f"After {iters}\n")
        for line in copy:
            file.write((''.join(line)) + '\n')
        file.write('\n')
        
def show_matrix(matrix, iters, clear=False):
    from pprint import pprint as print
    from os import system
    copy = [[c for c in line] for line in matrix]
    if clear:
        system('cls')
    print(f"After {iters}")
    for line in copy:
        print((''.join([str(c) for c in line])))
    print('\n')

from collections import deque
def bfs(matrix, start, end, obstacle):
    def bound(pos):
        assert len(pos) == 2
        bound_x = 0 <= pos[0] < len(matrix)
        bound_y = 0 <= pos[1] < len(matrix[0])
        return bound_x and bound_y

    def get_candidate(pos):
        for d in [(0,1), (1,0), (0,-1), (-1,0)]:
            new_pos = (pos[0] + d[0], pos[1] + d[1])
            if bound(new_pos) and matrix[new_pos[0]][new_pos[1]] != obstacle:
                yield new_pos
    
    queue = deque([(start,0)])
    seen  = {start}
    while queue:
        current, distance = queue.popleft()
        
        if current == end:
            return distance
        
        for cand in get_candidate(current):
            if cand not in seen:
                queue.append((cand, distance + 1))
                seen.add(cand)
    
    return -1

def bfs_with_path(matrix, start, end, obstacle):
    def bound(pos):
        assert len(pos) == 2
        bound_x = 0 <= pos[0] < len(matrix)
        bound_y = 0 <= pos[1] < len(matrix[0])
        return bound_x and bound_y

    def get_candidate(pos):
        for d in [(0,1), (1,0), (0,-1), (-1,0)]:
            new_pos = (pos[0] + d[0], pos[1] + d[1])
            if bound(new_pos) and matrix[new_pos[0]][new_pos[1]] != obstacle:
                yield new_pos
    
    queue = deque([(start,0)])
    seen  = {start : 0}
    while queue:
        current, distance = queue.popleft()
        
        if current == end:
            seen[current] = distance
            print(seen[current])
            break
        
        for cand in get_candidate(current):
            if cand not in seen:
                queue.append((cand, distance + 1))
                seen[cand] = distance + 1
        
    
    if end not in seen:
        return []
    
    queue = deque([end])
    new_seen = set()
    path = []
    while queue:
        
        current = queue.popleft()
        all_scores = []
        for cand in get_candidate(current):
            all_scores.append(seen.get(cand, 'inf'))
        best_score = min(all_scores)
        for cand in get_candidate(current):
            if seen.get(cand,'inf') == best_score and cand not in new_seen:
                queue.append(cand)
                new_seen.add(cand)
        
        path.append(current)
    
    return path, seen
    
        
        