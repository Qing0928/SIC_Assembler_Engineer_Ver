from os import write


instruction_set = {
    "ADD": 0x18, "ADDF": 0x58, "AND": 0x40, "COMP": 0x28, "COMPF": 0x88,
    "DIV": 0x24, "DIVF": 0x64, "J": 0x3C, "JEQ": 0x30, "JGT": 0x34,
    "JLT": 0x38, "JSUB": 0x48, "LDA": 0x00, "LDB": 0x68, "LDCH": 0x50,
    "LDF": 0x70, "LDL": 0x08, "LDS": 0x6C, "LDT": 0x74, "LDX": 0x04,
    "LPS": 0xD0, "MUL": 0x20, "MULF": 0x60, "OR": 0x44, "RD": 0xD8,
    "RSUB": 0x4C, "SSK": 0xEC, "STA": 0x0C, "STB": 0x78, "STCH": 0x54,
    "STF": 0x80, "STI": 0xD4, "STL": 0x14, "STS": 0x7C, "STSW": 0xE8,
    "STT": 0x84, "STX": 0x10, "SUB": 0x1C, "SUBF": 0x5C, "TD": 0xE0,
    "TIX": 0x2C, "WD": 0xDC
}

pseudo_list = ["START", "END", "BYTE", "WORD", "RESB", "RESW"]

sym_table = {}

#LOC
loc_num = 0
with open('source.txt', 'r') as f:
    for line in f.readlines():
        with open('loc.txt', 'a') as f_loc:
            instruction = line.split()
            if (len(instruction) == 3) and (instruction[1] == 'START'):
                loc_num = int(instruction[2], 16)
                print('\t' + line)
                f_loc.write('\t' + line)

            elif (len(instruction) == 2) and (instruction[0] == 'END'):
                print("{:X}".format(loc_num) + '\t' + line)
                f_loc.write("{:X}".format(loc_num) + '\t' + line)
                
            elif (len(instruction) == 3) and (instruction[1] not in pseudo_list):
                print("{:X}".format(loc_num) + '\t' + line)
                f_loc.write("{:X}".format(loc_num) + '\t' + line)
                loc_num += 3
            
            elif (len(instruction) == 2) and (instruction[0] not in pseudo_list):
                print("{:X}".format(loc_num) + '\t' + line)
                f_loc.write("{:X}".format(loc_num) + '\t' + line)
                loc_num += 3

            elif (len(instruction) == 3) and (instruction[1] in pseudo_list):
                if instruction[1] == 'WORD':
                    print("{:X}".format(loc_num) + '\t' + line)
                    f_loc.write("{:X}".format(loc_num) + '\t' + line)
                    loc_num += 3

                elif instruction[1] == 'BYTE':
                    print("{:X}".format(loc_num) + '\t' + line)
                    f_loc.write("{:X}".format(loc_num) + '\t' + line)
                    loc_add = instruction[2].split('\'')
                    
                    if loc_add[0] == 'C':
                        loc_num += len(loc_add[1])
                    elif loc_add[0] == 'X':
                        loc_num += len(loc_add[1]) // 2 

                elif instruction[1] == 'RESW':
                    print("{:X}".format(loc_num) + '\t' + line)
                    f_loc.write("{:X}".format(loc_num) + '\t' + line)
                    loc_num += int(instruction[2])*3

                elif instruction[1] == 'RESB':
                    print("{:X}".format(loc_num) + '\t' + line)
                    f_loc.write("{:X}".format(loc_num) + '\t' + line)
                    loc_num += int(instruction[2])
            
            elif (len(instruction) == 1) and (instruction[0] not in pseudo_list) and (instruction[0] != '.'):
                print("{:X}".format(loc_num) + '\t' + line)
                f_loc.write("{:X}".format(loc_num) + '\t' + line)
                loc_num += 3
            
            else:
                print(line)
                f_loc.write(line)

#sym_table
with open('loc.txt', 'r') as f:
    for line in f.readlines():
        instruction = line.split()
        if (len(instruction) != 4) or instruction[1] == 'FIRST':
            continue
        else:
            sym_table.setdefault(instruction[1], instruction[0])

