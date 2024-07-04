import sys
dict_inst = {"00000": "add", "00001": "sub", "00010": "movI", "00011": "movR", "00100": "ld", 
            "00101": "st", "00110": "mul", "00111": "div", "01000": "rs", "01001": "ls", 
            "01010": "xor", "01011": "or", "01100": "and", "01101": "not", "01110": "cmp", 
            "01111": "jmp", "11100": "jlt", "11101": "jgt", "11111": "je", "11010": "hlt",
            "10000": "addf", "10001": "subf", "10010": "movf","10100": "incf","10101": "decf",
            "10110": "rrl","10111": "rrr","11000": "swap"}

dict_reg = {"000": "R0", "001": "R1", "010": "R2", "011": "R3", "100": "R4", "101": 
            "R5", "110": "R6", "111": "FLAGS"}

list_reg = ["R0", "R1", "R2", "R3", "R4", "R5", "R6", "FLAGS"]
reg_values = {"R0": '0000000000000000', "R1": '0000000000000000', "R2": '0000000000000000', 
            "R3": '0000000000000000', "R4": '0000000000000000', "R5": '0000000000000000', 
            "R6": '0000000000000000', "FLAGS": "0000000000000000"}
            # this is just for testing, initially set all to zeroes
            # Register value is 16 bits (hence range [0,65535] (0 to 2^16-1))

list_typeA = ["add", "sub", "mul", "xor", "or", "and"]
list_typeAf = ["addf", "subf"]
list_typeB = ["movI", "rs", "ls", "incf", "decf", "rrl", "rrr"]
list_typeC = ["movR", "div", "not", "cmp", "swap"]
list_typeD = ["ld", "st"]
list_typeE = ["jmp", "jlt", "jgt", "je"]

input_file_list = []
memory_dict = {}
list_opcode = []

def dec_bin(n):
    return bin(n).replace("0b", "")

def dec_bin7(dec):
    dec = int(dec)
    binary = ''
    while dec != 0:
        if dec % 2 == 0:
            binary += '0'
        if dec % 2 == 1:
            binary += '1'
        dec = dec // 2

    unused = 7 - len(binary)
    binary = binary[-1::-1]
    binary = '0' * unused + binary
    return binary

def bin_dec(binary):
    l = len(binary) - 1
    val = 0
    for i in binary:
        val += (int(i)) * (2 ** l)
        l -= 1
    return val

def dec_binf(dec):
    dec = int(dec)
    binary = ''
    while dec != 0:
        if dec % 2 == 0:
            binary += '0'
        if dec % 2 == 1:
            binary += '1'
        dec = dec // 2
    binary = binary[-1::-1]
    return binary

def fbin_dec(binary):
    val = 0
    for i in range(len(binary)):
        val += (int(binary[i])) * (2 ** -(i+1))
    return val

