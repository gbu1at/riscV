import sys

lenCache = 64 
memsize = 2 ** 18 
kolcacheline = 8 

def printf(fmt, *args):
    sys.stdout.write(fmt % args)


def to_int32(x: int):
    x %= 2 ** 32
    if x >= 2 ** 31:
        x = x - 2 ** 32
    return x


class LruCacheLine:
    def __init__(self, size):
        self.size = size
        self.lru_cache = {}
        self.cachearray = []

    def add(self, address):
        if address in self.lru_cache:
            self.cachearray.remove(address)
            self.cachearray.append(address)
            return True
        else:
            if len(self.lru_cache) >= self.size:
                lru = self.cachearray.pop(0)
                del self.lru_cache[lru]
            self.lru_cache[address] = True
            self.cachearray.append(address)
            return False

class BitpLruCacheLine:
    def __init__(self, size):
        

        self.size = size
        self.mru = {}
        self.cachearray = []
    
    def add(self, address):
        if address in self.mru:
            return True
        elif address in self.cachearray:
            if len(self.mru) == self.size - 1:
                self.mru = {}
            self.mru[address] = True
            return True
        else:
            if len(self.cachearray) < self.size:
                self.cachearray.append(address)
            else:
                for i, add in enumerate(self.cachearray):
                    if add not in self.mru:
                        self.cachearray[i] = address
                        break
            
            if len(self.mru) == self.size - 1:
                self.mru = {}
            self.mru[address] = True
            
            return False

