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
        i[-1]=i[-1].split(",")
        cmd.append(i)

instr={"R":["add","sub","sll","slt","sltu","xor","srl","or","and"],"I":["lw","addi","sltiu","jalr"],"S":["sw"],"B":["beq","bne","blt","bge","bltu","bgeu"],"U":["lui","auipc"],"J":["jal"]}

for exe in cmd:
    idx=0
    for chk in list(instr.values()):
        if exe[0] in chk:
            break
        else:
            idx+=1
    if idx==0:
        print("R")
        #execute R-type
    elif idx==1:
        print("I")
        #execute I-type
    elif idx==2:
        print("S")
        #execute S-type
    elif idx==3:
        print("B")
        #execute B-type
    elif idx==4:
        print("U")
        #execute U-type
    elif idx==5:
        print("J")
        #execute J-type
    else:
        print("NA")
        #error:cmd not found
        

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









