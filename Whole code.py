import sys
dict_opcodes = {"add":"00000", "sub":"00001", "mov": ["00010", "00011"], "ld":"00100", "st":"00101", 
                "mul":"00110", "div":"00111", "rs":"01000", "ls":"01001", "xor":"01010", 
                "or":"01011", "and":"01100", "not":"01101", "cmp":"01110", "jmp":"01111", 
                "jlt":"11100", "jgt":"11101", "je":"11111", "hlt":"11010","addf":"10000",
                "subf":"10001"}
# Types of instructions :- 
# Type A: 3 register type - add, sub, mul, xor, or, and
# Type B: register and immediate type - mov[0], rs, ls
# Type C: 2 registers type - mov[1], div, not, cmp
# Type D: register and memory address type - ld, st
# Type E: memory address type - jmp, jlt, jgt, je
# Type F: halt - hlt
dict_reg = {"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4":"100", "R5":"101", "R6":"110",
            "FLAGS":"111"}
list_reg = ["R0","R1","R2","R3","R4","R5","R6","FLAGS"]
reg_values = {"r0":0, "r1":0, "r2":0, "r3":0, "r4":0, "r5":0, "r6":0, 
        "flags":"0000000000000000"} #Register value is 16 bits (hence range [0,65535] (0 to 2^16-1))
list_of_assembly_inst= []
list_of_firstwords = []
list_var = []
dict_var = {}
list_typeA = ["add","sub","mul","xor","or","and"]
list_typeB = ["mov","rs","ls"]
list_typeC = ["mov","div","not","cmp"]
list_typeD = ["ld","st"]
list_typeE = ["jmp","jlt","jgt","je"]
list_label = []
list_label2 = []
defined_label = []
dict_label = {}
list_assembler = []
dict_assembler = {}
def dec_bin(dec):
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

lineinput = []
for i in sys.stdin:
    lineinput.append(i)

for lines in lineinput:
    a = lines.strip(' ')
    b = a.strip('\t')
    c = b.strip('\n')
    d = c.replace("\t"," ")
    line1 = d.split(" ")
    line=[]
    for item in line1:
        if item!="":
            line.append(item)
    if line[0]=="":
        continue
    list_of_assembly_inst.append(line)

# print(list_of_assembly_inst)
list_of_assembly_inst2=[]
for item in list_of_assembly_inst:
    if item[0][-1]==":":
        list_of_assembly_inst2.append(item[1:])
        continue
    list_of_assembly_inst2.append(item)
# print(list_of_assembly_inst2)
for item in list_of_assembly_inst:
    list_of_firstwords.append(item[0])
# print(list_of_firstwords)
list_of_firstwords_instr=[]
for item in list_of_assembly_inst:
    if item[0][-1]==":":
        list_of_firstwords_instr.append(item[1])
        continue
    list_of_firstwords_instr.append(item[0])
# print(list_of_firstwords_instr)
def_var=[]
var_count=0
if list_of_firstwords_instr[0]=="var":
    def_var.append(list_of_assembly_inst[0][1])
    var_count=1 
for i in range(len(list_of_firstwords_instr)):
    if i!=len(list_of_firstwords_instr)-1 and list_of_firstwords_instr[i]=="var" and list_of_firstwords_instr[i+1]=="var":
        var_count+=1
        def_var.append(list_of_assembly_inst[i+1][1])
# print(def_var)
count=0
for item in list_of_assembly_inst:
    if item[0] == '':
        break
    if item[0] == "var":
        list_var.append(item[1])
    if item[0] in list_typeE:
        list_label.append(item[1])
        list_label2.append(item[1]+":")        
        count+=1
    if item[0] not in list_typeE and item[0] in dict_opcodes:
        count+=1
    if item[0][-1]==":":
        defined_label.append(item[0])
        count+=1
# print(var_count)
# print(def_var)
# print(list_var)
# print(list_label)
# print(list_label2)
def_label=[]
def_label2=[]
for item in defined_label:
    i=item[:-1]
    def_label.append(i)
    def_label2.append(item)
# print(def_label)
# print(def_label2)
# print(f"The number of instructions are: {count}") 
count2=count
for item in list_var:
    dict_var[item]=dec_bin(count2)
    count2+=1
# print(dict_var)
for item in list_of_assembly_inst:
    if item[0] in def_label2:
        dict_label[item[0].replace(":","")]=dec_bin(list_of_firstwords.index(item[0])-len(list_var))
# print(dict_label)
# Error handling :-
errorgen=0
errorflag=0
errorvar1=0
errorvar2=0
errorvar3=0
errorlabel1=0
errorlabel2=0
errorinstrname=0
errorregname=0
errorimmvalue=0
newstring="" 
# Missing hlt instruction
if "hlt" not in list_of_firstwords_instr:
    newstring+="Error - Hlt instruction is missing"
    print(newstring) 
    exit()
# hlt not being used as the last instruction
if "hlt" in list_of_firstwords_instr:
    hlt_instr=list_of_firstwords_instr.index("hlt")
    if len(list_of_firstwords_instr)>hlt_instr+1:
        lineno = hlt_instr+1
        newstring+=f"Error in line no. {lineno} - Hlt is not being used as the last instruction"
        print(newstring)
        exit()
# General Syntax Error
for item in list_of_assembly_inst2:
    if len(item)<=1 and item[0]!="hlt":
        errorgen=1
        lineno = list_of_assembly_inst2.index(item)+1
        break
if (errorgen):
    newstring+=f"Error in line no. {lineno} - General Syntax Error -> Instruction invalid or incomplete"
    print(newstring)
    exit()
# variables not declared in the beginning
for item in list_of_firstwords[len(def_var):]:
    if item=="var":
        errorvar1=1
        lineno = list_of_firstwords[len(def_var):].index(item)+len(def_var)+1
        break
