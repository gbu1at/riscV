from functions import *


ADDR_LEN = 18 # длина адреса (в битах)
CACHE_INDEX_LEN = 3 # длина индекса блока кэш-линий  (в битах)
CACHE_LINE_SIZE = 64 # размер кэш-линии (в байтах)
CACHE_LINE_COUNT = 32 # кол-во кэш-линий

MEM_SIZE = 2 ** ADDR_LEN # размер памяти (в байтах)
CACHE_SIZE = CACHE_LINE_SIZE * CACHE_LINE_COUNT # размер кэша, без учёта служебной информации (в байтах)

CACHE_SETS = 2 ** CACHE_INDEX_LEN  # кол-во блоков кэш-линий
CACHE_WAY = CACHE_LINE_COUNT // CACHE_SETS # ассоциативность

CACHE_OFFSET_LEN = 6 # log2(CACHE_LINE_SIZE)
CACHE_TAG_LEN = ADDR_LEN - CACHE_OFFSET_LEN - CACHE_INDEX_LEN




REGISTERS_ALIASES = {
            "zero": "x0",
            "ra": "x1",
            "sp": "x2",
            "gp": "x3",
            "tp": "x4",
            "t0": "x5",
            "t1": "x6",
            "t2": "x7",
            "s0": "x8", "fp": "x8",
            "s1": "x9",
            "a0": "x10",
            "a1": "x11",
            "a2": "x12",
            "a3": "x13",
            "a4": "x14",
            "a5": "x15",
            "a6": "x16",
            "a7": "x17",
            "s2": "x18",
            "s3": "x19",
            "s4": "x20",
            "s5": "x21",
            "s6": "x22",
            "s7": "x23",
            "s8": "x24",
            "s9": "x25",
            "s10": "x26",
            "s11": "x27",
            "t3": "x28",
            "t4": "x29",
            "t5": "x30",
            "t6": "x31", 
            "x0": "x0" , "x1": "x1" , "x2": "x2" , "x3": "x3" , "x4": "x4" , "x5": "x5" , "x6": "x6" , "x7": "x7" , "x8": "x8" , "x9": "x9" , "x10": "x10" , "x11": "x11" , "x12": "x12" , "x13": "x13" , "x14": "x14" , "x15": "x15" , "x16": "x16" , "x17": "x17" , "x18": "x18" , "x19": "x19" , "x20": "x20" , "x21": "x21" , "x22": "x22" , "x23": "x23" , "x24": "x24" , "x25": "x25" , "x26": "x26" , "x27": "x27" , "x28": "x28" , "x29": "x29" , "x30": "x30", "x31": "x31"
        }




instruction_opcode = {
    "mul": {"opcode": "0110011"},
    "mulh": {"opcode": "0110011"},
    "mulhsu": {"opcode": "0110011"},
    "mulhu": {"opcode": "0110011"},
    "div": {"opcode": "0110011"},
    "divu": {"opcode": "0110011"},
    "rem": {"opcode": "0110011"},
    "remu": {"opcode": "0110011"},


    "lui": {"opcode": "0110111"},
    "auipc": {"opcode": "0010111"},
    "jalr": {"opcode": "1100111"},

    "add":  {"opcode": "0110011"},
    "addi": {"opcode": "0010011"},
    "sub":  {"opcode": "0110011"},

    "and":  {"opcode": "0110011"},
    "andi": {"opcode": "0010011"}, 
    "or":   {"opcode": "0110011"},  
    "ori":  {"opcode": "0010011"},
    "xor":  {"opcode": "0110011"},  
    "xori": {"opcode": "0010011"},

    "sll":   {"opcode": "0110011"},
    "slli":  {"opcode": "0010011"},
    "srl":   {"opcode": "0110011"},
    "srli":  {"opcode": "0010011"},
    "sra":   {"opcode": "0110011"},
    "srai":  {"opcode": "0010011"},

    "slt":   {"opcode": "0110011"},
    "slti":  {"opcode": "0010011"},
    "sltu":  {"opcode": "0110011"},
    "sltiu": {"opcode": "0010011"},

    "beq":  {"opcode": "1100011"},
    "bne":  {"opcode": "1100011"},
    "blt":  {"opcode": "1100011"},
    "bge":  {"opcode": "1100011"},
    "bltu": {"opcode": "1100011"},
    "bgeu": {"opcode": "1100011"},

    "lb":   {"opcode": "0000011"},
    "lh":   {"opcode": "0000011"},
    "lw":   {"opcode": "0000011"},
    "lbu":  {"opcode": "0000011"},
    "lhu":  {"opcode": "0000011"},

    "sb":   {"opcode": "0100011"},
    "sh":   {"opcode": "0100011"},
    "sw":   {"opcode": "0100011"},

    "jal": {"opcode": "1101111"}
}

