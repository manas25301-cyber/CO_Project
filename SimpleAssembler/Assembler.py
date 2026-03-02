import os

base=os.path.dirname(__file__)
path=os.path.join(base,"test_case_1.txt")

cmd=[]
with open(path) as f:
    tmp=[]
    x=f.read()
    tmp=x.split("\n")
    for i in tmp:
        if i=="":
            continue
        i=i.split()
        if len(i)!=2:
            continue
        i[-1]=i[-1].split(",")
        cmd.append(i)

instr={"R":["add","sub","sll","slt","sltu","xor","srl","or","and"],"I":["lw","addi","sltiu","jalr"],"S":["sw"],"B":["beq","bne","blt","bge","bltu","bgeu"],"U":["lui","auipc"],"J":["jal"]}

#exe->Each executable, format->[instruction, [rd, rs1, rs2]] (Nested List)

def main():
    for exe in cmd:
        idx=0
        for chk in list(instr.values()):
            if exe[0] in chk:
                break
            else:
                idx+=1

        if idx==0: #execute R-type
            print("R")

        elif idx==1: #execute I-type
            if exe[0]=="lw":
                tmp=exe[1][1]
                imm, rs = tmp.replace(")", "").split("(")
                print(I_type(exe[0], exe[1][0], rs, imm))
            else:
                print(I_type(exe[0], exe[1][0], exe[1][1], exe[1][2]))

        elif idx==2: #execute S-type
            print("S")         

        elif idx==3: #execute B-type
            print("B")    

        elif idx==4: #execute U-type
            print("U")
            
        elif idx==5: #execute J-type
            print("J")
            
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
    if c=='fp':
        b='01000'
    return b

def I_type(ins, rd, rs, imm):
    s=''
    imm=format(int(imm) & 0xFF, '012b')
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

main()