#obj_code
with open('loc.txt', 'r') as f:
    for line in f.readlines():
        with open('objcode.txt', 'a') as f_objcode:
            line = line.strip('\n')
            instruction = line.split()
            if line.startswith('.'):
                print(line + '\n')
                f_objcode.write(line + '\n')

            elif 'START' in instruction:
                print(line + '\n')
                f_objcode.write(line + '\n')
            
            elif 'END' in instruction:
                print(line + '\n')
                f_objcode.write(line + '\n')

            elif (len(instruction) == 4) and (instruction[2] not in pseudo_list):
                if ',X' in instruction[3]:
                    tmp = instruction[3].rstrip(',X')
                    sym_tmp = int(sym_table[tmp], 16) + 0x8000
                    print(line + '\t' + "{:02X}{:X}".format(instruction_set[instruction[2]], sym_tmp))
                    f_objcode.write(line + '\t' + "{:02X}{:X}".format(instruction_set[instruction[2]], sym_tmp) + '\n')
                else:
                    print(line + '\t' + "{:02X}".format(instruction_set[instruction[2]]) + sym_table[instruction[3]])
                    f_objcode.write(line + '\t' + "{:02X}".format(instruction_set[instruction[2]]) + sym_table[instruction[3]] + '\n')

            elif (len(instruction) == 3) and (instruction[1] not in pseudo_list):
                if ',X' in instruction[2]:
                    tmp = instruction[2].rstrip(',X')
                    sym_tmp = int(sym_table[tmp], 16) + 0x8000
                    print(line + '\t' + "{:02X}{:X}".format(instruction_set[instruction[1]], sym_tmp))
                    f_objcode.write(line + '\t' + "{:02X}{:X}".format(instruction_set[instruction[1]], sym_tmp) + '\n')
                else:
                    print(line + '\t' + "{:02X}".format(instruction_set[instruction[1]]) + sym_table[instruction[2]])
                    f_objcode.write(line + '\t' + "{:02X}".format(instruction_set[instruction[1]]) + sym_table[instruction[2]] + '\n')
            
            elif (len(instruction) == 2) and (instruction[1] == 'RSUB'):
                print(line + '\t\t' + "{:02X}".format(instruction_set[instruction[1]]) + '0000')
                f_objcode.write(line + '\t\t' + "{:02X}".format(instruction_set[instruction[1]]) + '0000' + '\n')
            
            elif (len(instruction) == 4) and (instruction[2] in pseudo_list):
                if (instruction[2] == 'RESW') or (instruction[2] == 'RESB'):
                    print(line + '\n')
                    f_objcode.write(line + '\n')
                elif instruction[2] == 'WORD':
                    print(line + '\t' + "{:06X}".format(int(instruction[3])))
                    f_objcode.write(line + '\t' + "{:06X}".format(int(instruction[3])) + '\n')
                elif instruction[2] == 'BYTE':
                    tmp = instruction[3].split('\'')
                    obj = ''
                    if tmp[0] == 'C':
                        for i in tmp[1]:
                            obj += "{:X}".format(ord(i))
                        print(line + '\t' + obj)
                        f_objcode.write(line + '\t' + obj + '\n')
                    elif tmp[0] == 'X':
                        print(line + '\t' + tmp[1])
                        f_objcode.write(line + '\t' + tmp[1] + '\n')

#object program
loc_list = []
with open('objcode.txt', 'r') as f:
    for line in f.readlines():
        instruction = line.split()
        if 'START' in instruction:
            continue
        else:
            loc_list.append(instruction[0])

with open('objcode.txt', 'r') as f:
    objcode = ''
    obj_cut = False

    for line in f.readlines():
        with open('object_program.txt', 'a') as f_objp:
            instruction = line.split()
            #print(instruction[0])
            if 'START' in instruction:
                pname = instruction[0]
                continue
            
            elif ('FIRST' in instruction) and ('END' not in instruction):
                start = int(instruction[0], 16)
                objcode += instruction[len(instruction)-1]
                plength = int(loc_list[len(loc_list)-1], 16) - int(loc_list[0], 16)
                print('H' + pname + "{:06X}{:06X}".format(start, plength))
                f_objp.write('H' + pname + "{:06X}{:06X}".format(start, plength) + '\n')
                continue
            
            elif (instruction[0] == loc_list[len(loc_list)-2]):
                if ('RESW' not in instruction) and ('RESB' not in instruction):
                    objcode += instruction[len(instruction)-1]
                objcode_length = (len(objcode))//2
                print('T' + "{:06X}{:02X}".format(start, objcode_length) + objcode)
                f_objp.write('T' + "{:06X}{:02X}".format(start, objcode_length) + objcode + '\n')
                start = int(instruction[0], 16)        
                objcode = ''
                objcode += instruction[len(instruction)-1]
                obj_cut = False

            elif 'END' in instruction:
                print('E' + "{:06X}".format(int(loc_list[0], 16)))
                f_objp.write('E' + "{:06X}".format(int(loc_list[0], 16)) + '\n')
            
            elif '.' in instruction:
                continue

            elif ('RESW' in instruction) or ('RESB' in instruction):
                obj_cut = True

            elif ('RESW' not in instruction) and ('START' not in instruction) and ('RESB' not in instruction) and ('.' not in instruction):
                if (len(objcode) + len(instruction[len(instruction)-1]) <= 60) and (obj_cut == False):
                    objcode += instruction[len(instruction)-1]
                else:
                    objcode_length = (len(objcode))//2
                    print('T' + "{:06X}{:02X}".format(start, objcode_length) + objcode)
                    f_objp.write('T' + "{:06X}{:02X}".format(start, objcode_length) + objcode + '\n')
                    start = int(instruction[0], 16)
                    
                    objcode = ''
                    objcode += instruction[len(instruction)-1]
                    obj_cut = False