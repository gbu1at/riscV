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
        assert(MEM_SIZE > address and address >= 0)

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

        opcode, parts = instruction.split(" ", 1)

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
            self.registers[rd] = (self.pc + (imm << 12)) & 0xFFFFFFFF

        elif opcode == "jal":
            rd, offset_str = parts[1], parts[2]
            offset = to_int32(offset_str)
            self.registers[rd] = self.pc + 4
            self.pc += offset - 4

        elif opcode == "jalr":
            rd, rs1, offset_str = parts[1], parts[2], parts[3]
            offset = to_int32(offset_str)
            self.registers[rd] = self.pc + 4
            self.pc = (self.registers[rs1] + offset) & ~1

        elif opcode == "beq":
            rs1, rs2, offset_str = parts[1], parts[2], parts[3]
            offset = to_int32(offset_str)
            if self.registers[rs1] == self.registers[rs2]:
                self.pc += offset - 4

        elif opcode == "bne":
            rs1, rs2, offset_str = parts[1], parts[2], parts[3]
            
            offset = to_int32(offset_str)

            if self.registers[rs1] != self.registers[rs2]:
                self.pc += offset - 4

        elif opcode == "blt":
            rs1, rs2, offset_str = parts[1], parts[2], parts[3]
            
            offset = to_int32(offset_str)

            if self.registers[rs1] < self.registers[rs2]:
                self.pc += offset - 4

        elif opcode == "bge":
            rs1, rs2, offset_str = parts[1], parts[2], parts[3]
            
            offset = to_int32(offset_str)

            if self.registers[rs1] >= self.registers[rs2]:
                self.pc += offset - 4

        elif opcode == "bltu":
            rs1, rs2, offset_str = parts[1], parts[2], parts[3]
            
            offset = to_int32(offset_str)

            if self.registers[rs1] < self.registers[rs2]:
                self.pc += offset - 4

        elif opcode == "bgeu":
            rs1, rs2, offset_str = parts[1], parts[2], parts[3]

            offset = to_int32(offset_str)

            if self.registers[rs1] >= self.registers[rs2]:
                self.pc += offset - 4





        elif opcode == "lh":
            rd, offset,  rs1  = parts[1], to_int32(parts[2]), parts[3]
            address = self.registers[rs1] + offset

            self.correct_memory_address(address)

            cell = self.memory.get(address)
            if cell is None or cell[1] != "mem":
                self.registers[rd] = 0

                self.lru_cache.add(address, "mem")
                self.bitp_lru_cache.add(address, "mem")
            else: assert(False)

        elif opcode == "lw":
            rd, offset, rs1  = parts[1], to_int32(parts[2]), parts[3]
            address = self.registers[rs1] + offset

            self.correct_memory_address(address)

            cell = self.memory.get(address)
            if cell is None or cell[1] != "mem":
                self.lru_cache.add(address, "mem")
                self.bitp_lru_cache.add(address, "mem")
                self.registers[rd] = 0
            else: assert(False)

        elif opcode == "lb":
            rd, offset, rs1  = parts[1], to_int32(parts[2]), parts[3]
            address = self.registers[rs1] + offset

            self.correct_memory_address(address)

            cell = self.memory.get(address)
            if cell is None or cell[1] != "mem":
                self.registers[rd] = 0
                self.lru_cache.add(address, "mem")
                self.bitp_lru_cache.add(address, "mem")
            else: assert(False)



        elif opcode == "lbu":
            rd, offset, rs1 = parts[1], to_int32(parts[2]), parts[3]
            address = self.registers[rs1] + offset

            self.correct_memory_address(address)

            cell = self.memory.get(address)
            if cell is None or cell[1] != "mem":
                self.registers[rd] = 0
                self.lru_cache.add(address, "mem")
                self.bitp_lru_cache.add(address, "mem")
            else: assert(False)

        elif opcode == "lhu":
            rd, offset, rs1 = parts[1], to_int32(parts[2]), parts[3]
            address = self.registers[rs1] + offset

            self.correct_memory_address(address)

            cell = self.memory.get(address)
            if cell is None or cell[1] != "mem":
                self.registers[rd] = 0
                self.lru_cache.add(address, "mem")
                self.bitp_lru_cache.add(address, "mem")
            else: assert(False)


        elif opcode == "sw":
            rd, offset, rs1 = parts[1], to_int32(parts[2]), parts[3]
            address = self.registers[rs1] + offset



            self.correct_memory_address(address)



            cell = self.memory.get(address)
            if cell is None or cell[1] != "mem":
                self.memory[address] = (self.registers[rd], "data")
                self.lru_cache.add(address, "mem")
                self.bitp_lru_cache.add(address, "mem")
            else: assert(False)

        elif opcode == "sb":
            rd, offset, rs1  = parts[1], to_int32(parts[2]), parts[3]
            address = self.registers[rs1] + offset

            self.correct_memory_address(address)

            cell = self.memory.get(address)
            if cell is None or cell[1] != "mem":
                self.memory[address] = (self.registers[rd] & 0xFF, "data")
                self.lru_cache.add(address, "mem")
                self.bitp_lru_cache.add(address, "mem")
            else: assert(False)

        elif opcode == "sh":
            rd, offset, rs1 = parts[1], to_int32(parts[2]), parts[3]

            address = self.registers[rs1] + offset
            self.correct_memory_address(address)

            cell = self.memory.get(address)
            if cell is None or cell[1] != "instruction":
                self.memory[address] = (self.registers[rd] & 0xFF, "data")
                self.lru_cache.add(address, "mem")
                self.bitp_lru_cache.add(address, "mem")
            else: assert(False)

        elif opcode == "addi":
            rd, rs1, imm = parts[1], parts[2], parts[3]
            imm = to_int32(imm)
            self.registers[rd] = to_int32(self.registers[rs1] + imm)

        elif opcode == "slti":
            rd, rs1, imm = parts[1], parts[2], parts[3]
            imm = to_int32(imm)
            self.registers[rd] = to_int32(self.registers[rs1] < imm)

        elif opcode == "sltiu":
            rd, rs1, imm = parts[1], parts[2], parts[3]
            imm = to_int32(imm) | 0xFFFFF000
            self.registers[rd] = to_int32((self.registers[rs1] & 0xFFFFFFFF) < imm)
        
        elif opcode == "xori":
            rd, rs1, imm = parts[1], parts[2], parts[3]
            imm = to_int32(imm)
            self.registers[rd] = self.registers[rs1] ^ imm
                
        elif opcode == "ori":
            rd, rs1, imm = parts[1], parts[2], parts[3]
            imm = to_int32(imm)
            self.registers[rd] = self.registers[rs1] | imm
                
        elif opcode == "andi":
            rd, rs1, imm = parts[1], parts[2], parts[3]
            imm = to_int32(imm)
            self.registers[rd] = self.registers[rs1] & imm
                
        elif opcode == "slli":
            rd, rs1, shift_str = parts[1], parts[2], parts[3]
            shift = to_int32(shift_str) & 0b11111
            
            self.registers[rd] = self.registers[rs1] << shift
                
        elif opcode == "srli":
            rd, rs1, shift_str = parts[1], parts[2], parts[3]
            shift = to_int32(shift_str) & 0b11111
            self.registers[rd] = (self.registers[rs1] & 0xFFFFFFFF) >> shift

                
        elif opcode == "srai":
            rd, rs1, shift_str = parts[1], parts[2], parts[3]
            shift = to_int32(shift_str) & 0b11111
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
                self.registers[rd] = to_int32(self.registers[rs1] / self.registers[rs2])

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
                self.registers[rd] = to_int32(self.registers[rs1] % self.registers[rs2])

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
