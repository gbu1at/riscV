from setting import *
from functions import *


def encode_riscv_instruction(instruction):

    if instruction in ["ecall", "ebreak"]:
        assert(False)

    cmd, parts = instruction.split(" ", 1)

    parts = parts.split(",")
    parts = [None] + [part.strip(" ") for part in parts]

    parts = [part if part not in REGISTERS_ALIASES else REGISTERS_ALIASES[part] for part in parts]

    cmd_opcode = instruction_opcode[cmd]["opcode"]


    res = ""

    if cmd in r_type_command:
        res =   r_type_instructions[cmd]["funct7"]  +\
                        registers_code[parts[3]]    +\
                        registers_code[parts[2]]    +\
                r_type_instructions[cmd]["funct3"]  +\
                        registers_code[parts[1]]    +\
                        cmd_opcode

    elif cmd in i_type_command:
        bits = reverse(get_segment_bits(parts[3], 0, 12))
        res =           reverse(bits[0:12]) +\
                        registers_code[parts[2]]      +\
                        i_type_instructions[cmd]["funct3"]      +\
                        registers_code[parts[1]]      +\
                        cmd_opcode

    elif cmd in s_type_command:
        bits = reverse(get_segment_bits(parts[2], 0, 12))
        res  =          reverse(bits[5:12])                   +\
                        registers_code[parts[1]]      +\
                        registers_code[parts[3]]      +\
                        s_type_instructions[cmd]["funct3"]      +\
                        reverse(bits[0:5]) +\
                        cmd_opcode

    elif cmd in b_type_command:
        bits = reverse(get_segment_bits(parts[3], 0, 13))
        res =       reverse(bits[5:11] + bits[12]) +\
                    registers_code[parts[2]]      +\
                    registers_code[parts[1]]      +\
                    b_type_instructions[cmd]["funct3"]      +\
                    reverse(bits[11] + bits[1:5]) +\
                    cmd_opcode

    elif cmd in u_type_command:
        bits = reverse(get_segment_bits(parts[2], 0, 32))
        res =       reverse(bits[12:32])       +\
                    registers_code[parts[1]]                    +\
                    cmd_opcode
        
    elif cmd in j_type_command:
        if cmd == "jal":
            bits = reverse(get_segment_bits(parts[2], 0, 21))
            res =       reverse(bits[12:20] + bits[11] + bits[1:11] + bits[20])            +\
                        registers_code[parts[1]]                                           +\
                        cmd_opcode
        

        elif cmd == "jalr":
            bits = reverse(get_segment_bits(parts[3], 0, 12))
            res =       reverse(bits)                   +\
                        registers_code[parts[2]]        +\
                        "000"                           +\
                        registers_code[parts[1]]        +\
                        "1100111"
    
    elif cmd in m_type_command:
            res =       "0000001"                       +\
                        registers_code[parts[3]]        +\
                        registers_code[parts[2]]        +\
                        m_type_instructions[cmd]["funct3"]                         +\
                        registers_code[parts[1]]        +\
                        "0111011"
    
    else:
        assert(False)

    return res
