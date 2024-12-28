import numpy as np
from collections import Counter
test_input = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
10 5 6 7 8
10 5 11 13
"""

def get_inputs():
    reports = []
    with open("inputs/input2", "r") as file:
        for line in file.readlines():
            # Do any additional parsing in here
            numbers = line.split()
            reports.append([int(num) for num in numbers])
    
    return reports

def get_test_input(string):
    reports = []
    lines = list(filter(lambda x: x != '', string.split("\n")))
    for line in lines:
        # Do any additional parsing in here
        numbers = line.split()
        reports.append([int(num) for num in numbers])

    return reports

def solve_day_2(reports):
    safe_reports = 0
    noticeable_reports = []
    for report in reports:
        mult = int(report[0] > report[1]) * -1 + int(report[0] < report[1]) * 1
        if mult == 0:
            continue
        
        total_nums = len(report)
        safe = True
        for i,num in enumerate(report):

            if i + 1 == total_nums:
                continue
            
            range1, range2 = num + mult * 1, num + mult * 3
            range1, range2 = tuple(sorted(list([range1, range2])))
            if report[i+1] not in set(range(range1, range2 + 1)):
                safe = False
                break
        
        safe_reports += int(safe)
        
    return safe_reports

def solve_day_2_part_2(reports):
    safe_reports = 0
    for report in reports:
        numbers = np.convolve(report, [1,-1], mode='valid')
        counter = Counter(numbers)
        increasing = 0
        for k in counter.keys():
            increasing += int(k >= 0) * counter[k] - int(k < 0) * counter[k]
        
        mult = int(increasing > 0) * 1 + int(increasing < 0) * -1
        
        safe_levels = set([mult*1, mult*2, mult*3])

        can_skip = True
        index = None
        safe = True
        for i in range(0, len(report) - 1):
            left = report[i]
            right = report[i+1]
            if right - left in safe_levels:
                continue
            elif right - left not in safe_levels and can_skip:
                can_skip = False
                index = [i, i+1]
                break
        copy = list(report)
        found = False
        attempts = 0

        while index and not found:
            rm = index.pop()
            report = list(copy)
            del report[rm]
        
            for i in range(0, len(report) - 1):
                left = report[i]
                right = report[i+1]
                if right - left in safe_levels:
                    continue
                else:
                    attempts += 1
                    safe = False or len(index) > 0 
                    break
            
            if attempts == 0:
                found = True
        
        safe_reports += int(safe)



    
    return safe_reports




print(solve_day_2(get_test_input(test_input)))

print(solve_day_2(get_inputs()))

print(solve_day_2_part_2(get_test_input(test_input)))

print(solve_day_2_part_2(get_inputs()))
