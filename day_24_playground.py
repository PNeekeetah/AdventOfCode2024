from collections import defaultdict

def AND(o1, o2):
        return o1 and o2

def XOR(o1, o2):
    return o1 ^ o2

def OR(o1, o2):
    return o1 or o2


class Day24Solution:
    
    def __init__(self, function=None):
        self.wires = {}
        self.gates = {}
        self.cache = {}
        self.function = function
        if function is None:
            self.function = Day24Solution.recursive

    
    def get_test_inputs(self, input):
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
                
                
        

        self.gates = logic_gates
        self.wires = wires


    def get_input(self):
        with open('inputs/input24', 'r') as file:
            return self.get_test_inputs(file.read())

    def recursive_print(self, name, op1, op2, operation, correct_gates  = None):
        if correct_gates is None:
            print(name, op1, op2, operation.__name__)
        
        these_gates = {name}
        res1 = None
        if op1 not in self.wires:
            these_gates.add(op1)
            res1 = self.recursive_print(op1,*self.gates[op1], correct_gates)
        else:
            res1 = self.wires[op1]
        
        if op2 not in self.wires:
            these_gates.add(op2)
            res2 = self.recursive_print(op2, *self.gates[op2], correct_gates)
        else:
            res2 = self.wires[op2]
        
        if correct_gates is not None:
            if these_gates - correct_gates != set():
                print(these_gates - correct_gates)
        
        
        return operation(res1, res2)

    def recursive_correct_gates(self, name, op1, op2, operation, correct_gates=None):
        if correct_gates is None:
            correct_gates = set()
        res1 = None
        correct_gates.add(name)
        
        if op1 not in self.wires:
            correct_gates.add(op1)
            res1, _ = self.recursive_correct_gates(op1,*self.gates[op1], correct_gates)
        else:
            correct_gates.add(op1)
            res1 = self.wires[op1]
        
        if op2 not in self.wires:
            correct_gates.add(op2)
            res2,_ = self.recursive_correct_gates(op2, *self.gates[op2],correct_gates)
        else:
            correct_gates.add(op2)
            res2 = self.wires[op2]
        
        
        return operation(res1, res2), correct_gates

        
    def recursive_no_cache(self, name, op1, op2, operation):
        res1 = None
        if op1 not in self.wires:
            res1 = self.recursive_no_cache(op1,*self.gates[op1])
        else:
            res1 = self.wires[op1]
        
        if op2 not in self.wires:
            res2 = self.recursive_no_cache(op2, *self.gates[op2])
        else:
            res2 = self.wires[op2]
        
        
        return operation(res1, res2)
    
    def set_function(self, function):
        self.function = function
        
    def recursive(self, name, op1, op2, operation):
            if name in self.cache:
                return self.cache[name]
            
            res1 = None
            if op1 not in self.wires:
                res1 = self.recursive(op1,*self.gates[op1])
            else:
                res1 = self.wires[op1]
            
            if op2 not in self.wires:
                res2 = self.recursive(op2, *self.gates[op2])
            else:
                res2 = self.wires[op2]
            
            if name not in self.cache:
                self.cache[name] = operation(res1, res2)
            
            return self.cache[name]
        
    def set_custom_input(self, x, y):
        # MSB on the left !
        assert self.wires != {}, "Wires must be set"
        assert len(x) == 45, "X must have 45 bits"
        assert len(y) == 45, "Y must have 45 bits"
        
        for w in self.wires:
            if 'x' in w:
                pos = int(w.replace('x',''))
                self.wires[w] = x[44-pos]
            if 'y' in w:
                pos = int(w.replace('y',''))
                self.wires[w] = y[44-pos]
                 
                

    def solve_day_24_part_1(self, interesting_outputs=[]):
        
        
        outputs = defaultdict(int)
        for logic_gate_name , logic_gate  in self.gates.items():
            
            if logic_gate_name[0] != 'z':
                continue
            if logic_gate_name in interesting_outputs:
                outputs[int(logic_gate_name.replace('z',''))] = self.recursive_print(logic_gate_name, *logic_gate)
            else:
                outputs[int(logic_gate_name.replace('z',''))] = self.function(self,logic_gate_name, *logic_gate)
        biggest_z = max(outputs.keys())
        
        output_result = list(reversed(['1' if outputs[key] else '0' for key in range(biggest_z+1)]))
        return output_result # int(''.join(output_result), 2)

    def debug_day_24_part_2(self, interesting_outputs=[]):        
        outputs = defaultdict(int)
        last_gates = None
        these_gates = None
        for logic_gate_name , logic_gate  in sorted(self.gates.items()):
            
            if logic_gate_name[0] != 'z':
                continue
            
            outputs[int(logic_gate_name.replace('z',''))], c_gates = self.recursive_correct_gates(logic_gate_name, *logic_gate, None)
            
            if these_gates is None:
                these_gates = c_gates
            elif these_gates:
                last_gates = these_gates
                these_gates = c_gates
            
            
            if logic_gate_name not in interesting_outputs:
                continue
            
            
            
            print(these_gates - last_gates)
            
            
                    
        
        
        biggest_z = max(outputs.keys())
        
        output_result = list(reversed(['1' if outputs[key] else '0' for key in range(biggest_z+1)]))
        return output_result # int(''.join(output_result), 2)
    
    def get_actual (self):
        
        x = sorted(list(filter(lambda x: 'x' in x, self.wires.keys())))
        num_x = ['1' if self.wires[i] else '0' for i in reversed(x)]
        num_x = int(''.join(num_x),2)
              
        y = sorted(list(filter(lambda x: 'y' in x, self.wires.keys())))
        num_y = ['1' if self.wires[i] else '0' for i in reversed(y)]
        num_y = int(''.join(num_y),2)
        
        num_z = num_x + num_y
        
        return bin(num_z)[2:]
    
    def get_wrong(self):
        z_correct = int(''.join(self.get_actual()),2)
        z_wrong = int(''.join(self.solve_day_24_part_1()),2)
        
        wrong_bits = z_wrong ^ z_correct
        
        wrong_positions = []
        for i, b in enumerate(reversed(bin(wrong_bits)[2:])):
            if b == '1':
                wrong_positions.append('z' + f'{i}'.rjust(2,'0'))
        
        return wrong_positions
        
        
                
        
        