if (errorvar1):
    newstring+=f"Error in line no. {lineno} - The variables are not declared at the beginning of the assembly program"
    print(newstring)
    exit()

# typos in instruction name
for item in list_of_assembly_inst2:
    if item[0] in list(dict_opcodes.keys()) or item[0]=="var" or item[0][-1]==":":
        errorinstrname=0
    else:
        errorinstrname=1
        lineno = list_of_assembly_inst2.index(item)+1
        break
if (errorinstrname):
    newstring+=f"Error in line no. {lineno} - There are typos in the instruction name"
    print(newstring)
    exit()

# Illegal Imm value
for item in list_of_assembly_inst2:
    if item[0] in list_typeB and item[-1][0]=="$":
        immvalue=int(item[-1][1:])
        if immvalue>=0 and immvalue<=127:
            errorimmvalue=0
        else:
            errorimmvalue=1
            lineno = list_of_assembly_inst2.index(item)+1
            break
if (errorimmvalue):
    newstring+=f"Error in line no. {lineno} - Illegal Imm value - it is out of range[0,127]"
    print(newstring)
    exit()
# Illegal use of FLAG register
for item in list_of_assembly_inst2:
    for i in range(len(item)):
        if item[i]=="FLAGS":
            if item[0]=="mov" and item[1] in list_reg:
                errorflag+=0
            else:
                errorflag+=1
                lineno = list_of_assembly_inst2.index(item)+1
                break
if (errorflag):
    newstring+=f"Error in line no. {lineno} - Illegal use of FLAG register - this operation is not allowed on FLAG register"
    print(newstring)
    exit()
# misuse of label as variable
for item in list_of_assembly_inst2:
    if item[0] in list_typeD:
        if item[-1] not in list_var and item[-1] in def_label:
            errorvar2=1
            lineno = list_of_assembly_inst2.index(item)+1
            break
if (errorvar2):
    newstring+=f"Error in line no. {lineno} - The mem_address is not a variable but a label (misuse of label as variable)"
    print(newstring)
    exit()
# use of undefined variables
for item in list_of_assembly_inst2:
    if item[0] in list_typeD:
        if item[-1] not in list_var:
            errorvar3=1
            lineno = list_of_assembly_inst2.index(item)+1
            break
if (errorvar3):
    newstring+=f"Error in line no. {lineno} - The mem_address is not a variable or the variable is undefined/undeclared"
    print(newstring)
    exit()
# misuse of variable as label 
for item in list_of_assembly_inst2:
    if item[0] in list_typeE:
        if item[-1] not in def_label and item[-1] in list_var:
            errorlabel1=1
            lineno = list_of_assembly_inst2.index(item)+1
            break
if (errorlabel1):
    newstring+=f"Error in line no. {lineno} - The mem_address is not a label but a variable (misuse of variable as label)"
    print(newstring)
    exit()
# use of undefined labels
for item in list_of_assembly_inst2:
    if item[0] in list_typeE:
        if item[-1] not in def_label:
            errorlabel2=1
            lineno = list_of_assembly_inst2.index(item)+1
            break
if (errorlabel2):
    newstring+=f"Error in line no. {lineno} - The mem_address is not a label or the label is undefined (no such label is found)"
    print(newstring)
    exit()
# typos in reg name
for item in list_of_assembly_inst2:
    if item[0] in list_typeA:
        if item[1] in list_reg and item[2] in list_reg and item[3] in list_reg:
            errorregname=0
        else:
            errorregname=1
            lineno = list_of_assembly_inst2.index(item)+1
            break
    if item[0] in list_typeB and item[-1][0]=="$":
        if item[1] in list_reg:
            errorregname=0
        else:
            errorregname=1
            lineno = list_of_assembly_inst2.index(item)+1
            break
    if item[0] in list_typeC and item[-1][0]!="$":
        if item[1] in list_reg and item[2] in list_reg:
            errorregname=0
        else:
            errorregname=1
            lineno = list_of_assembly_inst2.index(item)+1
            break
    if item[0] in list_typeD:
        if item[1] in list_reg:
            errorregname=0
        else:
            errorregname=1
            lineno = list_of_assembly_inst2.index(item)+1
            break
if (errorregname):
    newstring+=f"Error in line no. {lineno} - There are typos in register name"
    print(newstring)
    exit()

for lines in lineinput:
    a = lines.strip(' ')
    b = a.strip('\t')
    c = b.strip('\n')
    d = c.replace("\t"," ")
    line1 = d.split(" ")
    line=[]
    for item in line1:
        if item!="":
            line.append(item)
    if line[0]=="":
        continue
    str_final = ''
    single_line = ''
    new_str = ''
    for i in line:
        #print(i)
        if i == '':
            break
        if i == "var":
            break
        
        if i in dict_opcodes:
            if i == "mov":
                if line[-1][0] == '$':
                    single_line += dict_opcodes[i][0]
                else:
                    single_line += dict_opcodes[i][1]
            else:
                single_line += dict_opcodes[i]
        if i in dict_reg:
            single_line += dict_reg[i]
        if i[0] == '$':
            single_line += dec_bin(i[1::1])
        if i in dict_var:
            single_line += dict_var[i]
        if i in def_label:
            single_line += dict_label[i]
    unused = 16 - len(single_line)
    str_final = single_line[0:5] + ('0'*unused) + (single_line[5:])
    new_str += str_final + '\n'
    if new_str!="0000000000000000\n":
        list_assembler.append(str_final)
        print(new_str)       
# for i in range(count):
#     dict_assembler[dec_bin(i)]=list_assembler[i]
# # print(dict_assembler)