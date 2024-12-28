
from collections import deque
from copy import deepcopy
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

def get_test_inputs(input):
    start = None
    end = None
    matrix = []
    lines = input.split('\n')
    for i, line in enumerate(lines):
        matrix.append(list(line.replace('\n','')))
        if "S" in line:
            start = (i, line.index("S"))
        if "E" in line:
            end = (i, line.index("E"))

    return matrix, start


def get_input():
    with open('inputs/input16', 'r') as file:
        return get_test_inputs(file.read())
    

from heapq import heappush, heappop
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

def solve_day_16_part_1(matrix, start):
    orientation = "E"
    lowest_distance = MinHeap()

    lowest_distance.heappush((0, start, orientation))
    visited = set()

    def bounded(point):
        assert len(point) == 2
        y_bound = 0 <= point[0] < len(matrix)
        x_bound = 0 <= point[1] < len(matrix[0])
        return x_bound and y_bound

    def get_candidates(point):
        assert len(point) == 2
        directions = [
            ("E",(0,1)),
            ("W",(0,-1)),
            ("N",(-1,0)),
            ("S",(1,0))
        ]
        for orientation, d in directions:
            new = (point[0] + d[0], point[1] + d[1])
            if bounded(new) and matrix[new[0]][new[1]] in {'.', 'E'}:
                yield new, orientation
    


    while lowest_distance.size():
        distance, point, orientation = lowest_distance.heappop()

        if matrix[point[0]][point[1]] == "E":
            return distance

        for cand, new_orientation in get_candidates(point):
            if cand not in visited:
                added_dist = 1 + int(orientation != new_orientation) * 1000
                lowest_distance.heappush((distance + added_dist, cand, new_orientation))
        
        visited.add(point)
        matrix[point[0]][point[1]] = arrow(orientation)

#print(solve_day_16_part_1(*get_test_inputs(test_input)))
#print(solve_day_16_part_1(*get_input()))

# Took me about 38 minutes to implement it at first and now it took me 9 more minutes to write the input
# functions (this is the first problem i've solved)

from pprint import pprint as print
def solve_day_16_part_2(matrix, start):
    orientation = "E"
    end = None


    def bounded(point):
        assert len(point) == 2
        y_bound = 0 <= point[0] < len(matrix)
        x_bound = 0 <= point[1] < len(matrix[0])
        return x_bound and y_bound

    def get_candidates(point):
        assert len(point) == 2
        directions = [
            ("E",(0,1)),
            ("W",(0,-1)),
            ("N",(-1,0)),
            ("S",(1,0))
        ]
        for orientation, d in directions:
            new = (point[0] + d[0], point[1] + d[1])
            if bounded(new) and matrix[new[0]][new[1]] in {'.', 'E'}:
                yield new, orientation
    

    visited = {}
    orientations = {}
    
    # Step 0: part 1 code
    lowest_distance = MinHeap()
    lowest_distance.heappush((0, start, orientation))
    matrix_copy = [line[:] for line in matrix]
    while lowest_distance.size():
        distance, point, orientation = lowest_distance.heappop()

        if matrix_copy[point[0]][point[1]] == "E":
            visited[point] = distance
            matrix_copy[point[0]][point[1]] = arrow(orientation)
            end = point
            break

        for cand, new_orientation in get_candidates(point):
            if cand not in visited:
                added_dist = 1 + int(orientation != new_orientation) * 1000
                lowest_distance.heappush((distance + added_dist, cand, new_orientation))
        
        visited[point] = distance
        orientations[point] = orientation
        matrix_copy[point[0]][point[1]] = arrow(orientation)
    
    def get_best_candidates(point, visited):
        assert len(point) == 2
        directions = [
            ("E",(0,1)),
            ("W",(0,-1)),
            ("N",(-1,0)),
            ("S",(1,0))
        ]
        distances = []
        for _, d in directions:
            new = (point[0] + d[0], point[1] + d[1])
            if new in visited:
                distances.append(visited[new])
        
        best_distance = min(distances)
        for _, d in directions:
            new = (point[0] + d[0], point[1] + d[1])
            if new in visited and visited[new] == best_distance:
                yield new
    
    best_seats = {end}
    queue = deque([end])

    # Step 1 : get the best path
    while queue:
        current = queue.popleft()
        if current == start:
            best_seats.add(start)
            matrix[current[0]][current[1]] = 'O'
            break
        for candidate in get_best_candidates(current, visited):
            if candidate not in best_seats:
                best_seats.add(candidate)
                queue.append(candidate)
        matrix[current[0]][current[1]] = 'O'
    
    keys = list(orientations.keys())
    for k in keys:
        if k not in best_seats:
            del orientations[k]
        
    
    # Step 2 : find other best paths
    best_seats_queue = deque(list(best_seats))
    while best_seats_queue:
        best_seat = best_seats_queue.popleft()
        
        new_visited = {}
        lowest_distance = MinHeap()
        lowest_distance.heappush((visited[best_seat], best_seat, orientations[best_seat]))
        matrix_copy = [line[:] for line in matrix]
        
        end = None
        while lowest_distance.size():
            distance, point, orientation = lowest_distance.heappop()

            if point in best_seats and point != best_seat and distance == visited[best_seat]:
                end = point
                break

            for cand, new_orientation in get_candidates(point):
                if cand not in new_visited:
                    added_dist = 1 + int(orientation != new_orientation) * 1000
                    lowest_distance.heappush((distance + added_dist, cand, new_orientation))
            
            orientations[point] = orientation
            new_visited[point] = distance
            matrix_copy[point[0]][point[1]] = arrow(orientation)
            
        
        if end is None:
            continue
        
        best_seats = {end}
        queue = deque([end])
        
        while queue:
            current = queue.popleft()
            if current == best_seat:
                best_seats.add(start)
                matrix[current[0]][current[1]] = 'O'
                break
            for candidate in get_best_candidates(current, visited):
                if candidate not in best_seats:
                    best_seats.add(candidate)
                    queue.append(candidate)
            matrix[current[0]][current[1]] = 'O'
        
        keys = list(orientations.keys())
        for k in keys:
            if k not in best_seats:
                del orientations[k]
        for line in matrix:
            print(''.join(line))
    

    return len(best_seats)
        

print(solve_day_16_part_2(*get_test_inputs(test_input)))
#print(solve_day_16_part_2(*get_input()))