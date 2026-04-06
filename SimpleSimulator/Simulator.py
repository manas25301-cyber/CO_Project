import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

cmd=[]

with open(input_file) as f:
    tmp=[]
    x=f.read()
    tmp=x.split("\n")

    for i in tmp:
        i=i.strip()
        if i!="":
            cmd.append(i)
    
        
registers = {'zero':0, 'ra':0, 'sp':0, 'gp':0, 'tp':0, 't0':0, 't1':0, 't2':0, 's0':0, 
             's1':0, 'a0':0, 'a1':0, 'a2':0, 'a3':0, 'a4':0, 'a5':0, 'a6':0, 'a7':0, 's2':0, 
             's3':0, 's4':0, 's5':0, 's6':0, 's7':0, 's8':0, 's9':0, 's10':0, 's11':0, 
             't3':0, 't4':0, 't5':0, 't6':0}

memory = {}
base=0x00010000
for i in range(32):
    memory[base+i*4]=0 #initilize memory with 32 words (128 bytes) starting from address 0x00010000

f=open(output_file, 'w')
f.close() #Ensures output file is empty before writing

def write_register():
    with open(output_file, 'a') as f:
        for reg in registers:
            f.write("0b" + format(registers[reg] & 0xFFFFFFFF, '032b') + " ")
        f.write("\n")

def write_memory():
    with open(output_file, 'a') as f:
        for addr in sorted(memory.keys()):
            f.write(format(addr, '08X') + " : " + "0b" + format(memory[addr] & 0xFFFFFFFF, '032b') + "\n")

def main():
    current_pc=4
    for exe in cmd:
        instruction=exe.strip()
        opcode=instruction[25:32]
        pc_format='0b'+format(current_pc, '032b')
        if opcode=="0110011":
            print("R-type instruction at PC: "+pc_format)
            #R_type()

        elif (opcode=="0010011" or opcode=="0000011" or opcode=="1100111"):
            print("I-type instruction at PC: "+pc_format)
            I_type(current_pc, instruction)

        elif opcode=="0100011":
            print("S-type instruction at PC: "+pc_format)
            #S_type()

        elif opcode=="1100011": 
            print("B-type instruction at PC: "+pc_format)
            #B_type()

        elif (opcode=="0110111" or opcode=="0010111"):
            print("U-type instruction at PC: "+pc_format)
            #U_type()

        elif opcode=="1101111":
            print("J-type instruction at PC: "+pc_format)
            #J_type()

        else:
            print("Invalid instruction at PC: "+pc_format)

        with open(output_file, 'a') as f:
            f.write(pc_format+" ")

        current_pc+=4
        write_register()
    
    write_memory()

    return 0

def register(bin):
    reg = ['zero','ra','sp','gp','tp','t0','t1','t2','s0','s1',
           'a0','a1','a2','a3','a4','a5','a6','a7',
           's2','s3','s4','s5','s6','s7','s8','s9','s10','s11',
           't3','t4','t5','t6']
    decimal=int(bin, 2)
    return reg[decimal]

def R_type(instruction):
    return

def I_type(current_pc, instruction):
    imm=instruction[0:12]
    rs1=instruction[12:17]
    funct3=instruction[17:20]
    rd=instruction[20:25]
    opcode=instruction[25:32]

    imm=int(imm, 2)
    if imm & (1 << 11):
        imm -= 1 << 12
        
    src_reg=register(rs1)
    dest_reg=register(rd)
    print(f"Decoded I-type instruction: opcode={opcode}, funct3={funct3}, rs1={src_reg}, rd={dest_reg}, imm={imm}")

    if opcode=="0010011":
        if funct3=="000":
            #addi
            registers[dest_reg]=registers[src_reg]+imm

        elif funct3=="011":
            #sltiu
            if registers[src_reg]<imm:
                registers[dest_reg]=1

            else:
                registers[dest_reg]=0

    elif opcode=="0000011":
        if funct3=="010":
            #lw
            address=registers[src_reg]+imm
            if address%4 != 0:
                print("Error: Unaligned memory access at address "+hex(address))
                return -1   
            
            value=memory.get(address, 0) #default value is 0 if address not in memory

            registers[dest_reg]=value
    
    elif opcode=="1100111":
        if funct3=="000":
            #jalr
            registers[dest_reg]=current_pc+4
            current_pc=(registers[src_reg]+imm) & ~1 #make LSB=0
    
    else:
        print("Error: Invalid opcode for I-type instruction")
        return -1

    return 0

def S_type():
    return

def B_type():
    return

def U_type():
    return

def J_type():
    return

main()