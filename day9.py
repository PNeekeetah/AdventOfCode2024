test_input = """2333133121414131402"""

def get_test_inputs(input):
    numbers = []

    lines = input.split('\n')
    for line in lines:
        if line == '':
            continue
        numbers.extend(list(line))
    
    return numbers

def get_input():
    with open('inputs/input9', 'r') as file:
        return get_test_inputs(file.read())

def solve_day_9_part_1(numbers):
    id = 0
    blocks = []
    free_space = False

    for number in numbers:
        if free_space:
            blocks.extend(['.'] * int(number))
        else:
            blocks.extend([str(id)] * int(number))
            id += 1
        free_space = not free_space
    
    left = 0
    right = len(blocks) - 1
    
    def find_next_id(right):
        while blocks[right] == '.':
            right -= 1
        
        return right
    
    def find_next_free(left):
        while blocks[left] != '.':
            left += 1
        return left
    

    while left < right:
        left = find_next_free(left)
        right = find_next_id(right)
        if left < right:
            blocks[left], blocks[right] = blocks[right], blocks[left]        
    total = 0
    for i, number in enumerate(blocks):
        if number == '.':
            break
        total += i * int(number)
    
    return total


def solve_day_9_part_2(numbers):
    id = 0
    blocks = []
    free_space = False

    for number in numbers:
        if free_space:
            blocks.append(('.', int(number)))
        else:
            blocks.append((str(id), int(number)))
            id += 1
        free_space = not free_space
    
    left = 0
    right = len(blocks) - 1
    
    
    def find_next_id(right):
        while blocks[right][0] == '.':
            right -= 1
        
        return right
    
    def find_next_free(left):
        while blocks[left][0] != '.':
            left += 1
        return left
    
    right = len(blocks) - 1
    while right > 0:
        left = 0
        found = False
        while left < right:
            left = find_next_free(left)
            if left > right:
                break
            spaces_required = blocks[right][1]
            spaces_available = blocks[left][1]
            if spaces_available >= spaces_required:
                remaining_spaces = spaces_available - spaces_required
                blocks[left] = blocks[right]
                blocks[right] = ('.', spaces_required)
                found = True
                if remaining_spaces > 0:
                    blocks.insert(left + 1, ('.', remaining_spaces))
                    right += 1
                break
            else:
                left += 1
        if found:
            right = find_next_id(right)
        else:
            right = find_next_id(right - 1)

    string = []
    for block in blocks:
        string.extend([block[0]]*block[1])
    total = 0
    for i, chr in enumerate(string):
        if chr == '.':
            continue
        total += int(chr) * i

    return total


print(solve_day_9_part_1(get_test_inputs(test_input)))
print(solve_day_9_part_1(get_input()))
# This took 20:25 

print(solve_day_9_part_2(get_test_inputs(test_input)))
print(solve_day_9_part_2(get_input()))
# Overall, it took me 1h 8m to solve both parts.


#00992111777.44.333....5555.6666.....8888..
#00992111777.44.333....5555.6666.....8888..