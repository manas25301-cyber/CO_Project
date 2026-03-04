import sys

PC=0
cmd=[]
labels=[]
lines=sys.stdin.read().splitlines()

for x in lines:
    tmp=x.split("\n")
    for i in tmp:
        if i=="":
            continue
        i=i.split()
        if len(i)!=2:
            i[0]=i[0].replace(":", "")
            labels.append([i[0], format(PC,'08x')])
            i.pop(0)
        i[-1]=i[-1].split(",")
        i.append(format(PC,'08x'))
        cmd.append(i)
        PC+=4

instr={"R":["add","sub","sll","slt","sltu","xor","srl","or","and"],"I":["lw","addi","sltiu","jalr"],"S":["sw"],"B":["beq","bne","blt","bge","bltu","bgeu"],"U":["lui","auipc"],"J":["jal"]}

#exe->Each executable, format->[instruction, [rd, rs1, rs2], PC] (Nested List)

def main():
    for exe in cmd:
        idx=0
        for chk in list(instr.values()): #Checks Each List of the dictionary
            if exe[0] in chk:
                break
            else:
                idx+=1

        if idx==0: #execute R-type
            print(R_type(exe[0], exe[1][0], exe[1][1], exe[1][2]))

        elif idx==1: #execute I-type
            if exe[0]=="lw":
                tmp=exe[1][1]
                imm, rs = tmp.replace(")", "").split("(")
                print(I_type(exe[0], exe[1][0], rs, imm))
            else:
                print(I_type(exe[0], exe[1][0], exe[1][1], exe[1][2]))

        elif idx==2: #execute S-type
            print(S_Type(exe[0], exe[1][0], exe[1][1]))         

        elif idx==3: #execute B-type
            print(B_type(exe[0],exe[1][0],exe[1][1],exe[1][2],exe[-1]))    

        elif idx==4: #execute U-type
            print(U_Type(exe[0], exe[1][0], exe[1][1]))
            
        elif idx==5: #execute J-type
            currentpc = int(exe[-1], 16)
            for i in range(len(labels)):
                if labels[i][0] == exe[1][1]:
                    j = i
                    break
            label_program_counter = int(labels[j][1], 16)
            offset = label_program_counter - currentpc
            print(J_Type(exe[0],exe[1][0],offset))
            
        else: #error:cmd not found
            print("NA")                   

def register(r):
    reg=['zero','ra','sp','gp','tp','t0','t1','t2','s0','s1','a0','a1','a2','a3','a4','a5','a6','a7','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','t3','t4','t5','t6']
    c=0
    for i in range(32):
        if reg[i]==r:
            b=f'{i:05b}'
            c=1
            break
    if r=='fp':
        b='01000'
    return b

def R_type(ins,rd,rs1,rs2):
        opcode="0110011"
        rd=register(rd)
        rs1=register(rs1)
        rs2=register(rs2)
        func3= ["000","000","001","010","011","100","101","110","111"]
        func7=["0000000","0100000","0000000","0000000","0000000","0000000","0000000","0000000","0000000"]
        inst=["add","sub","sll","slt","sltu","xor","srl","or","and"]

        for i in range(9):
            if inst[i]==ins:
                code= func7[i] + rs2 + rs1 + func3[i] + rd + opcode
                break
        else:
            code="error"
        return code

def I_type(ins, rd, rs, imm):
    s=''
    imm=format(int(imm) & 0xFFF, '012b')
    rd=register(rd)
    rs=register(rs)
    s=s+imm
    if ins=="lw":
        s=s+rs+"010"+rd+"0000011"
    elif ins=="addi":
        s=s+rs+"000"+rd+"0010011"
    elif ins=="sltiu":
        s=s+rs+"011"+rd+"0010011"
    elif ins=="jalr":
        s=s+rs+"000"+rd+"1100111"
    else:
        s="error"
    return s

def S_Type(key, rs2, s):
    val = int(s[:s.index("(")])
    rs1 = s[s.index("(")+1 : -1]

    val_12bit = format(val & 0xFFF, '012b')

    rs2_B = register(rs2)
    rs1_B = register(rs1)

    opcode = "0100011"

    if key == "sb":
        funct3 = "000"
    elif key == "sh":
        funct3 = "001"
    elif key == "sw":
        funct3 = "010"
    else:
        raise ValueError("Invalid S-type instruction")

    return (val_12bit[0:7] + rs2_B + rs1_B + funct3 +
            val_12bit[7:] + opcode)


def B_type(ins,r1,r2,imm,currentpc):
    opcode = '1100011'
    r1_ = register(r1)
    r2_ = register(r2)
    func3=""
    if ins == "beq":
        func3 = "000"
    elif ins == "bne":
        func3 = "001"
    elif ins == "blt":
        func3 = "100"
    elif ins == "bge":
        func3 = "101"
    elif ins == "bltu":
        func3 = "110"
    elif ins == "bgeu":
        func3 = "111"
    j=-1
    for i in range(len(labels)):
        if labels[i][0]==imm:
            j=i
            break
    if j!=-1:
        currentpc = int(currentpc, 16)
        label_program_counter = int(labels[j][1], 16)
        offset = label_program_counter - currentpc
        imm = offset
    try:
        imm = int(imm)
    except:
        raise ValueError("ERROR: INVALID LABEL GIVEN")
    if imm % 2 != 0:
        raise ValueError("Branch offset must be multiple of 2")
    if imm < -4096 or imm > 4094:
        raise ValueError("Branch offset out of range")
    imm = imm // 2
    immcode = format(imm & 0xFFF, '012b')
    code = immcode[0] + immcode[2:8] + r2_ + r1_ + func3 + immcode[8:] + immcode[1] + opcode
    return code

def U_Type(key,rd,imm):
    imm_20bit = format(imm & 0xFFFFF, '020b')
    rd_B= register(rd)
    if key=="lui":
        opcode="0110111"
    elif key=="auipc":
        opcode="0010111"

    return(imm_20bit+rd_B+opcode)

def J_Type(key,rd,offset):
    offset=(offset)
    if offset % 2 != 0:
        raise ValueError("Offset must be 2-byte aligned")

    offset=offset//2

    if offset<-(2**20) or offset>=(2**20):
        raise ValueError("Offset out of 21-bit range")

    imm = offset & 0x1FFFFF
    offset_20bit = format(imm, '021b')

    rd_B= register(rd)
    opcode="1101111"

    return(offset_20bit[0]+offset_20bit[10:20]+offset_20bit[9]+offset_20bit[1:9]+rd_B+opcode)

main()
