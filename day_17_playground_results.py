def playground(reg_a, reg_b, reg_c, program):

    tape_head = 0
    output = []    
    
    def get_literal(operand):
        return operand
    
    def get_combo(operand):
        nonlocal reg_a, reg_b, reg_c
        if operand == 4:
            return reg_a
        elif operand == 5:
            return reg_b
        elif operand == 6:
            return reg_c
        elif operand == 7:
            raise Exception("Hello")
        
        return operand
    
    def adv(operand):
        nonlocal reg_a, tape_head
        numerator = reg_a
        denominator = 2 ** get_combo(operand)
        reg_a = numerator // denominator
        tape_head += 2
        
    def bxl(operand):
        nonlocal reg_b, tape_head
        reg_b = reg_b ^ get_literal(operand)
        tape_head += 2
        
    def bst(operand):
        nonlocal reg_b, tape_head
        reg_b = get_combo(operand) & 7
        tape_head += 2
        
    def jnz(operand):
        nonlocal reg_a, tape_head
        if reg_a == 0:
            tape_head += 2
            return
        
        tape_head = get_literal(operand)
        
    def bxc(operand):
        nonlocal reg_b, reg_c, tape_head
        reg_b = reg_b ^ reg_c
        tape_head += 2
        
    def out(operand):
        nonlocal output, tape_head
        value = get_combo(operand) & 7
        output.append(value)
        tape_head += 2
    
    def bdv(operand):
        nonlocal reg_a, reg_b, tape_head
        numerator = reg_a
        denominator = 2 ** get_combo(operand)
        reg_b = numerator // denominator
        tape_head += 2

    def cdv(operand):
        nonlocal reg_a, reg_c, tape_head
        numerator = reg_a
        denominator = 2 ** get_combo(operand)
        reg_c = numerator // denominator
        tape_head += 2
    
    opcodes = {
        0 : adv,
        1 : bxl,
        2 : bst,
        3 : jnz,
        4 : bxc,
        5 : out,
        6 : bdv,
        7 : cdv,
    }
        
    while tape_head < len(program):
        opcodes[program[tape_head]](program[tape_head+1])
    
    return output