s = Day24Solution(Day24Solution.recursive_no_cache)
s.get_input()


y = [False for _ in range(45)]
x = [False for _ in range(45)]

"""
for i in range(44,-1,-1):
    x = [False for _ in range(45)]
    x[i] = True
    s.set_custom_input(x,y) 
    res = s.debug_day_24_part_2(['z07','z12', 'z24', 'z39'])
    try:
        assert res[i+1] == '1'
    except Exception as e:
        print(f"Expected {i+1} ; found on pos {res.index('1')}")
        print(res)
"""

#res = s.debug_day_24_part_2(['z07','z12', 'z24', 'z39'])

s.get_actual()

wrong_outputs = []
last_wrong = 0
interesting_gates_0 = ['z38']
interesting_gates_1 = ['z06', 'z07', 'z08', 'z09', 'z10'] 
interesting_gates_2 = ['z12', 'z13', 'z14', 'z15', 'z16', 'z17', 'z18', 'z19', 'z20', 'z21', 'z22'] 
interesting_gates_3 = ['z38', 'z39', 'z40', 'z41', 'z42', 'z43', 'z44', 'z45']

for i in range(44,-1,-1):
    x = [False for _ in range(45)]
    y = [False for _ in range(45)]

    x[i] = True
    #y[i] = False

    s.set_custom_input(x,y)
    wrong_outputs.extend(s.get_wrong())
    
s.debug_day_24_part_2(wrong_outputs)
    #if last_wrong < len(wrong_outputs):
    #    print(i)
    #    last_wrong = len(wrong_outputs)

#correct_outputs = ['z05', 'z10', 'z22', 'z37', 'z04', 'z9', 'z21', 'z36']
#s.debug_day_24_part_2(wrong_outputs)
#s.debug_day_24_part_2(correct_outputs)



