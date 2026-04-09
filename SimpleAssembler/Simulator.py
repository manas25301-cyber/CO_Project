import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

cmd = []

with open(input_file) as f:
    tmp = []
    x = f.read()
    tmp = x.split("\n")

    for i in tmp:
        i = i.strip()
        if i != "":
            cmd.append(i)

registers = {'zero': 0, 'ra': 0, 'sp': 0, 'gp': 0, 'tp': 0, 't0': 0, 't1': 0, 't2': 0, 's0': 0,
             's1': 0, 'a0': 0, 'a1': 0, 'a2': 0, 'a3': 0, 'a4': 0, 'a5': 0, 'a6': 0, 'a7': 0, 's2': 0,
             's3': 0, 's4': 0, 's5': 0, 's6': 0, 's7': 0, 's8': 0, 's9': 0, 's10': 0, 's11': 0,
             't3': 0, 't4': 0, 't5': 0, 't6': 0}

memory = {}
base = 0x00010000
for i in range(32):
    memory[base + i * 4] = 0  # initilize memory with 32 words (128 bytes) starting from address 0x00010000

f = open(output_file, 'w')
f.close()  # Ensures output file is empty before writing


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
    i = 0
    while 0 <= i < len(cmd):
        instruction = cmd[i]
        opcode = instruction[25:32]
        if len(instruction) != 32:
            with open(output_file, 'a') as f:
                f.write(f"Invalid instruction at PC {current_pc}")
            return -1
        if opcode == "0110011":  # R-type
            print("R-type instruction detected at PC " + hex(current_pc))
            R_type(instruction)
            current_pc += 4
            i += 1
            zero_value_error()
            PC_BOUND(current_pc, cmd)

        elif (opcode == "0010011" or opcode == "0000011" or opcode == "1100111"):  # I-type
            print("I-type instruction detected at PC " + hex(current_pc))
            edited, final_pc, final_i = I_type(current_pc, instruction, i)
            if not edited:
                current_pc += 4
                i += 1
            else:
                current_pc = final_pc
                i = final_i
            zero_value_error()
            PC_BOUND(current_pc, cmd)

        elif opcode == "0100011":  # S-type
            print("S-type instruction detected at PC " + hex(current_pc))
            S_type(current_pc, instruction)
            current_pc += 4
            i += 1
            zero_value_error()
            PC_BOUND(current_pc, cmd)

        elif opcode == "1100011":  # B-type
            print("B-type instruction detected at PC " + hex(current_pc))
            edited, final_pc, final_i = B_type(current_pc, instruction, i)
            if not edited:
                current_pc += 4
                i += 1
            elif edited==2:
                print("VIRTUAL HALT INITIATED: PROGRAM STOPS")
                return -1
            else:
                current_pc = final_pc
                i = final_i
            zero_value_error()
            PC_BOUND(current_pc, cmd)

        elif (opcode == "0110111" or opcode == "0010111"):  # U-type
            print("U-type instruction detected at PC " + hex(current_pc))
            U_type(current_pc, instruction)
            current_pc += 4
            i += 1
            zero_value_error()
            PC_BOUND(current_pc, cmd)

        elif opcode == "1101111":  # J-type
            print("J-type instruction detected at PC " + hex(current_pc))
            current_pc, i = J_type(current_pc, instruction, i)
            if (current_pc==-1)and(i==-1):
                print("VIRTUAL HALT INITIATED: PROGRAM STOPS")
                return -1
            if (current_pc==-1)and(i==-2):
                return -1
            zero_value_error()
            PC_BOUND(current_pc, cmd)

        else:  # Invalid opcode
            with open(output_file, 'a') as f:
                f.write(f"Invalid instruction at PC {current_pc:032b}")
            return -1
        with open(output_file, 'a') as f:
            f.write(f"0b{current_pc:032b} ")
        write_register()
    write_memory()
    return 0


def write_reg(reg, value):
    if reg != 'zero':
        registers[reg] = unsigned_32_bits(value)


def B_To_D(binary_str):
    k = len(binary_str)
    val = int(binary_str, 2)
    if (val & (1 << (k - 1))):
        val = val - (1 << k)
    return val


def PC_BOUND(current_pc, cmd):
    if current_pc < 0:
        raise Exception("Invalid PC (IT PROJECTING LESS THAN ZERO)")
    if current_pc >= len(cmd) * 4:
        raise Exception("Invalid PC (OUT OF BOUND OF PROGRAM RANGE)")


def zero_value_error():
    if registers['zero'] != 0:
        registers['zero'] = 0


def unsigned_32_bits(value):
    return value & 0xFFFFFFFF


def two_compliment(x):
    value = int(x, 2)
    if x[0] == "1":
        value = value - (2 ** (len(x)))
    return value


def register(bin):
    reg = ['zero', 'ra', 'sp', 'gp', 'tp', 't0', 't1', 't2', 's0', 's1',
           'a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7',
           's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11',
           't3', 't4', 't5', 't6']
    decimal = int(bin, 2)
    return reg[decimal]


def R_type(instruction):
    # To be implemented
    return