def floattobin(num): # num is a float number in decimal system
    intpart = int(num//1)
    fracpart = float(num%1)
    intbinary = dec_binf(intpart)
    fracbinary = ''
    while fracpart > 0:
        fracpart *= 2
        if fracpart >= 1:
            fracbinary+="1"
            fracpart-=1
        else:
            fracbinary+="0"
    binary = intbinary + "." + fracbinary
    return binary

def bintofloat(bin): # bin is a binary representation
    if "." in bin:
        for i in range(len(bin)):
            if bin[i]==".":
                intbinary = bin[:i]
                fracbinary = bin[i+1:]
        intpart = bin_dec(intbinary)
        fracpart = fbin_dec(fracbinary)
        val = intpart + fracpart
        return val
    else: 
        val = bin_dec(bin)
        return val

def check8bitsfloat(binary):
    f=bintofloat(binary)
    if f>=0.125 and f<=31.5:
        if "." in binary:
            for i in range(len(binary)):
                if binary[i]==".":
                    index = i
                    break
            intnum = index
            fracnum = len(binary) - index - 1
            if index>=1:
                power = index-1   
                # print(power)      
                rep = "1." + binary[1:index] + binary[index+1:]
                repr = rep + f" * 2^{power}"
                if power<=4 and power>=-3:
                    l = len(rep[2:])
                    if l<=5:
                        mantissa = rep[2:]
                        unused = 5 - len(mantissa)
                        mantissa = mantissa + "0"*unused
                        exp = dec_binf(power+3)
                        unused = 3 - len(exp)
                        exp = "0"*unused + exp
                        # print(exp)
                    else: 
                        return 0
                else: 
                    return 0
                # print(repr)
                floating = exp + mantissa
                return floating
            if index<1:
                for j in range(len(binary)):
                    if binary[j]=="1":
                        index2=j
                        break
                power = index2
                rep = "1." + binary[index2+1:]
                repr = rep + f" * 2^{-power}"
                if power<=4 and power>=-3:
                    l = len(rep[2:])
                    if l<=5:
                        mantissa = rep[2:]
                        unused = 5 - len(mantissa)
                        mantissa = mantissa + "0"*unused
                        exp = dec_binf(-power+3)
                        unused = 3 - len(exp)
                        exp = "0"*unused + exp
                    else: 
                        return 0
                else: 
                    return 0
                # print(repr)
                floating = exp + mantissa
                return floating
    else:
        return 0
    
def floatingtoval(binary):
    e = binary[8:11]
    man = binary[11:]
    exp = bin_dec(e)
    exp -= 3
    mant = "0001." + man
    if exp>=0:
        bin = mant[:4]+mant[5:5+exp]+"."+mant[5+exp:]
    if exp<0:
        bin = "."+("0"*((-exp)-1))+"1"+man
    val = bintofloat(bin)
    return val

def type_A(inst, reg1, reg2, reg3):
    r2 = bin_dec(reg_values[reg2])
    r3 = bin_dec(reg_values[reg3])

    if inst == "add":
        r1 = r2 + r3
        if r1 <= 2**16 - 1:
            result = str(dec_bin(r1))
            filler = 16-len(result)
            st = "0"*filler + result
            reg_values[reg1] = st
            reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register
        else:
            # OVERFLOW CASE
            reg_values[reg1] = '0000000000000000'
            reg_values["FLAGS"] = '0000000000001000'

    elif inst == "sub":
        r1 = r2 - r3
        if r1 >= 0: #can be zero too
            result = str(dec_bin(r1))
            filler = 16 - len(result)
            st = "0"*filler + result
            reg_values[reg1] = st
            reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register
        else:
            # OVERFLOW CASE
            reg_values[reg1] = '0000000000000000'
            reg_values["FLAGS"] = '0000000000001000'

    elif inst == "mul":
        r1 = r2 * r3
        if r1 <= 2**16 - 1:
            result = str(dec_bin(r1))
            filler = 16 - len(result)
            st = "0"*filler + result
            reg_values[reg1] = st
            reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register
        else:
            # OVERFLOW CASE
            reg_values[reg1] = '0000000000000000'
            reg_values["FLAGS"] = '0000000000001000'

    elif inst == "xor":
        a = reg_values[reg2]
        b = reg_values[reg3]
        st = ''
        for i in range(16):
            if a[i] == b[i]:
                st += '0'
            else:
                st += '1'
        reg_values[reg1] = st
        reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register

    elif inst == "or":
        a = reg_values[reg2]
        b = reg_values[reg3]
        st = ''
        for i in range(16):
            if a[i] == '0' and b[i] == '0':
                st += '0'
            else:
                st += '1'
        reg_values[reg1] = st
        reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register

    elif inst == "and":
        a = reg_values[reg2]
        b = reg_values[reg3]
        st = ''
        for i in range(16):
            if a[i] == '1' and b[i] == '1':
                st += '1'
            else:
                st += '0'
        reg_values[reg1] = st
        reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register

    stringprint = f"{dec_bin7(pc)}        {reg_values['R0']} {reg_values['R1']} {reg_values['R2']} {reg_values['R3']} {reg_values['R4']} {reg_values['R5']} {reg_values['R6']} {reg_values['FLAGS']}"
    print(stringprint)
    # print(inst, reg1, reg2, reg3)
    # print(dec_bin7(pc))
    # print(reg_values)

def type_Af(inst, reg1, reg2, reg3):
    r2 = floatingtoval(reg_values[reg2])
    r3 = floatingtoval(reg_values[reg3])

    if inst == "addf":
        r1 = r2 + r3
        stra = str(r1)
        strans = floattobin(float(stra))
        if (check8bitsfloat(strans)):
            reg_values[reg1]="00000000"+check8bitsfloat(strans)
            reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register
        else:
            # OVERFLOW CASE
            reg_values[reg1] = '0000000000000000'
            reg_values["FLAGS"] = '0000000000001000'

    elif inst == "subf":
        r1 = r2 - r3
        if r1>=0:
            stra = str(r1)
            strans = floattobin(float(stra))
            if (check8bitsfloat(strans)):
                reg_values[reg1]="00000000"+check8bitsfloat(strans)
                reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register
            else:
                # OVERFLOW CASE
                reg_values[reg1] = '0000000000000000'
                reg_values["FLAGS"] = '0000000000001000'
        else:
            # OVERFLOW CASE
                reg_values[reg1] = '0000000000000000'
                reg_values["FLAGS"] = '0000000000001000'
    
    stringprint = f"{dec_bin7(pc)}        {reg_values['R0']} {reg_values['R1']} {reg_values['R2']} {reg_values['R3']} {reg_values['R4']} {reg_values['R5']} {reg_values['R6']} {reg_values['FLAGS']}\n"
    print(stringprint)
    # print(inst, reg1, reg2, reg3)
    # print(dec_bin7(pc))
    # print(reg_values)

def type_B(inst, reg, imm_val):

    if inst == 'movI':
        st = '000000000' + imm_val
        reg_values[reg] = st
        reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register

    elif inst == 'ls':
        val = bin_dec(imm_val)
        if val < 16:
            a = reg_values[reg][val:]
            st = a + '0'*val
            reg_values[reg] = st
            reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register
        else:
            reg_values[reg] = '0000000000000000'
            reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register
            # reg_values['FLAGS'] = '0000000000001000' - ls doesn't overflow (just all become 0's)

    elif inst == 'rs':
        val = bin_dec(imm_val)
        if val < 16:
            a = reg_values[reg][:16-val]
            st = '0'*val + a
            reg_values[reg] = st
            reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register
        else:
            reg_values[reg] = '0000000000000000'
            reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register
            # reg_values['FLAGS'] = '0000000000001000' - rs doesn't overflow (just all become 0's)

    elif inst == 'incf':
        val = bin_dec(imm_val)
        r1 = bin_dec(reg_values[reg])
        r = r1 + val
        if r <= 2**16-1:
            result = str(dec_bin(r))
            filler = 16-len(result)
            st = "0"*filler + result
            reg_values[reg] = st
            reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register
        else:
            # OVERFLOW CASE
            reg_values[reg] = '0000000000000000'
            reg_values["FLAGS"] = '0000000000001000'

    elif inst == 'decf':
        val = bin_dec(imm_val)
        r1 = bin_dec(reg_values[reg])
        r = r1 - val
        if r >= 0:
            result = str(dec_bin(r))
            filler = 16 - len(result)
            st = "0"*filler + result
            reg_values[reg] = st
            reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register
        else:
            # OVERFLOW CASE
            reg_values[reg] = '0000000000000000'
            reg_values["FLAGS"] = '0000000000001000'
            
    elif inst == 'rrl':
        val = bin_dec(imm_val)
        if val>=16 and val<32:
            val-=16
        elif val>=32 and val<48:
            val-=32
        elif val>=48 and val<64:
            val-=48
        elif val>=64 and val<80:
            val-=64
        elif val>=80 and val<96:
            val-=80
        elif val>=96 and val<108:
            val-=96
        elif val>=108 and val<120:
            val-=108
        elif val>=120 and val<128:
            val-=120
        # now do left rotate
        st = reg_values[reg][val:] + reg_values[reg][:val]
        reg_values[reg] = st
        reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register

    elif inst == 'rrr':
        val = bin_dec(imm_val)
        if val>=16 and val<32:
            val-=16
        elif val>=32 and val<48:
            val-=32
        elif val>=48 and val<64:
            val-=48
        elif val>=64 and val<80:
            val-=64
        elif val>=80 and val<96:
            val-=80
        elif val>=96 and val<108:
            val-=96
        elif val>=108 and val<120:
            val-=108
        elif val>=120 and val<128:
            val-=120
        # now do right rotate
        st = reg_values[reg][16-val:] + reg_values[reg][:16-val]
        reg_values[reg] = st
        reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register

    stringprint = f"{dec_bin7(pc)}        {reg_values['R0']} {reg_values['R1']} {reg_values['R2']} {reg_values['R3']} {reg_values['R4']} {reg_values['R5']} {reg_values['R6']} {reg_values['FLAGS']}"
    print(stringprint)
    # print(inst, reg, imm_val)
    # print(dec_bin7(pc))
    # print(reg_values)


def type_C(inst, reg1, reg2):

    if inst == 'movR':
        reg_values[reg1] = reg_values[reg2]
        reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register

    elif inst == 'div':
        r1 = bin_dec(reg_values[reg1])
        r2 = bin_dec(reg_values[reg2])
        if r2 != 0:
            quotient = r1//r2
            remainder = r1 % r2
            q_bin = dec_bin(quotient)
            q_str = '0'*(16-len(q_bin)) + q_bin
            r_bin = dec_bin(remainder)
            r_str = '0'*(16-len(r_bin)) + r_bin
            reg_values['R0'] = q_str
            reg_values['R1'] = r_str
            reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register
        else:
            # OVERFLOW CASE
            reg_values['R0'] = '0000000000000000'
            reg_values['R1'] = '0000000000000000'
            reg_values["FLAGS"] = '0000000000001000'

    elif inst == 'not':
        a = reg_values[reg2]
        st = ''
        for i in range(16):
            if a[i] == '0':
                st += '1'
            else:
                st += '0'
        reg_values[reg1] = st
        reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register

    elif inst == 'cmp':
        r1 = bin_dec(reg_values[reg1])
        r2 = bin_dec(reg_values[reg2])
        if r1 < r2:
            # if prev instr. is cmp, it flushes the previous result in FLAGS & set it for this particular instr.
            reg_values['FLAGS'] = "0000000000000100"
        elif r1 > r2:
            # if prev instr. is cmp, it flushes the previous result in FLAGS & set it for this particular instr.
            reg_values['FLAGS'] = "0000000000000010"
        elif r1 == r2:
            # if prev instr. is cmp, it flushes the previous result in FLAGS & set it for this particular instr.
            reg_values['FLAGS'] = "0000000000000001"

    elif inst == 'swap':                
        a = reg_values[reg1]
        b = reg_values[reg2]
        reg_values[reg1]=b
        reg_values[reg2]=a
        reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register

    stringprint = f"{dec_bin7(pc)}        {reg_values['R0']} {reg_values['R1']} {reg_values['R2']} {reg_values['R3']} {reg_values['R4']} {reg_values['R5']} {reg_values['R6']} {reg_values['FLAGS']}"
    print(stringprint)
    # print(inst, reg1, reg2)
    # print(dec_bin7(pc))
    # print(reg_values)

codeinput = []
for i in sys.stdin:
    codeinput.append(i)

for i in codeinput:
    i.strip()
    i.strip("\n")
    i1=i.replace("\n","")
    i2=i1.replace("\r","")
    input_file_list.append(i2)
    
# print(input_file_list)
# create a memory_dict and count till hlt instr, after then data memory
for i in range(len(input_file_list)):
    temp = str(dec_bin(i))
    pc_str = ''
    filler_0 = 7-len(temp)
    pc_str += "0"*filler_0 + temp
    memory_dict[pc_str] = input_file_list[i]

# memory dump --
for i in range(len(input_file_list),128):
    temp = str(dec_bin(i))
    pc_str = ''
    filler_0 = 7-len(temp)
    pc_str += "0"*filler_0 + temp
    memory_dict[pc_str] = "0000000000000000"

# this list_opcode will also have 5 bits of data memory, which is not required
# but will be okay as doing break & machine code (binary file) is error-free
for i in input_file_list:
    opcode = i[:5]
    list_opcode.append(opcode)

pc=0
while (pc<len(list_opcode)):
    if dict_inst[list_opcode[pc]] == "hlt":
        # print("hlt")
        reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register
        stringprint = f"{dec_bin7(pc)}        {reg_values['R0']} {reg_values['R1']} {reg_values['R2']} {reg_values['R3']} {reg_values['R4']} {reg_values['R5']} {reg_values['R6']} {reg_values['FLAGS']}"
        print(stringprint)
        # print(dec_bin7(pc))
        # print(reg_values)
        break
        pc+=1 # will go to var (data memory), hence stop here
    elif dict_inst[list_opcode[pc]]=="movf":
        q = input_file_list[pc]
        inst = dict_inst[list_opcode[pc]]
        reg1 = dict_reg[q[5:8]]
        float_val = q[8:]
        st = '00000000' + float_val
        reg_values[reg1] = st
        reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register
        stringprint = f"{dec_bin7(pc)}        {reg_values['R0']} {reg_values['R1']} {reg_values['R2']} {reg_values['R3']} {reg_values['R4']} {reg_values['R5']} {reg_values['R6']} {reg_values['FLAGS']}\n"
        print(stringprint)
        pc+=1
    elif dict_inst[list_opcode[pc]] in list_typeA:
        q = input_file_list[pc]
        inst = dict_inst[list_opcode[pc]]
        reg1 = dict_reg[q[7:10]]
        reg2 = dict_reg[q[10:13]]
        reg3 = dict_reg[q[13:16]]
        type_A(inst, reg1, reg2, reg3)
        pc+=1
    elif dict_inst[list_opcode[pc]] in list_typeAf:
        q = input_file_list[pc]
        inst = dict_inst[list_opcode[pc]]
        reg1 = dict_reg[q[7:10]]
        reg2 = dict_reg[q[10:13]]
        reg3 = dict_reg[q[13:16]]
        type_Af(inst, reg1, reg2, reg3)
        pc+=1
    elif dict_inst[list_opcode[pc]] in list_typeB:
        q = input_file_list[pc]
        inst = dict_inst[list_opcode[pc]]
        reg1 = dict_reg[q[6:9]]
        imm_val = q[9:]
        type_B(inst, reg1, imm_val)
        pc+=1
    elif dict_inst[list_opcode[pc]] in list_typeC:
        q = input_file_list[pc]
        inst = dict_inst[list_opcode[pc]]
        reg1 = dict_reg[q[10:13]]
        reg2 = dict_reg[q[13:]]
        type_C(inst, reg1, reg2)
        pc+=1
    elif dict_inst[list_opcode[pc]] in list_typeD:
        # load & store - 16 bit data after instruction memory will ld/st to reg/mem_addr
        q = input_file_list[pc]
        inst = dict_inst[list_opcode[pc]]
        reg1 = dict_reg[q[6:9]] 
        mem_addr = q[9:]
        if inst == "ld":
            reg_values[reg1] = memory_dict[mem_addr]
            reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register
            stringprint = f"{dec_bin7(pc)}        {reg_values['R0']} {reg_values['R1']} {reg_values['R2']} {reg_values['R3']} {reg_values['R4']} {reg_values['R5']} {reg_values['R6']} {reg_values['FLAGS']}"
            print(stringprint)
            # print(inst, reg1, mem_addr)
            # print(dec_bin7(pc))
            # print(reg_values)
            pc+=1
        elif inst == "st":
            memory_dict[mem_addr] = reg_values[reg1]
            reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register
            stringprint = f"{dec_bin7(pc)}        {reg_values['R0']} {reg_values['R1']} {reg_values['R2']} {reg_values['R3']} {reg_values['R4']} {reg_values['R5']} {reg_values['R6']} {reg_values['FLAGS']}"
            print(stringprint)
            # print(inst, reg1, mem_addr)
            # print(dec_bin7(pc))
            # print(reg_values)
            pc+=1
    elif dict_inst[list_opcode[pc]] in list_typeE:
        q = input_file_list[pc]
        inst = dict_inst[list_opcode[pc]]
        mem_addr = q[9:]
        if inst == "jmp":
            reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register
            stringprint = f"{dec_bin7(pc)}        {reg_values['R0']} {reg_values['R1']} {reg_values['R2']} {reg_values['R3']} {reg_values['R4']} {reg_values['R5']} {reg_values['R6']} {reg_values['FLAGS']}"
            print(stringprint)
            # print(inst, mem_addr)
            # print(dec_bin7(pc))
            # print(reg_values)
            pc=bin_dec(mem_addr)   # unconditional jump
        elif inst == "jlt":
            if reg_values["FLAGS"] == "0000000000000100":
                reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register
                stringprint = f"{dec_bin7(pc)}        {reg_values['R0']} {reg_values['R1']} {reg_values['R2']} {reg_values['R3']} {reg_values['R4']} {reg_values['R5']} {reg_values['R6']} {reg_values['FLAGS']}"
                print(stringprint)
                # print(inst, mem_addr)
                # print(dec_bin7(pc))
                # print(reg_values)
                pc=bin_dec(mem_addr)
            else: 
                reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register
                stringprint = f"{dec_bin7(pc)}        {reg_values['R0']} {reg_values['R1']} {reg_values['R2']} {reg_values['R3']} {reg_values['R4']} {reg_values['R5']} {reg_values['R6']} {reg_values['FLAGS']}"
                print(stringprint)
                # print(inst, mem_addr)
                # print(dec_bin7(pc))
                # print(reg_values)
                pc+=1
        elif inst == "jgt":
            if reg_values["FLAGS"] == "0000000000000010":
                reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register
                stringprint = f"{dec_bin7(pc)}        {reg_values['R0']} {reg_values['R1']} {reg_values['R2']} {reg_values['R3']} {reg_values['R4']} {reg_values['R5']} {reg_values['R6']} {reg_values['FLAGS']}"
                print(stringprint)
                # print(inst, mem_addr)
                # print(dec_bin7(pc))
                # print(reg_values)
                pc=bin_dec(mem_addr)
            else: 
                reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register
                stringprint = f"{dec_bin7(pc)}        {reg_values['R0']} {reg_values['R1']} {reg_values['R2']} {reg_values['R3']} {reg_values['R4']} {reg_values['R5']} {reg_values['R6']} {reg_values['FLAGS']}"
                print(stringprint)
                # print(inst, mem_addr)
                # print(dec_bin7(pc))
                # print(reg_values)
                pc+=1
        elif inst == "je":
            if reg_values["FLAGS"] == "0000000000000001":
                reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register
                stringprint = f"{dec_bin7(pc)}        {reg_values['R0']} {reg_values['R1']} {reg_values['R2']} {reg_values['R3']} {reg_values['R4']} {reg_values['R5']} {reg_values['R6']} {reg_values['FLAGS']}"
                print(stringprint)
                # print(inst, mem_addr)
                # print(dec_bin7(pc))
                # print(reg_values)
                pc=bin_dec(mem_addr)
            else: 
                reg_values['FLAGS'] = '0000000000000000' # instr doesn't set FLAGS register
                stringprint = f"{dec_bin7(pc)}        {reg_values['R0']} {reg_values['R1']} {reg_values['R2']} {reg_values['R3']} {reg_values['R4']} {reg_values['R5']} {reg_values['R6']} {reg_values['FLAGS']}"
                print(stringprint)
                # print(inst, mem_addr)
                # print(dec_bin7(pc))
                # print(reg_values)
                pc+=1
        

# print(input_file_list)
# print(memory_dict)
# print(list_opcode)
# print(reg_values)

for i in range(128):
    stringprint = memory_dict[dec_bin7(i)]
    print(stringprint)