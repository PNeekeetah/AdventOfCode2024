from collections import deque
test_input = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""

def get_test_inputs(input):
    matrix = []

    lines = input.split('\n')
    for line in lines:
        if line == '':
            continue
        matrix.append([plant for plant in line])
    
    return matrix

def get_input():
    with open('inputs/input12', 'r') as file:
        return get_test_inputs(file.read())
    

print(get_test_inputs(test_input))

def solve_day_12_part_1(matrix):
    
    
    def bound(pos):
        assert len(pos) == 2
        bound_x = 0 <= pos[0] < len(matrix)
        bound_y = 0 <= pos[1] < len(matrix[0])
        return bound_x and bound_y
    
    def get_candidate(pos, letter):
        assert len(pos) == 2
        for d in [(0,1),(1,0),(-1,0),(0,-1)]:
            new = (pos[0] + d[0], pos[1] + d[1])
            if bound(new) and matrix[new[0]][new[1]] == letter:
                yield new
    
    def get_perimeter(pos, letter):
        perimeter = 0
        for d in [(0,1),(1,0),(-1,0),(0,-1)]:
            new = (pos[0] + d[0], pos[1] + d[1])
            if not bound(new) or bound(new) and matrix[new[0]][new[1]] != letter:
                perimeter += 1 
        
        return perimeter

    def get_plot(pos, letter):
        
        queue = deque([pos])
        perimeter = 0
        area = set()
        area.add(pos)
        while queue:
            
            current = queue.popleft()
            perimeter += get_perimeter(current, letter)
            
            for candidate in get_candidate(current, letter):
                if candidate not in area:
                    area.add(candidate)
                    queue.append(candidate)
        
        return area, perimeter
    
    seen = set()
    total_price = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            current = (i,j)
            if current in seen:
                continue
            
            area, perimeter = get_plot(current, matrix[current[0]][current[1]])
            seen = seen.union(area)
            total_price += len(area) * perimeter
    
    return total_price

def solve_day_12_part_2(matrix):
    
    
    def bound(pos):
        assert len(pos) == 2
        bound_x = 0 <= pos[0] < len(matrix)
        bound_y = 0 <= pos[1] < len(matrix[0])
        return bound_x and bound_y
    
    def get_candidate(pos, letter):
        assert len(pos) == 2
        for d in [(0,1),(1,0),(-1,0),(0,-1)]:
            new = (pos[0] + d[0], pos[1] + d[1])
            if bound(new) and matrix[new[0]][new[1]] == letter:
                yield new
    
    def get_corners(pos, letter):
        #https://www.reddit.com/r/adventofcode/comments/1hcdnk0/comment/m1nkmol/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
        # this helped
        
        directions = [(-1,0),(0,1),(1,0),(0,-1),(-1,0)] # up, right, down, left, up
        ext_corn_dir = [(1,0),(0,-1),(-1,0),(0,1),(1,0)] # down, left, up, right, down
        interior_diags = [(-1,1),(1,1),(1,-1),(-1,-1)] #topright, bottomright, bottomleft, topleft
        total_corners = 0
        for i in range(4):
            plot1 = (pos[0] + directions[i][0], pos[1] + directions[i][1])
            plot2 = (pos[0] + directions[i+1][0], pos[1] + directions[i+1][1])
            plot3 = (pos[0] + ext_corn_dir[i][0], pos[1] + ext_corn_dir[i][1])
            plot4 = (pos[0] + ext_corn_dir[i+1][0], pos[1] + ext_corn_dir[i+1][1])

            int_diag = (pos[0] + interior_diags[i][0], pos[1] + interior_diags[i][1])
            

            isplot1 = bound(plot1) and matrix[plot1[0]][plot1[1]] == letter
            isplot2 = bound(plot2) and matrix[plot2[0]][plot2[1]] == letter
            
            isnotplot_int = not bound(int_diag) or bound(int_diag) and matrix[int_diag[0]][int_diag[1]] != letter
            isnotplot3 =  not bound(plot3) or bound(plot3) and matrix[plot3[0]][plot3[1]] != letter
            isnotplot4 =  not bound(plot4) or bound(plot4) and matrix[plot4[0]][plot4[1]] != letter

            total_corners += int(isplot1 and isplot2 and isnotplot_int)
            total_corners += int(isnotplot3 and isnotplot4)
        
        return total_corners
            
    
    def get_plot(pos, letter):
        
        queue = deque([pos])
        sides = 0
        area = set()
        area.add(pos)
        while queue:
            current = queue.popleft()
            sides += get_corners(current,letter)
            for candidate in get_candidate(current, letter):
                if candidate not in area:
                    area.add(candidate)
                    queue.append(candidate)
        
        return area, sides
    
    seen = set()
    total_price = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            current = (i,j)
            if current in seen:
                continue
            
            area, sides = get_plot(current, matrix[current[0]][current[1]])
            seen = seen.union(area)
            total_price += len(area) * sides
    
    return total_price
            
            
    
print(solve_day_12_part_1(get_test_inputs(test_input)))
print(solve_day_12_part_1(get_input()))
# 23m 34s up until now

    
print(solve_day_12_part_2(get_test_inputs(test_input)))
print(solve_day_12_part_2(get_input()))
# 3 h 12 to solve this one. Brutal. Couldn't solve this one without a hint about corners.
