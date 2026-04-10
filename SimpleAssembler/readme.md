# RISC-V Assembler (Instruction to Binary)

## Project Description
We implemented a RISC-V assembler written in Python that converts RISC-V assembly instructions into 32-bit machine code.

The program is designed to read the assembly instructions from an input file, process them, and then write the corresponding machine code or error messages into an output file.

## Objectives for the Assembler
- Parse RISC-V assembly instructions.
- Identify instruction types and move to the function accordingly.
- Encode instructions into 32-bit machine code.
- Handle labels and program counters.
- Check the instruction syntax and provided operands.
- Ensure the program contains a valid virtual halt instruction.

## A Flow Diagram for the Assembler's Working
             Start
               │
               │
        Read Input File
               │
               │
       Parse Instructions
               │
               │
        Detect Labels
               │
               │
    Determine Instruction Type
               │
               │
         Validate Syntax
               │
               │
        Encode Instruction
               │
               │
      Append Binary to Output
               │
               │
         Write Output File
               │
               │
              End

## Program Architecture
The assembler works in three major stages:
### Parsing Stage
The program reads the input file and:
- Removes empty lines
- Identifies labels
- Extracts instructions
- Stores instructions along with their program counter (PC)

To do this, we have made a list:
1. cmd: stores parsed instruction 
2. labels: stores the labels along with their PC
3. output_list: stores machine code or the error for the individual corresponding element in `cmd`

### Validation Stage
The assembler performs multiple checks:
- Duplicate labels
- Invalid registers
- Incorrect syntax
- Immediate range errors
- Undefined labels
- Invalid branch offsets

Depending on the instruction type, we duly check:
1. Incorrect syntax
2. Immediate range errors
3. Undefined labels
4. Invalid branch offsets

### 3. Encoding Stage

Each instruction is encoded based on its type and is sent to the following functions:
- R_type()
- I_type()
- S_Type()
- B_type()
- U_Type()
- J_Type()
## Usage
To implement the program, please follow up with this syntax
```
python assembler.py <input_file> <output_file>
```

Example:
```
python assembler.py program.s output.txt
```

- `<input_file>`: Assembly source file
- `<output_file>`: File where binary output (or errors) is written

## Input Format

- One instruction per line (Please avoid providing the instructions over two lines)
- Empty lines are ignored
- Labels are supported using `label:` (Please make sure to provide the ":" after the label)
- Label and instruction can be on the same line:

```
loop: add a0, a1, a2
```

## Supported Instruction Types 
We made sure to implement the ones that were stated in the instruction PDF, which are as follows:
### R-type
- `add`, `sub`, `sll`, `slt`, `sltu`, `xor`, `srl`, `or`, `and`
```
| funct7 | rs2 | rs1 | funct3 | rd | opcode |
| 7 bits |5bits|5bits| 3 bits |5bits|7 bits |
```
### I-type
- `lw`, `addi`, `sltiu`, `jalr`
```
| immediate | rs1 | funct3 | rd | opcode |
| 12 bits   |5bits| 3 bits |5bits|7 bits |
```
### S-type
- `sw`,`sb`,`sh`
```
| imm[11:5] | rs2 | rs1 | funct3 | imm[4:0] | opcode |
```
### B-type
- `beq`, `bne`, `blt`, `bge`, `bltu`, `bgeu`
```
| imm[12] | imm[10:5] | rs2 | rs1 | funct3 | imm[4:1] | imm[11] | opcode |
```
and the branch offset is: `offset = label_address - current_PC`
### U-type
- `lui`, `auipc`
```
| immediate[31:12] | rd | opcode |
```
### J-type
- `jal`
```
| imm[20] | imm[10:1] | imm[11] | imm[19:12] | rd | opcode |
```

## Register Names
The assembler accepts the naming convention:

`zero, ra, sp, gp, tp, t0, t1, t2, s0, s1, a0-a7, s2-s11, t3-t6`

A special case to be noted :
- `fp` is treated as `s0`

## Label Handling
- Label addresses are tracked using the current PC (increments by 4 per instruction) and are stored in the list named `labels`
- Duplicate labels are detected and will surely provide an error
- Branch and jump instructions may use labels or immediate offsets (depending on instruction logic)

## Virtual Halt Rule in This Implementation

This assembler is maintained to ensure a valid halt is provided as the very last instruction.
A program will be encoded only if the last instruction is in the format of:

- `jal <reg>, 0`
- `<last_label>: jal <reg>, <last_label>` where PC matches that label
- `beq <reg>, <same_reg>, 0`
- `<last_label>: beq <reg1>, <reg2>, <last_label>` where PC matches that label

If this condition is not met, it will return:

    ERROR: VALID PROGRAM HALT MISSING

## Error Handling

We had ensured that every possible error encountered was reported and fully handled by providing appropriate error handling.

FOR EXAMPLE: `Line 4 ERROR: Invalid register provided`

If any instruction fails, the basic format for errors is written as:

    Line <n> <error_message>

Common error messages include:

- Invalid instruction or syntax error:

      Error: Incorrect instruction syntax

- Invalid register

      ERROR: Invalid register provided
    
- Immediate out of range (I/S/U/J/B constraints)
      
      ERROR: immediate out of range

- Branch alignment/range issues

      ERROR: Branch offset must be a multiple of 2



## POINTS TO BE NOTED

- The assembler writes plain 32-bit binary strings (not hexadecimal output).
- PC starts at `0x00000000` and increments by 4 for each parsed instruction.

## Minimal Example

Input (`program.s`):

```
start: add a0, a1, a2
addi a0, a0, 4
beq a0, a0, 0
```

Run:

```
python assembler.py program.s output.txt
```

Output (`output.txt`) will contain one 32-bit binary instruction per line if all lines are valid.