r_type_instructions = {
    "add":   {"funct7": "0000000", "funct3": "000"},
    "sub":   {"funct7": "0100000", "funct3": "000"},
    "sll":   {"funct7": "0000000", "funct3": "001"},
    "slt":   {"funct7": "0000000", "funct3": "010"},
    "sltu":  {"funct7": "0000000", "funct3": "011"},
    "xor":   {"funct7": "0000000", "funct3": "100"},
    "srl":   {"funct7": "0000000", "funct3": "101"},
    "sra":   {"funct7": "0100000", "funct3": "101"},
    "or":    {"funct7": "0000000", "funct3": "110"},
    "and":   {"funct7": "0000000", "funct3": "111"},
    "mul":   {"funct7":"0000001","funct3":"000"},
    "div":   {"funct7":"0000010","funct3":"100"},
    "rem":   {"funct7":"0000011","funct3":"100"},
    "mulh":  {"funct7":"0000100","funct3":"000"},
    "mulhsu":{"funct7":"0000101","funct3":"000"},
    "mulhu": {"funct7":"0000110","funct3":"000"},
    "divu":  {"funct7":"0000111","funct3":"100"},
    "remu":  {"funct7":"0001000","funct3":"100"}
}

i_type_instructions = {
    "addi":   {"funct3": "000"},
    "slti":   {"funct3": "010"},
    "sltiu":  {"funct3": "011"},
    "xori":   {"funct3": "100"},
    "ori":    {"funct3": "110"},
    "andi":   {"funct3": "111"},
    "lb":     {"funct3": "000"},
    "lh":     {"funct3": "001"},
    "lw":     {"funct3": "010"},
    "lbu":    {"funct3": "100"},
    "lhu":    {"funct3": "101"}
}

s_type_instructions = {
    "sb":   {"funct3": "000"},
    "sh":   {"funct3": "001"},
    "sw":   {"funct3": "010"},
    "sd":   {"funct3": "011"}
}

b_type_instructions = {
    "beq":   {"funct3": "000"},
    "bne":   {"funct3": "001"},
    "blt":   {"funct3": "100"},
    "bge":   {"funct3": "101"},
    "bltu":  {"funct3": "110"},
    "bgeu":  {"funct3": "111"}
}

m_type_instructions = {
    "mul":   {"funct3": "000"},
    "mulh":   {"funct3": "001"},
    "mulhsu":   {"funct3": "010"},
    "mulhu":   {"funct3": "011"},
    "div":  {"funct3": "100"},
    "divu":  {"funct3": "101"},
    "rem":  {"funct3": "110"},
    "remu":  {"funct3": "111"}
}

si_type_instructions = {
    "slli":   {"funct3": "001", "code": "0000000"},
    "srli":   {"funct3": "101", "code": "0000000"},
    "srai":   {"funct3": "101", "code": "0100000"}
}


registers_code = {f"x{i}": get_last_N_bits(i, 5) for i in range(32)}

r_type_command = "add, sub, sll, slt, sltu, xor, srl, sra, or, and".split(", ")
i_type_command = "addi, slti, sltiu, xori, ori, andi, lb, lh, lw, lbu, lhu".split(", ")
s_type_command = "sb, sh, sw".split(", ")
b_type_command = "beq, bne, blt, bge, bltu, bgeu".split(", ")
u_type_command = "lui, auipc".split(", ")
j_type_command = "jal, jalr".split(", ")
m_type_command = "mul, mulh, mulhsu, mulhu, div, divu, rem, remu".split(", ")
si_type_command = "slli, srli, srai".split(", ")
