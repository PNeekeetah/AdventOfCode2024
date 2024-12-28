import re
def get_inputs():
    input = []
    with open("inputs/input3", "r") as file:
        for line in file.readlines():
            input.append(line)
    
    return input

def solve_day_3(input):
    total = 0 
    for line in input:
        all_muls = re.findall(r"mul\([0-9]+,[0-9]+\)", line)
        for mul in all_muls:
            mul = mul.replace('mul(','')
            mul = mul.replace(')','')
            nums = mul.split(',')
            total += int(nums[0]) * int(nums[1])
        
    return total

def solve_day_3_part_2(input):
    total = 0 
    enabled = True
    for line in input:
        all_muls = re.findall(r"mul\([0-9]+,[0-9]+\)|don't|do", line)
        print(all_muls)
        for mul in all_muls:
            if mul == "do":
                enabled = True
                continue
            elif mul == "don't":
                enabled = False
                continue
            
            if enabled:
                mul = mul.replace('mul(','')
                mul = mul.replace(')','')
                nums = mul.split(',')
                total += int(nums[0]) * int(nums[1])
        
    return total

print(solve_day_3(get_inputs()))

print(solve_day_3_part_2(get_inputs()))



