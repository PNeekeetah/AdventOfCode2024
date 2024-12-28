from collections import Counter

test_input = """
3   4
4   3
2   5
1   3
3   9
3   3
"""

def get_inputs():
    list_1 = []
    list_2 = []
    with open("inputs/input1", "r") as file:
        for line in file.readlines():
            # Do any additional parsing in here
            numbers = line.split()
            list_1.append(int(numbers[0]))
            list_2.append(int(numbers[1]))
    
    return list_1, list_2

def get_test_input(string):
    list_1 = []
    list_2 = []
    lines = list(filter(lambda x: x != '', string.split("\n")))
    for line in lines:
        # Do any additional parsing in here
        numbers = line.split()
        list_1.append(int(numbers[0]))
        list_2.append(int(numbers[1]))
    
    return list_1, list_2

def solve_day_1(list_1, list_2):
    list_1.sort()
    list_2.sort()
    distance = 0
    for n1, n2 in zip(list_1, list_2):
        distance += abs(n1 - n2)
    
    return distance

def solve_day_1_part_2(list_1, list_2):
    freq = Counter(list_2)
    similarity = 0
    for number in list_1:
        similarity += freq.get(number, 0) * number
    
    return similarity

print(solve_day_1(*get_test_input(test_input)))

print(solve_day_1(*get_inputs()))

print("Part 2")

print(solve_day_1_part_2(*get_test_input(test_input)))

print(solve_day_1_part_2(*get_inputs()))
