from setting import *
from functions import *


def encode_riscv_instruction(instruction):

    if instruction in ["ecall", "ebreak", "pause"]:
        if instruction == "ebreak":
            return "00000000000100000000000001110011"
        elif instruction == "ecall":
            return "00000000000000000000000001110011"
        elif instruction == "pause":
            return "00000001000000000000000000001111"
        else:
            return "--------------------------------"

    cmd, parts = instruction.split(" ", 1)

    if cmd == "fence":
        cmd, parts = instruction.split(" ", 1)
        parts = parts.split(",")
        p, s = parts[0], parts[1]
        x = 'iorw'
        p = p
        s = s
        p = ''.join(['1' if x[i] in p else '0' for i in range(4)])
        s = ''.join(['1' if x[i] in s else '0' for i in range(4)])
        return '0000' + p + s + '00000000000000001111'

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
        i, j = 3, 2
        if cmd in ["lb", "lh", "lw", "lbu", "lhu"]:
            i, j = 2, 3
        bits = reverse(get_segment_bits(parts[i], 0, 12))
        res =           reverse(bits[0:12]) +\
                        registers_code[parts[j]]      +\
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
                        "0110011"
    
    elif cmd in si_type_command:
        bits = reverse(get_segment_bits(parts[3], 0, 5))
        res =           si_type_instructions[cmd]["code"]         +\
                        reverse(bits)                             +\
                        registers_code[parts[2]]                  +\
                        si_type_instructions[cmd]["funct3"] +\
                        registers_code[parts[1]]                  +\
                        "0010011"


    return res