PROGRAM = [2,4,1,1,7,5,4,6,0,3,1,4,5,5,3,0]
all_nums = [10794, 10797, 10799, 535080, 6826496, 73934848, 73935360, 610803712, 745021440, 749518848, 879239168, 5174198272, 5174231040, 5174263808, 5174362112, 9200730112, 9200762880, 9200795648, 9200893952, 9469165568, 9469198336, 9469231104, 9469329408, 9603383296, 9603416064, 9603448832, 9603547136, 9607872512, 9608003584, 43560468480, 77920206848, 78322860032, 78327316480, 662035234816, 662043623424, 5882729463808, 6159587082240, 49040473456640, 51239496712192, 53438519967744, 57836566478848, 62234612989952, 404714768302080, 405264524115968, 405281703985152, 413510861324288, 414060617138176, 414077797007360, 418458663649280, 418475843518464, 431103047368704, 431652803182592, 431669983051776, 432202558996480, 432423749812224, 434367222513664, 434401582252032, 434435941990400, 448695233413120, 449244989227008, 449262169096192, 451959408558080, 451993768296448, 452028128034816, 453643035738112, 453660215607296, 456351012618240, 456357455069184, 456391814807552, 456419732094976, 456426174545920, 456832048955392, 456838491406336, 483879605501952, 484429361315840, 484446541185024, 487143780646912, 487178140385280, 487212500123648, 488827407826944, 488844587696128, 491535384707072, 491541827158016, 491576186896384, 491604104183808, 491610546634752, 492016421044224, 492022863495168, 519063977590784, 519613733404672, 519630913273856, 524011779915776, 524028959784960, 554248349679616, 554798105493504, 554815285362688, 558096640376832, 558113820246016, 559196152004608, 559213331873792, 562494686887936, 562511866757120, 562522604175360, 562934921035776, 4706004256161792, 4706554011975680, 4706571191844864, 4772524709642240, 4772541889511424, 4775823244525568, 4775840424394752, 4775849014329344, 4776192611713024, 4776373000339456, 4776922756153344, 4776939936022528, 4780221291036672, 4780238470905856, 4987479232872448, 4988028988686336, 4988046168555520, 4990743408017408, 4990777767755776, 4990812127494144, 4992427035197440, 4992444215066624, 4995132864593920, 4995141454528512, 4995175814266880, 4995201584070656, 4995210174005248, 4995596721061888, 4995613900931072, 4995622490865664, 5057847977050112, 5058397732864000, 5058414912733184, 5061696267747328, 5061713447616512, 5062795779375104, 5062812959244288, 5066094314258432, 5066111494127616, 5066120084062208, 5066532400922624, 5335474663063552, 5335491842932736, 5338773197946880, 5338790377816064, 5338798967750656, 5339142565134336]
all_nums = [6826538, 6826541, 6826543, 73935400, 610806272, 745024000, 879241728, 1013459456, 5174208512, 5174209024, 9200740352, 9200740864, 9469175808, 9469176320, 9603393536, 9603394048, 11804354560, 11804355072, 43560476672, 77920215040, 78322868224, 78327365632, 112279953408, 593316282368, 593316315136, 593316347904, 593316446208, 662035759104, 662035791872, 662035824640, 662035922944, 5060082270208, 6159593897984, 7259105525760, 44642500345856, 44642508734464, 46841523601408, 46841531990016, 49040546856960, 49040555245568, 51239570112512, 51239578501120, 53438593368064, 53438601756672, 57836639879168, 57836648267776, 62234686390272, 62234694778880, 66632732901376, 66632741289984, 71030779412480, 71030787801088, 75428825923584, 75428834312192, 370097935876096, 378894028898304, 383292075409408, 405282307964928, 414078400987136, 418476447498240, 431670587031552, 432424521564160, 449262773075968, 453660819587072, 484447145164800, 488845191675904, 519631517253632, 524029563764736, 554815889342464, 558114424225792, 559213935853568, 562512470736896, 713145563742208, 713899498274816, 4706571728715776, 4772542426382336, 4775840961265664, 4776940472893440, 4780239007776768, 4988046705426432, 4992444751937536, 5058415449604096, 5061713984487424, 5062813496115200, 5066112030998528, 5335492379803648, 5338790914686976, 5898442333224960, 5901740868108288, 6461392286646272, 6464690821529600]
all_nums = [6826538, 6826541, 610806312, 745024040, 5174209024, 9200740864, 43560478720, 43560479232, 593316290560, 662035767296, 5060082270208, 5060082302976, 44642500870144, 46841524125696, 370097942167552, 370097950556160]
all_nums = [10794, 535080, 6825984, 229425152, 879230976, 5174198272, 661961834496, 662028943360, 26482768347136, 202404628791296]
all_nums = [202972175280682, 202972175280685, 202972175280687]
print(sorted(all_nums))
print(playground(all_nums[-1], 0, 0, PROGRAM))
print(PROGRAM)

def minimized_function(reg_a):
    reg_b = 0
    reg_c = 0
    output = []
    while reg_a:
        # bst 4
        reg_b = reg_a & 7
        # bxl 1
        reg_b = reg_b ^ 1
        # cdv 5
        reg_c = reg_a >> reg_b
        # bxc 6
        reg_b = reg_b ^ reg_c
        # adv 3
        reg_a = reg_a >> 3
        # bxl 4
        reg_b = reg_b ^ 4
        # out 5
        output.append(reg_b & 7)
        # jnz 0
    
    return output

#for j in range(12):
#    mult = 1
#    for i in range(1,100_00):
#        a = minimized_function(i*mult)
#        b = playground(i*mult,0,0, PROGRAM)
#        assert minimized_function(i*mult) == playground(i*mult, 0,0,PROGRAM), print(a,b,i)
#    mult = mult * 8