class Cache:
    def __init__(self, CacheLine) -> None:
        self.caches = [CacheLine(4) for i in range(kolcacheline)]
        self.cache_hit_instruction = 0
        self.cache_total_instruction = 0

        self.cache_hit_memory = 0
        self.cache_total_memory = 0
    
    def add(self, address: int, type="inst") -> bool:

        tag_address = address - address % lenCache

        idx_adrress = (tag_address // lenCache) % kolcacheline

        hit = self.caches[idx_adrress].add(tag_address)

        if type == "inst":
            self.cache_total_instruction += 1
            if hit:
                self.cache_hit_instruction += 1
        elif type == "mem":
            self.cache_total_memory += 1
            if hit:
                self.cache_hit_memory += 1
        else: assert(False)

        return hit
    
    def get_info(self):

        cache_total = self.cache_total_memory + self.cache_total_instruction
        cache_hit = self.cache_hit_instruction + self.cache_hit_memory

        # print(self.cache_hit_instruction, self.cache_total_instruction)

        all_percent = 100 * cache_hit / cache_total
        instruction_percent = 100 * self.cache_hit_instruction / self.cache_total_instruction
        memory_percent = float("nan") if self.cache_total_memory == 0 else 100 * self.cache_hit_memory / self.cache_total_memory

        return all_percent, instruction_percent, memory_percent


class LruCache(Cache):
    def __init__(self) -> None:
        super().__init__(LruCacheLine)


class BitpLruCache(Cache):
    def __init__(self) -> None:
        super().__init__(BitpLruCacheLine)


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


class RiscVSimulator:
    def __init__(self):
        self.registers = {}

        for i in range(32):
            self.registers[f"x{i}"] = 0

        self.memory = {}
        self.pc = 0x10000
        self.lru_cache = LruCache()
        self.bitp_lru_cache = BitpLruCache()

        self.memory_limit = False

    def load_instructions(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            instructions = []
            for line in lines:
                if line.strip():
                    instruction = line.strip()
                    instructions.append(instruction)
                    address = self.pc
                    self.memory[address] = (instruction, "instruction")
                    self.pc += 4
        return instructions
    
    def correct_memory_address(self, address):
        assert(memsize > address and address >= 0)

    def execute(self):
        self.pc = 0x10000
        while True:

            self.correct_memory_address(self.pc)


            data = self.memory.get(self.pc)
            if data is None or data[1] != "instruction":
                return self.lru_cache.get_info(), self.bitp_lru_cache.get_info()

            self.lru_cache.add(self.pc, "inst")
            self.bitp_lru_cache.add(self.pc, "inst")

            instruction = data[0]

            self.parse_and_execute(instruction)
            self.pc += 4


    def parse_and_execute(self, instruction: str):
        if instruction in ["ecall", "ebreak"]:
            return
        
        # print(instruction)
        # print(self.registers["x9"])

        opcode, parts = instruction.split(" ", 1)

        parts = parts.split(",")
        parts = [None] + [part.strip(" ") for part in parts]

        parts = [part if part not in REGISTERS_ALIASES else REGISTERS_ALIASES[part] for part in parts]

        if opcode == "lui":
            rd, imm_str = parts[1], parts[2]
            imm = int(imm_str)
            self.registers[rd] = imm << 12

        elif opcode == "auipc":
            rd, imm_str = parts[1], parts[2]
            imm = int(imm_str)
            self.registers[rd] = (self.pc + (imm << 12)) & 0xFFFFFFFF

        elif opcode == "jal":
            rd, offset_str = parts[1], parts[2]
            offset = int(offset_str) if not offset_str.startswith('0x') else int(offset_str, 16)
            self.registers[rd] = self.pc + 4
            self.pc += offset - 4


        elif opcode == "jalr":
            rd, rs1, offset_str = parts[1], parts[2], parts[3]
            offset = int(offset_str) if not offset_str.startswith('0x') else int(offset_str, 16)
            self.registers[rd] = self.pc + 4
            self.pc = (self.registers[rs1] + offset) & ~1


        elif opcode == "beq":
            rs1, rs2, offset_str = parts[1], parts[2], parts[3]
            offset = int(offset_str) if not offset_str.startswith('0x') else int(offset_str, 16)
            if self.registers[rs1] == self.registers[rs2]:
                self.pc += offset - 4


        elif opcode == "bne":
            rs1, rs2, offset_str = parts[1], parts[2], parts[3]
            
            offset = int(offset_str) if not offset_str.startswith('0x') else int(offset_str, 16)

            if self.registers[rs1] != self.registers[rs2]:
                self.pc += offset - 4

        elif opcode == "blt":
            rs1, rs2, offset_str = parts[1], parts[2], parts[3]
            
            offset = int(offset_str) if not offset_str.startswith('0x') else int(offset_str, 16)

            if self.registers[rs1] < self.registers[rs2]:
                self.pc += offset - 4

        elif opcode == "bge":
            rs1, rs2, offset_str = parts[1], parts[2], parts[3]
            
            offset = int(offset_str) if not offset_str.startswith('0x') else int(offset_str, 16)

            if self.registers[rs1] >= self.registers[rs2]:
                self.pc += offset - 4

        elif opcode == "bltu":
            rs1, rs2, offset_str = parts[1], parts[2], parts[3]
            
            offset = int(offset_str) if not offset_str.startswith('0x') else int(offset_str, 16)

            if self.registers[rs1] < self.registers[rs2]:
                self.pc += offset - 4

        elif opcode == "bgeu":
            rs1, rs2, offset_str = parts[1], parts[2], parts[3]

            offset = int(offset_str) if not offset_str.startswith('0x') else int(offset_str, 16)

            if self.registers[rs1] >= self.registers[rs2]:
                self.pc += offset - 4





        elif opcode == "lh":
            rd, rs1, offset = parts[1], parts[2], int(parts[3])
            address = self.registers[rs1] + offset

            self.correct_memory_address(address)

            cell = self.memory.get(address)
            if cell is None or cell[1] != "mem":
                # if cell is None:
                self.registers[rd] = 0
                # else:
                #     extned = 0xFFFF0000 if cell[0] < 0 else 0
                #     b = (cell[0] & 0xFFFF) | extned
                #     self.registers[rd] = b
                self.lru_cache.add(address, "mem")
                self.bitp_lru_cache.add(address, "mem")
            else: assert(False)

        elif opcode == "lw":
            rd, rs1, offset = parts[1], parts[2], int(parts[3])
            address = self.registers[rs1] + offset

            self.correct_memory_address(address)

            cell = self.memory.get(address)
            if cell is None or cell[1] != "mem":
                # self.registers[rd] = 0 if cell is None else cell[0]
                self.lru_cache.add(address, "mem")
                self.bitp_lru_cache.add(address, "mem")
                self.registers[rd] = 0
            else: assert(False)

        elif opcode == "lb":
            rd, rs1, offset = parts[1], parts[2], int(parts[3])
            address = self.registers[rs1] + offset

            self.correct_memory_address(address)

            cell = self.memory.get(address)
            if cell is None or cell[1] != "mem":
                # if cell is None:
                self.registers[rd] = 0
                # else:
                #     # print(cell[0])
                #     extned = 0xFFFFFFF0 if cell[0] < 0 else 0
                #     # print(cell[0] & 0x0000000F)
                #     b = (cell[0] & 0xF) | extned

                #     self.registers[rd] = b
                # print(machine.registers["x2"])
                self.lru_cache.add(address, "mem")
                self.bitp_lru_cache.add(address, "mem")
            else: assert(False)



        elif opcode == "lbu":
            rd, rs1, offset = parts[1], parts[2], int(parts[3])
            address = self.registers[rs1] + offset

            self.correct_memory_address(address)


            cell = self.memory.get(address)
            if cell is None or cell[1] != "mem":
                # if cell is None:
                self.registers[rd] = 0
                # else:
                #     b = cell[0].to_bytes(1, byteorder='little', signed=False)
                #     self.registers[rd] = int.from_bytes(b, byteorder='little', signed=False)
                self.lru_cache.add(address, "mem")
                self.bitp_lru_cache.add(address, "mem")
            else: assert(False)

        elif opcode == "lhu":
            rd, rs1, offset = parts[1], parts[2], int(parts[3])
            address = self.registers[rs1] + offset

            self.correct_memory_address(address)

            cell = self.memory.get(address)
            if cell is None or cell[1] != "mem":
                # if cell is None:
                self.registers[rd] = 0
                # else:
                #     b = cell[0].to_bytes(2, byteorder='little', signed=False)
                #     self.registers[rd] = int.from_bytes(b, byteorder='little', signed=False)
                self.lru_cache.add(address, "mem")
                self.bitp_lru_cache.add(address, "mem")
            else: assert(False)


        # elif opcode == "sb":
        #     rd, rs1, offset = parts[1], parts[2], int(parts[3])
        #     address = self.registers[rs1] + offset
        #     cell = self.memory.get(address)
        #     if cell is None or cell[1] != "instruction":
        #         self.memory[address] = (self.registers[rd] & 0xFF, "data")
        #         if self.lru_cache.add(address):
        #             self.lru_cache_hit_memory += 1
        #         else:
        #             self.lru_cache_miss_memory += 1
        #     else: assert(False)

        elif opcode == "sw":
            rd, offset, rs1 = parts[1], int(parts[2]), parts[3]
            address = self.registers[rs1] + offset

            # print("sw", self.registers[rs1])


            self.correct_memory_address(address)



            cell = self.memory.get(address)
            if cell is None or cell[1] != "mem":
                self.memory[address] = (self.registers[rd], "data")
                self.lru_cache.add(address, "mem")
                self.bitp_lru_cache.add(address, "mem")
            else: assert(False)

        elif opcode == "sb":
            rd, offset, rs1  = parts[1], int(parts[2]), parts[3]
            address = self.registers[rs1] + offset

            self.correct_memory_address(address)

            cell = self.memory.get(address)
            if cell is None or cell[1] != "mem":
                self.memory[address] = (self.registers[rd] & 0xFF, "data")
                self.lru_cache.add(address, "mem")
                self.bitp_lru_cache.add(address, "mem")
            else: assert(False)

        elif opcode == "sh":
            rd, offset, rs1 = parts[1], int(parts[2]), parts[3]

            # print(offset)
            address = self.registers[rs1] + offset

            # print(address)
            self.correct_memory_address(address)

            cell = self.memory.get(address)
            if cell is None or cell[1] != "instruction":
                self.memory[address] = (self.registers[rd] & 0xFF, "data")
                self.lru_cache.add(address, "mem")
                self.bitp_lru_cache.add(address, "mem")
            else: assert(False)

        elif opcode == "addi":
            rd, rs1, imm = parts[1], parts[2], parts[3]
            imm = int(imm)
            self.registers[rd] = to_int32(self.registers[rs1] + imm)

        elif opcode == "slti":
            rd, rs1, imm = parts[1], parts[2], parts[3]
            imm = int(imm)
            self.registers[rd] = int(self.registers[rs1] < imm)


        elif opcode == "sltiu":
            rd, rs1, imm = parts[1], parts[2], parts[3]
            imm = int(imm) | 0xFFFFF000
            self.registers[rd] = int((self.registers[rs1] & 0xFFFFFFFF) < imm)
        
        elif opcode == "xori":
            rd, rs1, imm = parts[1], parts[2], parts[3]
            imm = int(imm)
            self.registers[rd] = self.registers[rs1] ^ imm
                
        elif opcode == "ori":
            rd, rs1, imm = parts[1], parts[2], parts[3]
            imm = int(imm)
            self.registers[rd] = self.registers[rs1] | imm
                
        elif opcode == "andi":
            rd, rs1, imm = parts[1], parts[2], parts[3]
            imm = int(imm)
            self.registers[rd] = self.registers[rs1] & imm
                
        elif opcode == "slli":
            rd, rs1, shift_str = parts[1], parts[2], parts[3]
            shift = int(shift_str) & 0b11111
            
            self.registers[rd] = self.registers[rs1] << shift
                
        elif opcode == "srli":
            rd, rs1, shift_str = parts[1], parts[2], parts[3]
            shift = int(shift_str) & 0b11111
            self.registers[rd] = (self.registers[rs1] & 0xFFFFFFFF) >> shift
            # print(self.registers[rd])
                
        elif opcode == "srai":
            rd, rs1, shift_str = parts[1], parts[2], parts[3]
            shift = int(shift_str) & 0b11111
            self.registers[rd] = (self.registers[rs1] & 0xFFFFFFFF) >> shift
        
        elif opcode == "add":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            self.registers[rd] = to_int32(self.registers[rs1] + self.registers[rs2])
                
        elif opcode == "sub":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            self.registers[rd] = to_int32(self.registers[rs1] - self.registers[rs2])
                
        elif opcode == "sll":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            shift = self.registers[rs2] & 0x1F
            self.registers[rd] = self.registers[rs1] << shift
                
        elif opcode == "slt":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            self.registers[rd] = int(self.registers[rs1] < self.registers[rs2])
                
        elif opcode == "sltu":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            self.registers[rd] = int((self.registers[rs1] & 0xFFFFFFFF) < (self.registers[rs2] & 0xFFFFFFFF))
                
        elif opcode == "xor":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            self.registers[rd] = self.registers[rs1] ^ self.registers[rs2]
                
        elif opcode == "srl":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            shift = self.registers[rs2] & 0x1F
            self.registers[rd] = self.registers[rs1] >> shift
                
        elif opcode == "sra":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            shift = self.registers[rs2] & 0x1F
            self.registers[rd] = (self.registers[rs1] & 0xFFFFFFFF) >> shift
                
        elif opcode == "or":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            self.registers[rd] = self.registers[rs1] | self.registers[rs2]
                
        elif opcode == "and":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            self.registers[rd] = self.registers[rs1] & self.registers[rs2]
                
        elif opcode == "fence":
            pass
                
        elif opcode == "ecall":
            pass

        elif opcode == "ebreak":
            pass
        
        elif opcode == "mul":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            self.registers[rd] = to_int32(self.registers[rs1] * self.registers[rs2])
        
        elif opcode == "mulh":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            result = self.registers[rs1] * self.registers[rs2]
            self.registers[rd] = (result >> 32) & 0xFFFFFFFF


        elif opcode == "mulhsu":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            result = self.registers[rs1] * (self.registers[rs2] & 0xFFFFFFFF)
            self.registers[rd] = (result >> 32) & 0xFFFFFFFF

        elif opcode == "mulhu":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            result = (self.registers[rs1] & 0xFFFFFFFF) * (self.registers[rs2] & 0xFFFFFFFF)
            self.registers[rd] = (result >> 32) & 0xFFFFFFFF

        elif opcode == "div":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            if self.registers[rs2] == 0:
                self.registers[rd] = -1
            else:
                self.registers[rd] = int(self.registers[rs1] / self.registers[rs2])

        elif opcode == "divu":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            if self.registers[rs2] == 0:
                self.registers[rd] = -1
            else:
                self.registers[rd] = (self.registers[rs1] & 0xFFFFFFFF) // (self.registers[rs2] & 0xFFFFFFFF)

        elif opcode == "rem":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            if self.registers[rs2] == 0:
                self.registers[rd] = -1
            else:
                self.registers[rd] = int(self.registers[rs1] % self.registers[rs2])

        elif opcode == "remu":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            if self.registers[rs2] == 0:
                self.registers[rd] = -1
            else:
                self.registers[rd] = (self.registers[rs1] & 0xFFFFFFFF) % (self.registers[rs2] & 0xFFFFFFFF)
            
        else:
            print()
            print(opcode, "!!!")
            print()
            assert(False)

        self.registers["x0"] = 0


def get_last_N_bits(number, N):
    assert(N > 0)
    last_N_bits = int(number) & ((1 << N) - 1)
    binary_string = bin(last_N_bits)[2:]
    padded_bits = binary_string.zfill(N)
    return padded_bits

def get_segment_bits(number:str, l, r):
    assert(r > l)
    if number.startswith("0x"):
        number = int(number, 16)
    seg_bits = ((int(number) + 2 ** 33) & ((1 << r) - 1)) >> l
    binary_string = bin(seg_bits)[2:]
    padded_bits = binary_string.zfill(r - l)
    return padded_bits



instruction_opcode = {
    "add":  {"opcode": "0110011"},
    "addi": {"opcode": "0010011"},
    "sub":  {"opcode": "0110011"},

    "and":  {"opcode": "0110011"},
    "andi": {"opcode": "0b0010011"}, 
    "or":   {"opcode": "0b0110011"},  
    "ori":  {"opcode": "0b0010011"},
    "xor":  {"opcode": "0b0110011"},  
    "xori": {"opcode": "0b0010011"},

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

registers_code = {f"x{i}": get_last_N_bits(i, 5) for i in range(32)}

r_type_command = "add, sub, sll, slt, sltu, xor, srl, sra, or, and".split(", ")
i_type_command = "addi, slti, sltiu, xori, ori, andi, lb, lh, lw, lbu, lhu, slli, srli, srai".split(", ")
s_type_command = "sb, sh, sw".split(", ")
b_type_command = "beq, bne, blt, bge, bltu, bgeu".split(", ")
u_type_command = "lui, auipc".split(", ")
j_type_command = "jal, jalr".split(", ")


def reverse(s):
    return "".join(reversed(s))

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
    
    else:
        assert(False)

    return res



def binary_to_hex(binary_string):
    assert(len(binary_string) == 32)
    byte_array = reversed(bytearray(int(binary_string[i:i + 8], 2) for i in range(0, len(binary_string), 8)))
    hex_string = ' '.join(f"{byte:02X}" for byte in byte_array)
    return hex_string


if __name__ == "__mainrail__":
    machine = RiscVSimulator()
    _, *args = sys.argv
    

    filename = ""
    bin_filename = ""

    write_in_bin_file = False

    if len(args) == 2:
        if args[0] == "--asm":
            filename = args[1]
        else: assert(False)

    if len(args) == 4:
        if args[0] == "--asm" and args[2] == "--bin":
            filename = args[1]
            bin_filename = args[3]
            write_in_bin_file = True
        else: assert(False)


    instructions = machine.load_instructions(filename)

    lru_arg, bitplru_arg = machine.execute()
    arg = lru_arg + bitplru_arg
    fmt_0 = "replacement\thit rate\thit rate (inst)\thit rate (data)\n"
    fmt_1 = "        LRU\t%3.5f%%\t%3.5f%%\t%3.5f%%\n"
    fmt_2 = "       pLRU\t%3.5f%%\t%3.5f%%\t%3.5f%%\n"
    fmt =  fmt_0 + fmt_1 + fmt_2
    
    
    result = fmt % arg
    print(result)


    if write_in_bin_file:
        with open(bin_filename, "w") as file:
            for inst in instructions:
                inst_bin_str = encode_riscv_instruction(inst)
                inst_hex_str = binary_to_hex(inst_bin_str)
                file.write(inst_hex_str + "\n")