swap_gates = ['cpf', 'z07', 'dqp', 'y32', 'qtc', 'ssf', 'vtc', 'pmc', 'x14', 'gsr', 'krq', 'cdj', 'cwp', 'nqb', 'hgh', 'x21', 'y05', 'hct', 'y09', 'x33', 'csr', 'jbk', 'x15', 'x11', 'wjn', 'y24', 'fkp', 'y07', 'x19', 'fsn', 'x23', 'fnj', 'bsv', 'vcn', 'x16', 'x29', 'ddq', 'y11', 'brq', 'cnm', 'jns', 'cqq', 'x35', 'vrp', 'gkv', 'wpq', 'x07', 'hkm', 'nhw', 'sgf', 'vkf', 'x39', 'nkv', 'cmb', 'wjj', 'vdm', 'cqh', 'tgg', 'x34', 'hvf', 'bhd', 'qpf', 'bcg', 'z11', 'bps', 'fmm', 'kts', 'frf', 'kkp', 'jwg', 'x22', 'y00', 'tgw', 'y14', 'fdf', 'y30', 'jvk', 'wng', 'y08', 'y31', 'y25', 'rdr', 'vks', 'brp', 'mjh', 'cqr', 'x24', 'x37', 'jmc', 'qqr', 'pjh', 'vft', 'gqf', 'hfd', 'bff', 'x09', 'dbp', 'jvs', 'dpb', 'fhd', 'y10', 'x32', 'dfg', 'mbb', 'x02', 'mtd', 'fjs', 'z39', 'y39', 'kdb', 'y38', 'wnv', 'y16', 'mss', 'qsj', 'y02', 'x28', 'htq', 'x03', 'nhv', 'hnb', 'z24', 'fkh', 'jgm', 'trb', 'gtf', 'x25', 'y19', 'y35', 'vdp', 'mmp', 'fgw', 'kwn', 'z06', 'jjg', 'y28', 'wrn', 'y03', 'x36', 'y15', 'ntc', 'mtp', 'pww', 'dhg', 'y18', 'y21', 'y13', 'rsb', 'smm', 'pfm', 'nvf', 'pvc', 'mdk', 'tcs', 'z38', 'hbw', 'y33', 'gjg', 'rfw', 'stm', 'y22', 'ttj', 'x05', 'csn', 'hsv', 'pmt', 'pmw', 'pnh', 'qbn', 'mmj', 'y06', 'cjd', 'jpw', 'z12', 'nhb', 'x27', 'x30', 'y23', 'khd', 'cbg', 'y26', 'cgn', 'cbw', 'pkq', 'y29', 'y37', 'ssn', 'qhv', 'x18', 'scp', 'x08', 'x17', 'ckp', 'y04', 'rdw', 'pws', 'jpc', 'x31', 'x38', 'brk', 'y34', 'x13', 'dhd', 'grp', 'nbf', 'twj', 'gsj', 'x06', 'x10', 'ktj', 'y12', 'hpg', 'z23', 'wcb', 'qqq', 'x01', 'kpd', 'vpw', 'sbj', 'y20', 'x26', 'y01', 'y27', 'dds', 'vpt', 'qwk', 'x20', 'y17', 'tng', 'dpd', 'rjn', 'sjw', 'x12', 'cbq', 'x04', 'cfw', 'mqf', 'nfb', 'cfr', 'x00', 'y36', 'vms']
swap_gates = ['frf', 'krq', 'dpd', 'bhd', 'z06', 'cwp', 'brk', 'jvk', 'hvf', 'wjj', 'nbf', 'z38', 'z23', 'nvf', 'z11', 'dhg', 'vcn', 'dfg', 'dqp'] # stage 2 - these swaps cause 6 errors each
wires_copy = dict(s.wires)
gates_copy = dict(s.gates)

#current_wrong_outputs = 8
#for i in range(len(swap_gates)):
#   for j in range(i+1, len(swap_gates)):
#        wrong_outputs = []
#        s.wires = dict(wires_copy)
#        s.gates = dict(gates_copy)
#        
#        if swap_gates[i] in s.wires and swap_gates[j] in s.gates:
#            continue
#        if swap_gates[j] in s.wires and swap_gates[i] in s.gates:
#            continue
#        
#        if swap_gates[i] in s.gates:
#            aux = s.gates[swap_gates[i]]
#            aux2 = s.gates[swap_gates[j]]
#        elif swap_gates[i] in s.wires:
#            aux = s.wires[swap_gates[i]]
#            aux2 = s.wires[swap_gates[j]]
#            
#        if swap_gates[i] in s.wires and swap_gates[j] in s.wires:
#            s.wires[swap_gates[i]] = aux2
#            s.wires[swap_gates[j]] = aux
#        
#        if swap_gates[i] in s.gates and swap_gates[j] in s.gates:
#            s.gates[swap_gates[i]] = aux2
#            s.gates[swap_gates[j]] = aux
#        
#        for r in range(44,-1,-1):
#            x = [False for _ in range(45)]
#            x[r] = True
#            exception = None
#            try:
#                s.set_custom_input(x,y)
#                wrong_outputs.extend(s.get_wrong())
#            except Exception as e:
#                print(e)
#                exception = e
#                break
#
#        with open("outputs/logic_gates.txt", 'a+') as file:
#            #file.write(str((swap_gates[i], swap_gates[j], wrong_outputs, len(wrong_outputs), exception)) + '\n\n')
#            pass

