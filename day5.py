test_input = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

def get_test_inputs(input):
    before = {}
    after = {}
    books = []

    lines = input.split('\n')
    for line in lines:
        line = line.replace('\n','')
        if '|' in line:
            line = line.split('|')
            n1, n2 = int(line[0]),int(line[1])
            before[n2] = before.get(n2, set()) 
            before[n2].add(n1)
            after[n1] = after.get(n1, set())
            after[n1].add(n2)
        elif ',' in line:
            books.append([int(num) for num in line.split(',')])
    
    return before, after, books

def get_inputs():
    before = {}
    after = {}
    books = []
    with open("inputs/input5", "r") as file:
        for line in file.readlines():
            line = line.replace('\n','')
            if '|' in line:
                line = line.split('|')
                n1, n2 = int(line[0]),int(line[1])
                before[n2] = before.get(n2, set()) 
                before[n2].add(n1)
                after[n1] = after.get(n1, set())
                after[n1].add(n2)
            elif ',' in line:
                books.append([int(num) for num in line.split(',')])
    
    return before, after, books

def solve_5_part_1(before, after, books):
    total = 0

    for pages in books:
        correct = True
        for i in range(len(pages)):
            page = pages[i]
            before_pages = pages[0:i]
            after_pages = pages[i+1:]
            for p in before_pages:
                if page in before.get(p, set()):
                    correct = False
                    break
            for p in after_pages:
                if not correct:
                    break
                if page in after.get(p, set()):
                    correct = False
                    break
        if correct:
            middle = len(pages) // 2
            total += pages[middle]
    
    return total

def solve_5_part_2(before, after, books):
    total = 0

    incorrect_pages = []

    for pages in books:
        correct = True
        for i in range(len(pages)):
            page = pages[i]
            before_pages = pages[0:i]
            after_pages = pages[i+1:]
            for p in before_pages:
                if page in before.get(p, set()):
                    correct = False
                    break
            for p in after_pages:
                if not correct:
                    break
                if page in after.get(p, set()):
                    correct = False
                    break
        if not correct:
            incorrect_pages.append(pages)
    
    # the moment you find a page which is incorrect, swap them. This ensures the correct order.
    # Retry and see whether it's correct. Repeat until correct.
    for pages in incorrect_pages:
        correct = False
        while not correct:
            lock = True
            for i in range(len(pages)):
                page = pages[i]
                before_pages = pages[0:i]
                after_pages = pages[i+1:]
                for j,p in enumerate(before_pages):
                    if page in before.get(p, set()):
                        before_pages[j], page = page, before_pages[j]
                        pages = before_pages + [page] + after_pages
                        lock = False
                        break
                for j,p in enumerate(after_pages):
                    if page in after.get(p, set()):
                        after_pages[j], page = page, after_pages[j]
                        pages = before_pages + [page] + after_pages
                        lock = False
                        break
            correct = lock
        middle = len(pages) // 2
        total += pages[middle]
    return total
            

#print(solve_5_part_1(*get_test_inputs(test_input)))

#print(solve_5_part_1(*get_inputs()))

print(solve_5_part_2(*get_test_inputs(test_input)))

print(solve_5_part_2(*get_inputs()))
