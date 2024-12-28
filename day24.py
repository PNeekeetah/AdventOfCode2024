test_input = """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02"""

test_input2 = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""

def AND(o1, o2):
    return o1 and o2

def XOR(o1, o2):
    return o1 ^ o2

def OR(o1, o2):
    return o1 or o2

from collections import defaultdict
def get_test_inputs(input):
    logic_gates = defaultdict(list)
    wires = defaultdict(bool)
    lines = input.split('\n')
    for line in lines:
        if line == '':
            continue
        if ":" in line:
            line = line.split(': ')
            wires[line[0]] = bool(int(line[1]))
        elif "->" in line:
            line = line.split(' -> ')
            operation = None
            operands = None
            if " XOR " in line[0]:
                operation = XOR
                operands = line[0].split(' XOR ')
            elif " AND " in line[0]:
                operation = AND
                operands = line[0].split(' AND ')
            elif " OR " in line[0]:
                operation = OR
                operands = line[0].split(' OR ')
            logic_gates[line[1]] = [*operands, operation]
            
            
    

    return wires, logic_gates


def get_input():
    with open('inputs/input24', 'r') as file:
        return get_test_inputs(file.read())
    
#print(get_test_inputs(test_input))


def solve_day_24_part_1(wires, logic_gates):
    
    results = {}
        
    def recursive(name, op1, op2, operation):
        nonlocal results
        if name in results:
            return results[name]
        res1 = None
        if op1 not in wires:
            res1 = recursive(op1,*logic_gates[op1])
        else:
            res1 = wires[op1]
        
        if op2 not in wires:
            res2 = recursive(op2, *logic_gates[op2])
        else:
            res2 = wires[op2]
        
        if name not in results:
            results[name] = operation(res1, res2)
        
        return results[name]
    
    
    outputs = defaultdict(int)
    for logic_gate_name , logic_gate  in logic_gates.items():
        
        if logic_gate_name[0] != 'z':
            continue
        
        outputs[int(logic_gate_name.replace('z',''))] = recursive(logic_gate_name, *logic_gate)
    
    biggest_z = max(outputs.keys())
    
    output_result = list(reversed(['1' if outputs[key] else '0' for key in range(biggest_z+1)]))

    return int(''.join(output_result), 2)

#print(solve_day_24_part_1(*get_test_inputs(test_input)))

#print(solve_day_24_part_1(*get_test_inputs(test_input2)))

#print(solve_day_24_part_1(*get_input()))

# Took me 32 m 36 to solve this one. 


def solve_day_24_part_2(wires, logic_gates):
    
    results = {}
    correct_gates = set()

    two_to_the_64 =2**64
    number_x = two_to_the_64
    number_y = two_to_the_64
    for wire in wires:
        if 'x' in wire:
            position = int(wire.replace('x',''))
            number_x ^= 2**position
        else:
            position = int(wire.replace('y',''))
            number_y ^= 2**position
    number_x ^= two_to_the_64
    number_y ^= two_to_the_64
    number_z = number_x + number_y
        
        
    def recursive(name, op1, op2, operation, force_recalc = False, depth=0):
        nonlocal correct_gates
    
        
        if force_recalc and name not in correct_gates:
            
            print(set((name, op1, op2)) - correct_gates, depth)
        
        if name in results and not force_recalc:
            return results[name]
    
        res1 = None
        if op1 not in wires or op1 in logic_gates and force_recalc:
            res1 = recursive(*(op1,*logic_gates[op1], force_recalc, depth + 1))
        elif op1 in wires:
            res1 = wires[op1]
        
        if op2 not in wires or op2 in logic_gates and force_recalc:
            res2 = recursive(*(op2, *logic_gates[op2], force_recalc, depth + 1))
        elif op2 in wires:
            res2 = wires[op2]
        
        if name not in results:
            results[name] = operation(res1, res2)
        
        return results[name]
    
    def recursive_correct_ones(name, op1, op2, function, correct_ones = set()):
        if correct_ones is None:
            correct_ones = set()
        
        print(f'{name} = {op1} {function.__name__} {op2}')
        
        correct_ones.add(name)
        correct_ones.add(op1)
        correct_ones.add(op2)
        
        if op1 not in wires :
            op1p, op2p, _ = logic_gates[op1]
            recursive_correct_ones(op1, op1p, op2p, _, correct_ones)   

        if op2 not in wires:
            op1p, op2p, _ = logic_gates[op2]
            recursive_correct_ones(op2, op1p, op2p, _, correct_ones)   
        
        return correct_ones
    
    
    
    outputs = defaultdict(int)
    for logic_gate_name , logic_gate  in logic_gates.items():
        
        if logic_gate_name[0] != 'z':
            continue
        
        outputs[int(logic_gate_name.replace('z',''))] = recursive(logic_gate_name, *logic_gate)
    
    biggest_z = max(outputs.keys())
    
    output_result = list(reversed(['1' if outputs[key] else '0' for key in range(biggest_z+1)]))

    actual = int(''.join(output_result), 2)
    
    for i, res in enumerate(list(reversed(bin(actual ^ number_z).replace('0b', '')))):
        if res == '1':
            continue
        gate_name = 'z' + f'{i}'.rjust(2,'0')
        op1, op2, _ = logic_gates[gate_name]
        correct_gates = correct_gates.union(recursive_correct_ones(gate_name, op1, op2,_))
        
    for i, res in enumerate(list(reversed(bin(actual ^ number_z).replace('0b', '')))):
        if res == '0':
            continue
        gate_name = 'z' + f'{i}'.rjust(2,'0')
        op1, op2, operation = logic_gates[gate_name]
        recursive(gate_name, op1, op2, operation, force_recalc=True)
        
             
    
    #print(bin(actual ^ number_z))

solve_day_24_part_2(*get_input())

#    {'mrr', 'gmb', 'mvd', 'nvf', 'prv', 'jwh', 'mjf', 'jvk', 'sqt'}
# 9 sets are wrong :)

# {'mrr', 'gmb', 'mvd', 'prv', 'jwh', 'mjf', 'sqt'} # culprit here? 

# sqt ? 

# y00 XOR x00

"""

z00 = y00 XOR x00

z01 = hbw XOR fhd
hbw = x01 XOR y01
fhd = x00 AND y00

z02 = ddq XOR csn

ddq = y02 XOR x02
csn = jjg OR kkp 

kkp = y01 AND x01
jjg = fhd AND hbw

fhd = x00 AND y00
hbw = x01 XOR y01

"""

# 2 hours 19 m and counting. God damnit :)