"""
swapable_pairs = [
    ('dqp', 'dpd'),
    ('krq', 'z11'),
    ('cwp', 'dpd'),
    ('vcn', 'z23'),
    ('wjj', 'dpd'),
    ('hvf', 'z38'),
    ('bhd', 'z23'),
    ('z11', 'dpd'),
    ('frf', 'nvf'),
    ('jvk', 'dhg'),
    ('dfg', 'z38'),
    ('z06', 'dhg'),
    ('dhg', 'nvf'),
    ('z38', 'nbf'),
    ('brk', 'dpd'),
]

current_wrong_outputs = 6
pairs = []
for i in range(len(swapable_pairs)):

    for j in range(i+1, len(swapable_pairs)):
        s.wires = dict(wires_copy)
        s.gates = dict(gates_copy)
        g1, g2 = swapable_pairs[i]
        g3, g4 = swapable_pairs[j]
        
        if {g1,g2}.intersection({g3,g4}) != set():
            continue
        
        s.gates[g1], s.gates[g2] = s.gates[g2], s.gates[g1]
        s.gates[g3], s.gates[g4] = s.gates[g4], s.gates[g3]
            
        wrong_outputs = []
        
        for r in range(44,-1,-1):
            x = [False for _ in range(45)]
            x[r] = True
            exception = None
            try:
                s.set_custom_input(x,y)
                wrong_outputs.extend(s.get_wrong())
            except Exception as e:
                print(e)
                exception = e
                break
        
        if len(wrong_outputs) == 4:
            pairs.append(((g1,g2), (g3,g4)))                

#print(pairs)

pairs2 = []
for i in range(len(pairs)):

    for j in range(len(swapable_pairs)):
        s.wires = dict(wires_copy)
        s.gates = dict(gates_copy)
        (g1, g2), (g3,g4) = pairs[i]
        g5, g6 = swapable_pairs[j]
        
        if {g1,g2,g3,g4}.intersection({g5,g6}) != set():
            continue
        
        s.gates[g1], s.gates[g2] = s.gates[g2], s.gates[g1]
        s.gates[g3], s.gates[g4] = s.gates[g4], s.gates[g3]
        s.gates[g5], s.gates[g6] = s.gates[g6], s.gates[g5]
            
        wrong_outputs = []
        
        for r in range(44,-1,-1):
            x = [False for _ in range(45)]
            x[r] = True
            exception = None
            try:
                s.set_custom_input(x,y)
                wrong_outputs.extend(s.get_wrong())
            except Exception as e:
                print(e)
                exception = e
                break
        
        if len(wrong_outputs) == 2:
            pairs2.append(((g1,g2), (g3,g4), (g5,g6)))                

pairs3 = []
for i in range(len(pairs2)):

    for j in range(len(swapable_pairs)):
        s.wires = dict(wires_copy)
        s.gates = dict(gates_copy)
        (g1, g2), (g3,g4), (g5,g6) = pairs2[i]
        g7, g8 = swapable_pairs[j]
        
        if {g1,g2,g3,g4,g5,g6}.intersection({g7,g8}) != set():
            continue
        
        s.gates[g1], s.gates[g2] = s.gates[g2], s.gates[g1]
        s.gates[g3], s.gates[g4] = s.gates[g4], s.gates[g3]
        s.gates[g5], s.gates[g6] = s.gates[g6], s.gates[g5]
        s.gates[g7], s.gates[g8] = s.gates[g8], s.gates[g7]

            
        wrong_outputs = []
        
        for r in range(44,-1,-1):
            x = [False for _ in range(45)]
            x[r] = True
            exception = None
            try:
                s.set_custom_input(x,y)
                wrong_outputs.extend(s.get_wrong())
            except Exception as e:
                print(e)
                exception = e
                break
        
        if len(wrong_outputs) == 0 and exception is None:
            pairs3.append(((g1,g2), (g3,g4), (g5,g6), (g7,g8)))                

print(pairs3)
"""
unique_pairs = list({(('bhd', 'z23'), ('frf', 'nvf'), ('hvf', 'z38'), ('krq', 'z11')), (('brk', 'dpd'), ('frf', 'nvf'), ('hvf', 'z38'), ('vcn', 'z23')), (('brk', 'dpd'), ('dfg', 'z38'), ('dhg', 'jvk'), ('vcn', 'z23')), (('cwp', 'dpd'), ('dfg', 'z38'), ('dhg', 'nvf'), ('vcn', 'z23')), (('dhg', 'nvf'), ('dpd', 'z11'), ('nbf', 'z38'), ('vcn', 'z23')), (('bhd', 'z23'), ('dhg', 'z06'), ('hvf', 'z38'), ('krq', 'z11')), (('dpd', 'wjj'), ('frf', 'nvf'), ('hvf', 'z38'), ('vcn', 'z23')), (('cwp', 'dpd'), ('frf', 'nvf'), ('hvf', 'z38'), ('vcn', 'z23')), (('brk', 'dpd'), ('dfg', 'z38'), ('frf', 'nvf'), ('vcn', 'z23')), (('bhd', 'z23'), ('dhg', 'jvk'), ('dpd', 'wjj'), ('nbf', 'z38')), (('bhd', 'z23'), ('brk', 'dpd'), ('dhg', 'z06'), ('hvf', 'z38')), (('brk', 'dpd'), ('dhg', 'jvk'), ('hvf', 'z38'), ('vcn', 'z23')), (('bhd', 'z23'), ('dfg', 'z38'), ('dhg', 'nvf'), ('dpd', 'wjj')), (('dhg', 'nvf'), ('hvf', 'z38'), ('krq', 'z11'), ('vcn', 'z23')), (('bhd', 'z23'), ('brk', 'dpd'), ('dfg', 'z38'), ('frf', 'nvf')), (('cwp', 'dpd'), ('dfg', 'z38'), ('dhg', 'jvk'), ('vcn', 'z23')), (('bhd', 'z23'), ('brk', 'dpd'), ('dhg', 'z06'), ('nbf', 'z38')), (('bhd', 'z23'), ('dhg', 'z06'), ('dpd', 'dqp'), ('hvf', 'z38')), (('bhd', 'z23'), ('dpd', 'dqp'), ('frf', 'nvf'), ('hvf', 'z38')), (('bhd', 'z23'), ('dhg', 'nvf'), ('dpd', 'dqp'), ('nbf', 'z38')), (('cwp', 'dpd'), ('dhg', 'jvk'), ('hvf', 'z38'), ('vcn', 'z23')), (('bhd', 'z23'), ('brk', 'dpd'), ('dhg', 'jvk'), ('hvf', 'z38')), (('bhd', 'z23'), ('dhg', 'nvf'), ('dpd', 'z11'), ('hvf', 'z38')), (('bhd', 'z23'), ('dhg', 'z06'), ('dpd', 'dqp'), ('nbf', 'z38')), (('bhd', 'z23'), ('dpd', 'dqp'), ('frf', 'nvf'), ('nbf', 'z38')), (('bhd', 'z23'), ('dhg', 'z06'), ('dpd', 'z11'), ('hvf', 'z38')), (('dfg', 'z38'), ('dpd', 'wjj'), ('frf', 'nvf'), ('vcn', 'z23')), (('bhd', 'z23'), ('brk', 'dpd'), ('dhg', 'jvk'), ('nbf', 'z38')), (('bhd', 'z23'), ('dhg', 'nvf'), ('dpd', 'z11'), ('nbf', 'z38')), (('bhd', 'z23'), ('brk', 'dpd'), ('dfg', 'z38'), ('dhg', 'jvk')), (('brk', 'dpd'), ('dfg', 'z38'), ('dhg', 'nvf'), ('vcn', 'z23')), (('bhd', 'z23'), ('dhg', 'z06'), ('krq', 'z11'), ('nbf', 'z38')), (('dhg', 'z06'), ('dpd', 'dqp'), ('hvf', 'z38'), ('vcn', 'z23')), (('dhg', 'jvk'), ('dpd', 'dqp'), ('hvf', 'z38'), ('vcn', 'z23')), (('dhg', 'nvf'), ('krq', 'z11'), ('nbf', 'z38'), ('vcn', 'z23')), (('cwp', 'dpd'), ('dhg', 'z06'), ('nbf', 'z38'), ('vcn', 'z23')), (('dpd', 'z11'), ('frf', 'nvf'), ('hvf', 'z38'), ('vcn', 'z23')), (('bhd', 'z23'), ('brk', 'dpd'), ('frf', 'nvf'), ('nbf', 'z38')), (('bhd', 'z23'), ('cwp', 'dpd'), ('dfg', 'z38'), ('dhg', 'z06')), (('dfg', 'z38'), ('frf', 'nvf'), ('krq', 'z11'), ('vcn', 'z23')), (('dhg', 'z06'), ('dpd', 'wjj'), ('nbf', 'z38'), ('vcn', 'z23')), (('dhg', 'jvk'), ('krq', 'z11'), ('nbf', 'z38'), ('vcn', 'z23')), (('dhg', 'jvk'), ('dpd', 'wjj'), ('hvf', 'z38'), ('vcn', 'z23')), (('bhd', 'z23'), ('dfg', 'z38'), ('dhg', 'z06'), ('krq', 'z11')), (('bhd', 'z23'), ('dhg', 'nvf'), ('hvf', 'z38'), ('krq', 'z11')), (('bhd', 'z23'), ('brk', 'dpd'), ('dfg', 'z38'), ('dhg', 'nvf')), (('bhd', 'z23'), ('dhg', 'jvk'), ('dpd', 'wjj'), ('hvf', 'z38')), (('bhd', 'z23'), ('brk', 'dpd'), ('dhg', 'nvf'), ('hvf', 'z38')), (('dhg', 'jvk'), ('hvf', 'z38'), ('krq', 'z11'), ('vcn', 'z23')), (('bhd', 'z23'), ('cwp', 'dpd'), ('dfg', 'z38'), ('frf', 'nvf')), (('dfg', 'z38'), ('dhg', 'nvf'), ('dpd', 'dqp'), ('vcn', 'z23')), (('bhd', 'z23'), ('dfg', 'z38'), ('dhg', 'z06'), ('dpd', 'dqp')), (('bhd', 'z23'), ('frf', 'nvf'), ('krq', 'z11'), ('nbf', 'z38')), (('bhd', 'z23'), ('cwp', 'dpd'), ('dhg', 'z06'), ('nbf', 'z38')), (('bhd', 'z23'), ('brk', 'dpd'), ('dhg', 'nvf'), ('nbf', 'z38')), (('dfg', 'z38'), ('dhg', 'z06'), ('dpd', 'dqp'), ('vcn', 'z23')), (('dfg', 'z38'), ('dhg', 'jvk'), ('dpd', 'dqp'), ('vcn', 'z23')), (('frf', 'nvf'), ('krq', 'z11'), ('nbf', 'z38'), ('vcn', 'z23')), (('bhd', 'z23'), ('dfg', 'z38'), ('dhg', 'jvk'), ('krq', 'z11')), (('bhd', 'z23'), ('dhg', 'nvf'), ('dpd', 'dqp'), ('hvf', 'z38')), (('bhd', 'z23'), ('cwp', 'dpd'), ('dhg', 'jvk'), ('hvf', 'z38')), (('dfg', 'z38'), ('dhg', 'nvf'), ('dpd', 'wjj'), ('vcn', 'z23')), (('bhd', 'z23'), ('dfg', 'z38'), ('dhg', 'jvk'), ('dpd', 'dqp')), (('bhd', 'z23'), ('dfg', 'z38'), ('dpd', 'z11'), ('frf', 'nvf')), (('bhd', 'z23'), ('cwp', 'dpd'), ('dhg', 'jvk'), ('nbf', 'z38')), (('dfg', 'z38'), ('dhg', 'z06'), ('dpd', 'wjj'), ('vcn', 'z23')), (('dfg', 'z38'), ('dhg', 'jvk'), ('dpd', 'wjj'), ('vcn', 'z23')), (('dfg', 'z38'), ('dhg', 'z06'), ('krq', 'z11'), ('vcn', 'z23')), (('dfg', 'z38'), ('dhg', 'jvk'), ('krq', 'z11'), ('vcn', 'z23')), (('bhd', 'z23'), ('dhg', 'nvf'), ('dpd', 'wjj'), ('hvf', 'z38')), (('dfg', 'z38'), ('dpd', 'z11'), ('frf', 'nvf'), ('vcn', 'z23')), (('dhg', 'z06'), ('dpd', 'z11'), ('nbf', 'z38'), ('vcn', 'z23')), (('bhd', 'z23'), ('dhg', 'nvf'), ('dpd', 'wjj'), ('nbf', 'z38')), (('bhd', 'z23'), ('dhg', 'nvf'), ('krq', 'z11'), ('nbf', 'z38')), (('bhd', 'z23'), ('dpd', 'z11'), ('frf', 'nvf'), ('hvf', 'z38')), (('brk', 'dpd'), ('frf', 'nvf'), ('nbf', 'z38'), ('vcn', 'z23')), (('dhg', 'z06'), ('dpd', 'z11'), ('hvf', 'z38'), ('vcn', 'z23')), (('frf', 'nvf'), ('hvf', 'z38'), ('krq', 'z11'), ('vcn', 'z23')), (('bhd', 'z23'), ('brk', 'dpd'), ('frf', 'nvf'), ('hvf', 'z38')), (('cwp', 'dpd'), ('dhg', 'nvf'), ('nbf', 'z38'), ('vcn', 'z23')), (('cwp', 'dpd'), ('dhg', 'z06'), ('hvf', 'z38'), ('vcn', 'z23')), (('dpd', 'wjj'), ('frf', 'nvf'), ('nbf', 'z38'), ('vcn', 'z23')), (('bhd', 'z23'), ('dpd', 'z11'), ('frf', 'nvf'), ('nbf', 'z38')), (('dhg', 'jvk'), ('dpd', 'wjj'), ('nbf', 'z38'), ('vcn', 'z23')), (('bhd', 'z23'), ('dhg', 'jvk'), ('dpd', 'dqp'), ('nbf', 'z38')), (('bhd', 'z23'), ('dfg', 'z38'), ('dhg', 'nvf'), ('krq', 'z11')), (('bhd', 'z23'), ('cwp', 'dpd'), ('dfg', 'z38'), ('dhg', 'nvf')), (('brk', 'dpd'), ('dhg', 'z06'), ('nbf', 'z38'), ('vcn', 'z23')), (('bhd', 'z23'), ('dhg', 'jvk'), ('dpd', 'z11'), ('hvf', 'z38')), (('bhd', 'z23'), ('dpd', 'wjj'), ('frf', 'nvf'), ('nbf', 'z38')), (('dhg', 'nvf'), ('dpd', 'dqp'), ('nbf', 'z38'), ('vcn', 'z23')), (('bhd', 'z23'), ('dfg', 'z38'), ('dhg', 'nvf'), ('dpd', 'dqp')), (('bhd', 'z23'), ('dhg', 'jvk'), ('dpd', 'z11'), ('nbf', 'z38')), (('bhd', 'z23'), ('cwp', 'dpd'), ('dhg', 'z06'), ('hvf', 'z38')), (('bhd', 'z23'), ('cwp', 'dpd'), ('dhg', 'nvf'), ('nbf', 'z38')), (('dhg', 'nvf'), ('dpd', 'wjj'), ('nbf', 'z38'), ('vcn', 'z23')), (('bhd', 'z23'), ('dfg', 'z38'), ('dhg', 'z06'), ('dpd', 'z11')), (('dhg', 'jvk'), ('dpd', 'z11'), ('nbf', 'z38'), ('vcn', 'z23')), (('dfg', 'z38'), ('dhg', 'nvf'), ('krq', 'z11'), ('vcn', 'z23')), (('bhd', 'z23'), ('dhg', 'jvk'), ('hvf', 'z38'), ('krq', 'z11')), (('bhd', 'z23'), ('cwp', 'dpd'), ('dfg', 'z38'), ('dhg', 'jvk')), (('brk', 'dpd'), ('dfg', 'z38'), ('dhg', 'z06'), ('vcn', 'z23')), (('dpd', 'z11'), ('frf', 'nvf'), ('nbf', 'z38'), ('vcn', 'z23')), (('bhd', 'z23'), ('dhg', 'z06'), ('dpd', 'wjj'), ('hvf', 'z38')), (('dhg', 'nvf'), ('dpd', 'wjj'), ('hvf', 'z38'), ('vcn', 'z23')), (('dhg', 'jvk'), ('dpd', 'z11'), ('hvf', 'z38'), ('vcn', 'z23')), (('bhd', 'z23'), ('dhg', 'z06'), ('dpd', 'wjj'), ('nbf', 'z38')), (('bhd', 'z23'), ('dfg', 'z38'), ('dhg', 'jvk'), ('dpd', 'z11')), (('bhd', 'z23'), ('dfg', 'z38'), ('frf', 'nvf'), ('krq', 'z11')), (('dhg', 'jvk'), ('dpd', 'dqp'), ('nbf', 'z38'), ('vcn', 'z23')), (('bhd', 'z23'), ('cwp', 'dpd'), ('frf', 'nvf'), ('hvf', 'z38')), (('cwp', 'dpd'), ('dhg', 'nvf'), ('hvf', 'z38'), ('vcn', 'z23')), (('dhg', 'z06'), ('hvf', 'z38'), ('krq', 'z11'), ('vcn', 'z23')), (('bhd', 'z23'), ('cwp', 'dpd'), ('frf', 'nvf'), ('nbf', 'z38')), (('cwp', 'dpd'), ('frf', 'nvf'), ('nbf', 'z38'), ('vcn', 'z23')), (('dfg', 'z38'), ('dpd', 'dqp'), ('frf', 'nvf'), ('vcn', 'z23')), (('bhd', 'z23'), ('dhg', 'jvk'), ('dpd', 'dqp'), ('hvf', 'z38')), (('brk', 'dpd'), ('dhg', 'jvk'), ('nbf', 'z38'), ('vcn', 'z23')), (('dpd', 'dqp'), ('frf', 'nvf'), ('nbf', 'z38'), ('vcn', 'z23')), (('cwp', 'dpd'), ('dfg', 'z38'), ('dhg', 'z06'), ('vcn', 'z23')), (('bhd', 'z23'), ('brk', 'dpd'), ('dfg', 'z38'), ('dhg', 'z06')), (('brk', 'dpd'), ('dhg', 'nvf'), ('nbf', 'z38'), ('vcn', 'z23')), (('bhd', 'z23'), ('dpd', 'wjj'), ('frf', 'nvf'), ('hvf', 'z38')), (('dpd', 'dqp'), ('frf', 'nvf'), ('hvf', 'z38'), ('vcn', 'z23')), (('bhd', 'z23'), ('cwp', 'dpd'), ('dhg', 'nvf'), ('hvf', 'z38')), (('brk', 'dpd'), ('dhg', 'nvf'), ('hvf', 'z38'), ('vcn', 'z23')), (('dhg', 'nvf'), ('dpd', 'z11'), ('hvf', 'z38'), ('vcn', 'z23')), (('brk', 'dpd'), ('dhg', 'z06'), ('hvf', 'z38'), ('vcn', 'z23')), (('bhd', 'z23'), ('dhg', 'jvk'), ('krq', 'z11'), ('nbf', 'z38')), (('bhd', 'z23'), ('dfg', 'z38'), ('dpd', 'dqp'), ('frf', 'nvf')), (('bhd', 'z23'), ('dfg', 'z38'), ('dhg', 'z06'), ('dpd', 'wjj')), (('dhg', 'z06'), ('dpd', 'wjj'), ('hvf', 'z38'), ('vcn', 'z23')), (('dfg', 'z38'), ('dhg', 'nvf'), ('dpd', 'z11'), ('vcn', 'z23')), (('bhd', 'z23'), ('dfg', 'z38'), ('dhg', 'nvf'), ('dpd', 'z11')), (('dhg', 'nvf'), ('dpd', 'dqp'), ('hvf', 'z38'), ('vcn', 'z23')), (('cwp', 'dpd'), ('dhg', 'jvk'), ('nbf', 'z38'), ('vcn', 'z23')), (('dfg', 'z38'), ('dhg', 'jvk'), ('dpd', 'z11'), ('vcn', 'z23')), (('dhg', 'z06'), ('dpd', 'dqp'), ('nbf', 'z38'), ('vcn', 'z23')), (('bhd', 'z23'), ('dfg', 'z38'), ('dpd', 'wjj'), ('frf', 'nvf')), (('dhg', 'z06'), ('krq', 'z11'), ('nbf', 'z38'), ('vcn', 'z23')), (('bhd', 'z23'), ('dfg', 'z38'), ('dhg', 'jvk'), ('dpd', 'wjj')), (('cwp', 'dpd'), ('dfg', 'z38'), ('frf', 'nvf'), ('vcn', 'z23')), (('dfg', 'z38'), ('dhg', 'z06'), ('dpd', 'z11'), ('vcn', 'z23')), (('bhd', 'z23'), ('dhg', 'z06'), ('dpd', 'z11'), ('nbf', 'z38'))})
from random import choice
for i in range(len(unique_pairs)):

    s.wires = dict(wires_copy)
    s.gates = dict(gates_copy)
    (g1, g2), (g3,g4), (g5,g6), (g7,g8) = unique_pairs[i]

    s.gates[g1], s.gates[g2] = s.gates[g2], s.gates[g1]
    s.gates[g3], s.gates[g4] = s.gates[g4], s.gates[g3]
    s.gates[g5], s.gates[g6] = s.gates[g6], s.gates[g5]
    s.gates[g7], s.gates[g8] = s.gates[g8], s.gates[g7]

        
    wrong_outputs = []
    correct = True
    
    for r in range(20):
        x = [choice([True, False]) for _ in range(45)]
        y = [choice([True, False]) for _ in range(45)]

        s.set_custom_input(x,y)
        wrong_outputs.extend(s.get_wrong())
        if wrong_outputs:
            correct = False
    
    if correct:
        print(unique_pairs[i])
            
        
