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


def U_Type(key,rd,imm):
    imm_20bit = format(imm & 0xFFFFF, '020b')
    rd_B= register(rd)
    if key=="lui":
        opcode="0110111"
    elif key=="auipc":
        opcode="0010111"

    return(imm_20bit+rd_B+opcode)
    
def J_Type(key,rd,offset):
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

print(S_Type("sw","s2","0(s0)"))
print(U_Type("lui","ra",20))
print(J_Type("jal","ra",20))