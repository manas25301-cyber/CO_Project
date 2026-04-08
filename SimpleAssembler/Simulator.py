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
    current_pc = 0
    i=0
    while 0<=i<len(cmd):
        exe=cmd[i]
        pc = exe.split(":")[0]
        instruction = exe.split(":")[1]
        opcode = instruction[25:32]
        if len(instruction)!=32:
            raise Exception(f"Invalid instruction at PC {pc}")
        if opcode == "0110011":
            R_type()
            current_pc += 4
            i+=1
            zero_value_error()
            PC_BOUND(current_pc,cmd)
        elif (opcode == "0010011" or opcode == "0000011" or opcode == "1100111"):
            I_type(current_pc, instruction)
            current_pc += 4
            i+=1
            zero_value_error()
            PC_BOUND(current_pc, cmd)
        elif opcode == "0100011":
            S_type()
            current_pc += 4
            i+=1
            zero_value_error()
            PC_BOUND(current_pc, cmd)
        elif opcode == "1100011":
            edited,final_pc,final_i=B_type(current_pc, instruction,i)
            if not edited:
                current_pc += 4
                i+=1
            else:
                current_pc=final_pc
                i=final_i
            zero_value_error()
            PC_BOUND(current_pc, cmd)
        elif (opcode == "0110111" or opcode == "0010111"):
            U_type()
            current_pc += 4
            i+=1
            zero_value_error()
            PC_BOUND(current_pc, cmd)
        elif opcode == "1101111":
            current_pc,i=J_type(current_pc,instruction,i)
            zero_value_error()
            PC_BOUND(current_pc, cmd)
        else:
            raise Exception(f"Invalid instruction at PC {pc}")
    return 0


def PC_BOUND(current_pc,cmd):
    if current_pc<0:
        raise Exception("Invalid PC (IT PROJECTING LESS THAN ZERO)")
    if current_pc >= len(cmd)*4:
        raise Exception("Invalid PC (OUT OF BOUND OF PROGRAM RANGE)")

def zero_value_error():
    if registers['zero']!=0:
        raise Exception("ERROR: ZERO REGISTER IS FILLED WITH VALUE (NOT ALLOWED)")

def unsigned_32_bits(value):
    return value & 0xFFFFFFFF

def two_compliment(x):
    value = int(x,2)
    if x[0]=="1":
        value=value-(2**(len(x)))
    return value

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
    command=instruction[17:20]
    r1=instruction[12:17]
    r2=instruction[7:12]
    imm=instruction[0]+instruction[24]+instruction[1:7]+instruction[20:24]+"0"
    imm=two_compliment(imm)
    edited=0
    if command == "000":
        if registers[register(r1)]==registers[register(r2)]:
            edited=1
    elif command == "001":
        if registers[register(r1)]!=registers[register(r2)]:
            edited=1
    elif command == "100":
        if registers[register(r1)]<registers[register(r2)]:
            edited = 1
    elif command == "101":
        if registers[register(r1)]>=registers[register(r2)]:
            edited = 1
    elif command == "110":
        if unsigned_32_bits(registers[register(r1)])<unsigned_32_bits(registers[register(r2)]):
            edited = 1
    elif command == "111":
        if unsigned_32_bits(registers[register(r1)])>=unsigned_32_bits(registers[register(r2)]):
            edited = 1
    if edited:
        current_pc+=imm
        i =current_pc//4
    if current_pc % 4 != 0:
        raise Exception("ERROR: MISALIGNED PC")
    return edited,current_pc,i

def U_type():
    return

def J_type():
    rd= instruction[20:25]
    imm=instruction[0]+instruction[12:20]+instruction[11]+instruction[1:11]+"0"
    imm=two_compliment(imm)
    if register(rd)!="zero":
        registers[register(rd)]=current_pc+4
    else:
        raise Exception("ERROR: ZERO REGISTER IS FILLED WITH VALUE (NOT ALLOWED)")
    current_pc+=imm
    if current_pc % 4 != 0:
        raise Exception("ERROR: MISALIGNED PC")
    i =current_pc//4
    return current_pc,i

main()
