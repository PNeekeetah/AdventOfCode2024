from pprint import pprint as print
from heapq import heappush, heappop
from collections import deque
from utils import show_matrix, write_to_file_string
import asyncio

test_input = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

test_input_2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

def get_test_inputs(input):
    start = None
    end = None
    matrix = []
    lines = input.split('\n')
    for i, line in enumerate(lines):
        if line == '':
            continue
        matrix.append(list(line.replace('\n','')))
        if "S" in line:
            start = (i, line.index("S"))
        if "E" in line:
            end = (i, line.index("E"))

    return matrix, start, end


def get_input():
    with open('inputs/input16', 'r') as file:
        return get_test_inputs(file.read())

class MinHeap:
    def __init__(self):
        self.array = []

    def heappush(self, element):
        assert len(element) == 3
        assert isinstance(element[0],int)
        assert len(element[1]) == 2
        assert isinstance(element[2], str)
        heappush(self.array, element)
    
    def heappop(self):
        return heappop(self.array)

    def size(self):
        return len(self.array)

def arrow(orientation):
    m = {
        "E" : ">",
        "W" : "<",
        "N" : "^",
        "S" : "v",
    }
    return m[orientation]
    

def djikstra(matrix, start, end):

    def bound(point):
        assert len(point) == 2
        y_bound = 0 <= point[0] < len(matrix)
        x_bound = 0 <= point[1] < len(matrix[0])
        return x_bound and y_bound

    def get_candidates(point):
        assert len(point) == 2
        directions = [ ("E",(0,1)), ("W",(0,-1)), ("N",(-1,0)), ("S",(1,0))]
        for orientation, d in directions:
            new = (point[0] + d[0], point[1] + d[1])
            if bound(new) and matrix[new[0]][new[1]] in {'.', 'E'}:
                yield new, orientation
                
    # Find the best path
    orientation = "E"
    visited = {start : 0}
    lowest_distance = MinHeap()
    lowest_distance.heappush((0, start, orientation))

    matrix_copy = [line[:] for line in matrix]
    while lowest_distance.size():
        distance, point, orientation = lowest_distance.heappop()

        if matrix_copy[point[0]][point[1]] == "E":
            visited[point] = distance
            continue
            
        for cand, new_orientation in get_candidates(point):
            if cand not in visited:
                added_dist = 1 + int(orientation != new_orientation) * 1000
                lowest_distance.heappush((distance + added_dist, cand, new_orientation))
                visited[cand] = distance
        
        matrix_copy[point[0]][point[1]] = arrow(orientation)
    
    return visited[end], visited

def mark_on_matrix(matrix, states):
    c = [line[:] for line in matrix]
    for s in states:
        c[s[0]][s[1]] = 'O'
    write_to_file_string(c, 0, "outputs/backtrack_matrix")

def solve_part_2(matrix, start, end):
    total_dots = 0
    print(len(matrix))
    print(len(matrix[0]))
    
    for i in range(len(matrix)):
        for j in range(len(matrix[0]) - 1):
            total_dots += matrix[i][j] == '.'
    
    expected_iters = total_dots ** 3
    lowest_score, visited = djikstra(matrix, start, end)
    best_seats = set()
    state = []
    
    def get_new_position(pos, direction):
        return (pos[0] + direction[0], pos[1] + direction[1])
    iters = 0 
    def backtrack(position, orientation, score, state):
        nonlocal best_seats, iters, expected_iters, visited
        iters += 1
        print(f"{iters} out of {expected_iters}")
        #mark_on_matrix(matrix, state)
        directions = [ ("E",(0,1)), ("W",(0,-1)), ("N",(-1,0)), ("S",(1,0))]
        opposites = {"E": "W", "N":"S", "S":"N", "W":"E"}
        directions = list(filter(lambda x: x[0] != opposites[orientation], directions)) # no sense going back.

        if position == end and score == lowest_score:
            print("Hit a best path ! :>")
            best_seats = best_seats.union(set(state))
            return
        
        if score > visited[position] + 2000:
            return
        
        if score > lowest_score:
            return
        
        
        for o, d in directions:
            new_pos = get_new_position(position, d)
            if new_pos in state or matrix[new_pos[0]][new_pos[1]] == '#':
                continue
            added_score = 1 + int(orientation != o) * 1000
            state.append(new_pos)
            backtrack(new_pos, o, score + added_score, state)
            state.pop()
            
        
    state.append(start)
    backtrack(start, "E", 0, state)

    return len(best_seats)

#print(solve_part_2(*get_test_inputs(test_input_2)))

print(solve_part_2(*get_input()))

# Took me 4 hours 20 to come up with this.
# I will admit I used a hint from reddit for this one - I've seen somebody say they've implemented a backtrack
# I implemented a backtrack with some pruning after writing a dumb backtrack at first because it would have taken 
# ages for the algorithm to complete.
# The idea behind the pruning backtrack was that I already get a set of optimal distances with Djikstra, I might
# as well introduce a tolerance factor ( visited[node] + 1500 in this case) after which I terminate that backtrack branch.