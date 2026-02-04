def register(r):
    reg=['zero','ra','sp','gp','tp','t0','t1','t2','s0','s1','a0','a1','a2','a3','a4','a5','a6','a7','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','t3','t4','t5','t6']
    c=0
    for i in range(32):
        if reg[i]==r:
            b=f'{i:05b}'
            c=1
            break
    if c==0:
        b='01000'
    return b

def S-Type(key,rs2,s):
    val= int(s[:s.index("(")])
    rs1= s[s.index("(")+1 : -1]
    val_12bit = format(val, '012b')
    
    rs2_B= register(rs2)
    rs1_B= register(rs1)
    
    opcode="0100011"
    
    if key=="sb":
        funct3="000"
    elif key=="sh":
        funct3="001"
    elif key=="sw":
        funct3="010"
    
    return(val_12bit[0:7]+rs2_B+rs1_B+funct3+val_12bit[7:]+opcode)


def U-Type():

def J-Type():