def I_type(current_pc, instruction, i):
    imm = instruction[0:12]
    rs1 = instruction[12:17]
    funct3 = instruction[17:20]
    rd = instruction[20:25]
    opcode = instruction[25:32]

    imm = int(imm, 2)
    if imm & (1 << 11):
        imm -= 1 << 12

    src_reg = register(rs1)
    dest_reg = register(rd)

    edited = 0
    final_pc = current_pc
    final_i = i

    if opcode == "0010011":
        if funct3 == "000":
            # addi
            write_reg(dest_reg, registers[src_reg] + imm)

        elif funct3 == "011":
            # sltiu
            # Compare as unsigned values
            if unsigned_32_bits(registers[src_reg]) < unsigned_32_bits(imm):
                write_reg(dest_reg, 1)
            else:
                write_reg(dest_reg, 0)

    elif opcode == "0000011":
        if funct3 == "010":
            # lw
            address = registers[src_reg] + imm
            if address % 4 != 0:
                with open(output_file, 'a') as f:
                    f.write(f"Error: Unaligned memory access at address {address:08x}\n")
                return -1, final_pc, final_i

            value = memory.get(address, 0)  # default value is 0 if address not in memory
            write_reg(dest_reg, value)

    elif opcode == "1100111":  # jalr
        if funct3 == "000":
            target = (registers[src_reg] + imm) & ~1
            write_reg(dest_reg, current_pc + 4)
            if target % 4 != 0:
                with open(output_file, 'a') as f:
                    f.write(f"Error: Misaligned PC at address {target:032b}\n")
                return -1, final_pc, final_i
            final_pc = target
            final_i = final_pc // 4
            edited = 1

    return edited, final_pc, final_i


def S_type(current_pc, instr):
    imm1 = instr[0:7]
    rs2 = instr[7:12]
    rs1 = instr[12:17]
    funct3 = instr[17:20]
    imm2 = instr[20:25]
    opcode = instr[25:32]

    imm = imm1 + imm2
    imm = int(imm, 2)

    if imm & (1 << 11):
        imm -= (1 << 12)

    src1 = register(rs1)
    src2 = register(rs2)

    if funct3 == "010":
        addr = registers[src1] + imm
        if addr % 4 != 0:
            with open(output_file, 'a') as f:
                f.write(f"Error: Unaligned memory access at address {addr:08x}\n")
            return -1
        memory[addr] = unsigned_32_bits(registers[src2])
    else:
        with open(output_file, 'a') as f:
            f.write(f"Invalid S-type instruction at PC {current_pc:032b}\n")
        return -1

    return 0


def B_type(current_pc, instruction, i):
    command = instruction[17:20]
    r1 = instruction[12:17]
    r2 = instruction[7:12]
    imm = instruction[0] + instruction[24] + instruction[1:7] + instruction[20:24] + "0"
    imm = two_compliment(imm)
    edited = 0
    # Treat register values as signed for blt/bge
    val1 = registers[register(r1)]
    val2 = registers[register(r2)]
    # Sign extend for signed comparisons
    if val1 & 0x80000000:
        val1_signed = val1 - 0x100000000
    else:
        val1_signed = val1

    if val2 & 0x80000000:
        val2_signed = val2 - 0x100000000
    else:
        val2_signed = val2

    if command == "000":  # beq
        if val1 == val2:
            edited = 1
    elif command == "001":  # bne
        if val1 != val2:
            edited = 1
    elif command == "100":  # blt (signed)
        if val1_signed < val2_signed:
            edited = 1
    elif command == "101":  # bge (signed)
        if val1_signed >= val2_signed:
            edited = 1
    elif command == "110":  # bltu (unsigned)
        if unsigned_32_bits(val1) < unsigned_32_bits(val2):
            edited = 1
    elif command == "111":  # bgeu (unsigned)
        if unsigned_32_bits(val1) >= unsigned_32_bits(val2):
            edited = 1
    if edited:
        if imm==0:
            edited = 2
        else:
            current_pc += imm
            i = current_pc // 4
    if current_pc % 4 != 0:
        with open(output_file, 'a') as f:
            f.write(f"Error: Misaligned PC at address {current_pc:032b}\n")
        return -1, current_pc, i
    return edited, current_pc, i


def U_type(current_pc, instr):
    imm = int(instr[0:20], 2) << 12  # upper 20 bits shifted left
    rd = register(instr[20:25])
    opcode = instr[25:32]

    if opcode == "0110111":  # LUI
        write_reg(rd, unsigned_32_bits(imm))

    elif opcode == "0010111":  # AUIPC
        write_reg(rd, unsigned_32_bits(current_pc + imm))

    else:
        with open(output_file, 'a') as f:
            f.write(f"Invalid U-type instruction at PC {current_pc:032b}\n")
        return -1

    return 0


def J_type(current_pc, instruction, i):
    rd = instruction[20:25]
    imm = instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11] + "0"
    imm = two_compliment(imm)
    if imm==0:
        with open(output_file, 'a') as f:
            f.write("VIRTUAL HALT INITIATED: PROGRAM STOPS")
        return -1,-1
    dest_reg = register(rd)
    write_reg(dest_reg, unsigned_32_bits(current_pc + 4))
    current_pc += imm
    if current_pc % 4 != 0:
        with open(output_file, 'a') as f:
            f.write(f"Error: Misaligned PC at address {current_pc:032b}\n")
        return -1, -2
    i = current_pc // 4
    return current_pc, i


main()
