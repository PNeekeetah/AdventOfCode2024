test_input = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

def get_test_inputs(input):
    equations = []

    lines = input.split('\n')
    for line in lines:
        if line == '':
            continue
        line = line.replace('\n','')
        line = line.split(':')
        result = int(line[0])
        terms = [int(num) for num in line[1].split()]
        equations.append((terms, result))
    
    return equations

def get_input():
    with open('inputs/input7', 'r') as file:
        return get_test_inputs(file.read())

def solve_day_7_part_1(equations):
    total = 0
    
    def generate_symbols(numbers):
        total_symbols = len(numbers) - 1
        for i in range(2**total_symbols):
            yield f"{bin(i)[2:]}".rjust(total_symbols,'0')
    
    def calculate(numbers, symbols):
        
        total = numbers[0]
        for i in range(len(symbols)):
            if symbols[i] == '0':
                total += numbers[i+1]
            elif symbols[i] == '1':
                total *= numbers[i+1]
        
        return total
            

    for equation in equations:
        numbers, result = equation
        for symbols in generate_symbols(numbers):
            if calculate(numbers, symbols) == result:
                total += result
                break
    return total

def solve_day_7_part_2(equations):
    total = 0
    
    def ternary(num):
        string = ''
        while num != 0:
            string = str(num % 3) + string
            num //= 3
        
        return string

    def generate_symbols(numbers):
        total_symbols = len(numbers) - 1
        for i in range(3**total_symbols):
            yield f"{ternary(i)}".rjust(total_symbols,'0')
    
    def calculate(numbers, symbols, result):
        
        total = numbers[0]
        for i in range(len(symbols)):
            if symbols[i] == '0':
                total += numbers[i+1]
            elif symbols[i] == '1':
                total *= numbers[i+1]
            elif symbols[i] == '2':
                total = int(str(total) + str(numbers[i+1]))
            
            # Abrupt end. At this point, it's only growing
            if total > result:
                return 0
        
        return total
            
    runs = 0
    for equation in equations:
        runs += 1
        print(runs, len(equations))
        numbers, result = equation
        for symbols in generate_symbols(numbers):
            if calculate(numbers, symbols, result) == result:
                total += result
                break
    return total
        
    
print(solve_day_7_part_1(get_test_inputs(test_input)))
print(solve_day_7_part_1(get_input()))

print(solve_day_7_part_2(get_test_inputs(test_input)))
print(solve_day_7_part_2(get_input()))
