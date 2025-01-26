from Cache import LruCache, BitpLruCache
from functions import *
from setting import *




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
            text = file.read()
            lines = clean_text(text).split("\n")
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
        pass

    def execute(self):

        self.pc = 0x10000

        while True:

            self.correct_memory_address(self.pc)
            data = self.memory.get(self.pc)

            if data is None or data[1] != "instruction" or self.registers["x1"] == self.pc:
                return self.lru_cache.get_info(), self.bitp_lru_cache.get_info()

            self.lru_cache.add(self.pc, "inst")
            self.bitp_lru_cache.add(self.pc, "inst")

            instruction = data[0]


            self.parse_and_execute(instruction)
        
            self.pc += 4


    def parse_and_execute(self, instruction: str):
        if instruction in ["ecall", "ebreak", "fence.tso"]:
            return

        opcode, parts = instruction.split(" ", 1)

        if opcode == "fence":
            return

        parts = parts.split(",")
        parts = [None] + [part.strip(" ") for part in parts]

        parts = [part if part not in REGISTERS_ALIASES else REGISTERS_ALIASES[part] for part in parts]

        if opcode == "lui":
            rd, imm_str = parts[1], parts[2]
            imm = to_int32(imm_str)
            self.registers[rd] = imm << 12

        elif opcode == "auipc":
            rd, imm_str = parts[1], parts[2]
            imm = to_int32(imm_str)
            self.registers[rd] = to_int32((self.pc + (imm << 12)) & 0xFFFFFFFF)

        elif opcode == "jal":
            rd, offset_str = parts[1], parts[2]
            offset = to_int32(offset_str)
            self.registers[rd] = self.pc + 4
            self.pc += offset - 4

        elif opcode == "jalr":
            rd, rs1, offset_str = parts[1], parts[2], parts[3]

            offset = extract_sign_extend_12_bits(to_int32(offset_str))

            self.registers[rd] = self.pc + 4
            self.pc = (self.registers[rs1] + offset) & ~1

        elif opcode == "beq":
            rs1, rs2, offset_str = parts[1], parts[2], parts[3]

            offset = extract_sign_extend_13_bits(to_int32(offset_str))
            
            if self.registers[rs1] == self.registers[rs2]:
                self.pc += offset - 4

        elif opcode == "bne":
            rs1, rs2, offset_str = parts[1], parts[2], parts[3]
            
            offset = extract_sign_extend_13_bits(to_int32(offset_str))

            if self.registers[rs1] != self.registers[rs2]:
                self.pc += offset - 4

        elif opcode == "blt":
            rs1, rs2, offset_str = parts[1], parts[2], parts[3]
            
            offset = extract_sign_extend_13_bits(to_int32(offset_str))

            if self.registers[rs1] < self.registers[rs2]:
                self.pc += offset - 4

        elif opcode == "bge":
            rs1, rs2, offset_str = parts[1], parts[2], parts[3]
            
            offset = extract_sign_extend_13_bits(to_int32(offset_str))

            if self.registers[rs1] >= self.registers[rs2]:
                self.pc += offset - 4

        elif opcode == "bltu":
            rs1, rs2, offset_str = parts[1], parts[2], parts[3]
            
            offset = extract_sign_extend_13_bits(to_int32(offset_str))

            if self.registers[rs1] < self.registers[rs2]:
                self.pc += offset - 4

        elif opcode == "bgeu":
            rs1, rs2, offset_str = parts[1], parts[2], parts[3]

            offset = extract_sign_extend_13_bits(to_int32(offset_str))

            if self.registers[rs1] >= self.registers[rs2]:
                self.pc += offset - 4

        elif opcode == "lh":
            rd, offset,  rs1  = parts[1], to_int32(parts[2]), parts[3]
            address = self.registers[rs1] + extract_sign_extend_12_bits(offset)

            self.lru_cache.add(address, "mem")
            self.bitp_lru_cache.add(address, "mem")
            # self.registers[rd] = 0

        elif opcode == "lw":
            rd, offset, rs1  = parts[1], to_int32(parts[2]), parts[3]
            address = self.registers[rs1] + extract_sign_extend_12_bits(offset)

            self.lru_cache.add(address, "mem")
            self.bitp_lru_cache.add(address, "mem")
            # self.registers[rd] = 0

        elif opcode == "lb":
            rd, offset, rs1  = parts[1], to_int32(parts[2]), parts[3]
            address = self.registers[rs1] + extract_sign_extend_12_bits(offset)
            self.lru_cache.add(address, "mem")
            self.bitp_lru_cache.add(address, "mem")
            # self.registers[rd] = 0


        elif opcode == "lbu":
            rd, offset, rs1 = parts[1], to_int32(parts[2]), parts[3]
            address = self.registers[rs1] + extract_sign_extend_12_bits(offset)
            self.lru_cache.add(address, "mem")
            self.bitp_lru_cache.add(address, "mem")
            # self.registers[rd] = 0

        elif opcode == "lhu":
            rd, offset, rs1 = parts[1], to_int32(parts[2]), parts[3]
            address = self.registers[rs1] + extract_sign_extend_12_bits(offset)

            self.lru_cache.add(address, "mem")
            self.bitp_lru_cache.add(address, "mem")
            # self.registers[rd] = 0


        elif opcode == "sw":
            rd, offset, rs1 = parts[1], to_int32(parts[2]), parts[3]
            address = self.registers[rs1] + extract_sign_extend_12_bits(offset)


            self.lru_cache.add(address, "mem")
            self.bitp_lru_cache.add(address, "mem")
            # self.memory[address] = (self.registers[rd], "data")


        elif opcode == "sb":
            rd, offset, rs1  = parts[1], to_int32(parts[2]), parts[3]
            address = self.registers[rs1] + extract_sign_extend_12_bits(offset)

            self.lru_cache.add(address, "mem")
            self.bitp_lru_cache.add(address, "mem")            
            # self.memory[address] = (self.registers[rd] & 0xFF, "data")

        elif opcode == "sh":
            rd, offset, rs1 = parts[1], to_int32(parts[2]), parts[3]
            address = self.registers[rs1] + extract_sign_extend_12_bits(offset)

            self.lru_cache.add(address, "mem")
            self.bitp_lru_cache.add(address, "mem")
            # self.memory[address] = (self.registers[rd] & 0xFF, "data")

        elif opcode == "addi":
            rd, rs1, imm = parts[1], parts[2], parts[3]
            imm = extract_sign_extend_12_bits(to_int32(imm))
            self.registers[rd] = to_int32(self.registers[rs1] + imm)

        elif opcode == "slti":
            rd, rs1, imm = parts[1], parts[2], parts[3]
            imm = extract_sign_extend_12_bits(to_int32(imm))
            self.registers[rd] = to_int32(self.registers[rs1] < imm)

        elif opcode == "sltiu":
            rd, rs1, imm = parts[1], parts[2], parts[3]
            imm = extract_sign_extend_12_bits(to_int32(imm))
            self.registers[rd] = to_int32((self.registers[rs1] & 0xFFFFFFFF) < imm)
        
        elif opcode == "xori":
            rd, rs1, imm = parts[1], parts[2], parts[3]
            imm = extract_sign_extend_12_bits(to_int32(imm))
            self.registers[rd] = self.registers[rs1] ^ imm
                
        elif opcode == "ori":
            rd, rs1, imm = parts[1], parts[2], parts[3]
            imm = extract_sign_extend_12_bits(to_int32(imm))
            self.registers[rd] = self.registers[rs1] | imm
                
        elif opcode == "andi":
            rd, rs1, imm = parts[1], parts[2], parts[3]
            imm = extract_sign_extend_12_bits(to_int32(imm))
            self.registers[rd] = self.registers[rs1] & imm
                
        elif opcode == "slli":
            rd, rs1, shift_str = parts[1], parts[2], parts[3]
            shift = to_int32(shift_str) & 0b11111
            
            self.registers[rd] = to_int32(self.registers[rs1] << shift)
                
        elif opcode == "srli":
            rd, rs1, shift_str = parts[1], parts[2], parts[3]
            shift = to_int32(shift_str) & 0b11111
            self.registers[rd] = (self.registers[rs1] & 0xFFFFFFFF) >> shift

        elif opcode == "srai":
            rd, rs1, shift_str = parts[1], parts[2], parts[3]
            shift = to_int32(shift_str) & 0b11111
            sign = (self.registers[rs1] & 0x80000000) >> 31
            self.registers[rd] = to_int32(((self.registers[rs1] & 0xFFFFFFFF) >> shift) | \
                                ((((1 << shift) - 1) * sign) << (32 - shift)))
        
        elif opcode == "add":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            self.registers[rd] = to_int32(self.registers[rs1] + self.registers[rs2])
                
        elif opcode == "sub":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            self.registers[rd] = to_int32(self.registers[rs1] - self.registers[rs2])
                
        elif opcode == "sll":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            shift = self.registers[rs2] & 0x1F
            self.registers[rd] = to_int32(self.registers[rs1] << shift)
                
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
            self.registers[rd] = to_int32((self.registers[rs1] & 0xFFFFFFFF) >> shift)
                
        elif opcode == "sra":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            shift = self.registers[rs2] & 0x1F
            sign = (self.registers[rs1] & 0x80000000) >> 31
            self.registers[rd] = to_int32(((self.registers[rs1] & 0xFFFFFFFF) >> shift) | 
                                          ((((1 << shift) - 1) * sign) << (32 - shift)))
                
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
            self.registers[rd] = to_int32((result >> 32) & 0xFFFFFFFF)

        elif opcode == "mulhsu":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            result = self.registers[rs1] * (self.registers[rs2] & 0xFFFFFFFF)
            self.registers[rd] = to_int32((result >> 32) & 0xFFFFFFFF)

        elif opcode == "mulhu":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            result = (self.registers[rs1] & 0xFFFFFFFF) * (self.registers[rs2] & 0xFFFFFFFF)
            self.registers[rd] = to_int32((result >> 32) & 0xFFFFFFFF)

        elif opcode == "div":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            if self.registers[rs2] == 0:
                self.registers[rd] = -1
            else:
                sign = 1 if self.registers[rs1] * self.registers[rs2] >= 0 else -1
                self.registers[rd] = to_int32(sign * (abs(self.registers[rs1]) // abs(self.registers[rs2])))

        elif opcode == "divu":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            if self.registers[rs2] == 0:
                self.registers[rd] = -1
            else:
                self.registers[rd] = (self.registers[rs1] & 0xFFFFFFFF) // (self.registers[rs2] & 0xFFFFFFFF)

        elif opcode == "rem":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            if self.registers[rs2] == 0:
                self.registers[rd] = self.registers[rs1]
            else:
                a = self.registers[rs1]
                b = self.registers[rs2]
                
                result = a % b
                if (a < 0 and result > 0) or (a > 0 and result < 0):
                    result -= b
                
                self.registers[rd] = result
                
        elif opcode == "remu":
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            if self.registers[rs2] == 0:
                self.registers[rd] = self.registers[rs1]
            else:
                self.registers[rd] = to_int32((self.registers[rs1] & 0xFFFFFFFF) % (self.registers[rs2] & 0xFFFFFFFF))
            
        else:
            return

        self.registers["x0"] = 0
