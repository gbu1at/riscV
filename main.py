import sys


ADDR_LEN = 18 # длина адреса (в битах)
CACHE_INDEX_LEN = 3 # длина индекса блока кэш-линий  (в битах)
CACHE_LINE_SIZE = 64 # размер кэш-линии (в байтах)
CACHE_LINE_COUNT = 32 # кол-во кэш-линий

MEM_SIZE = 2 ** ADDR_LEN # размер памяти (в байтах)
CACHE_SIZE = CACHE_LINE_SIZE * CACHE_LINE_COUNT # размер кэша, без учёта служебной информации (в байтах)

CACHE_SETS = 2 ** CACHE_INDEX_LEN  # кол-во блоков кэш-линий
CACHE_WAY = CACHE_LINE_COUNT // CACHE_SETS # ассоциативность


# CACHE_TAG_LEN = 7 # длина тэга адреса (в битах)
# CACHE_OFFSET_LEN – длина смещения внутри кэш-линии (в битах)


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
        self.access_order = []

    def add(self, address):
        if address in self.lru_cache:
            self.access_order.remove(address)
            self.access_order.append(address)
            return True
        else:
            if len(self.lru_cache) >= self.size:
                lru = self.access_order.pop(0)
                del self.lru_cache[lru]
            self.lru_cache[address] = True
            self.access_order.append(address)
            return False

class BitpLruCacheLine:
    def __init__(self, size):
        self.size = size
        self.mru = {}
        self.access_order = []
    
    def add(self, address):
        if address in self.mru:
            self.access_order.remove(address)
            self.access_order.append(address)
            return True
        elif address in self.access_order:
            self.access_order.remove(address)
            self.access_order.append(address)
            if len(self.mru) == self.size - 1:
                self.mru = {}
            self.mru[address] = True
            return True
        else:
            if len(self.mru) == self.size - 1:
                self.mru = {}
            self.mru[address] = True

            if len(self.access_order) < self.size:
                self.access_order.append(address)
            else:
                for add in self.access_order:
                    if add not in self.mru:
                        self.access_order.remove(add)
                        break
                self.access_order.append(address)
            return False

class Cache:
    def __init__(self, CacheLine) -> None:
        self.caches = [CacheLine(CACHE_WAY) for i in range(CACHE_SETS)]
        self.cache_hit_instruction = 0
        self.cache_total_instruction = 0

        self.cache_hit_memory = 0
        self.cache_total_memory = 0
    
    def add(self, address: int, type="inst") -> bool:

        address = address - address % CACHE_LINE_SIZE

        idx_adrress = (address // CACHE_LINE_SIZE) % CACHE_SETS

        
        val = self.caches[idx_adrress].add(address)

        if type == "inst":
            self.cache_total_instruction += 1
            if val:
                self.cache_hit_instruction += 1
        elif type == "mem":
            self.cache_total_memory += 1
            if val:
                self.cache_hit_memory += 1
        else: assert(False)

        return val
    
    def get_info(self):

        cache_total = self.cache_total_memory + self.cache_total_instruction
        cache_hit = self.cache_hit_instruction + self.cache_hit_memory

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

class RiscVSimulator:
    def __init__(self):
        self.registers = {}

        self.registers_aliases = {
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
            "t6": "x31"
        }

        for i in range(32):
            self.registers_aliases[f"x{i}"] = f"x{i}"
            self.registers[f"x{i}"] = 0

        self.memory = {}
        self.pc = 0x10000
        self.lru_cache = LruCache()
        self.bitp_lru_cache = BitpLruCache()

        self.memory_limit = False

    def load_instructions(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.strip():
                    instruction = line.strip()
                    address = self.pc
                    self.memory[address] = (instruction, "instruction")
                    self.pc += 4
    
    def correct_memory_address(self, address):
        # print(address, MEM_SIZE)
        assert(MEM_SIZE > address and address >= 0)
        # pass

    def execute(self):
        self.pc = 0x10000
        while True:

            self.correct_memory_address(self.pc)

            self.lru_cache.add(self.pc, "inst")
            self.bitp_lru_cache.add(self.pc, "inst")

            data = self.memory.get(self.pc)
            if data is None or data[1] != "instruction":
                return self.lru_cache.get_info(), self.bitp_lru_cache.get_info()


            instruction = data[0]

            self.parse_and_execute(instruction)
            self.pc += 4


    def parse_and_execute(self, instruction: str):
        # print(instruction)
        if instruction in ["ecall", "ebreak"]:
            return
        opcode, parts = instruction.split(" ", 1)

        parts = parts.split(",")
        parts = [None] + [part.strip(" ") for part in parts]

        parts = [part if part not in self.registers_aliases else self.registers_aliases[part] for part in parts]

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
                if cell is None:
                    self.registers[rd] = 8736548
                else:
                    b = cell[0].to_bytes(2, byteorder='little', signed=True)
                    self.registers[rd] = int.from_bytes(b, byteorder='little', signed=True)
                self.lru_cache.add(address, "mem")
                self.bitp_lru_cache.add(address, "mem")
            else: assert(False)

        elif opcode == "lw":
            rd, rs1, offset = parts[1], parts[2], int(parts[3])
            address = self.registers[rs1] + offset

            self.correct_memory_address(address)

            cell = self.memory.get(address)
            if cell is None or cell[1] != "mem":
                self.registers[rd] = 8736548 if cell is None else cell[0]
                self.lru_cache.add(address, "mem")
                self.bitp_lru_cache.add(address, "mem")
            else: assert(False)

        elif opcode == "lb":
            rd, rs1, offset = parts[1], parts[2], int(parts[3])
            address = self.registers[rs1] + offset

            self.correct_memory_address(address)

            cell = self.memory.get(address)
            if cell is None or cell[1] != "mem":
                if cell is None:
                    self.registers[rd] = 0
                else:
                    # print(cell[0])
                    extned = 0xFFFFFFF0 if cell[0] < 0 else 0
                    b = (cell[0] & 0xF) | extned

                    # print(b)
                    self.registers[rd] = b
                self.lru_cache.add(address, "mem")
                self.bitp_lru_cache.add(address, "mem")
            else: assert(False)



        elif opcode == "lbu":
            rd, rs1, offset = parts[1], parts[2], int(parts[3])
            address = self.registers[rs1] + offset

            self.correct_memory_address(address)

            cell = self.memory.get(address)
            if cell is None or cell[1] != "mem":
                if cell is None:
                    self.registers[rd] = 0
                else:
                    b = cell[0].to_bytes(1, byteorder='little', signed=False)
                    self.registers[rd] = int.from_bytes(b, byteorder='little', signed=False)
                self.lru_cache.add(address, "mem")
                self.bitp_lru_cache.add(address, "mem")
            else: assert(False)

        elif opcode == "lhu":
            rd, rs1, offset = parts[1], parts[2], int(parts[3])
            address = self.registers[rs1] + offset

            self.correct_memory_address(address)

            cell = self.memory.get(address)
            if cell is None or cell[1] != "mem":
                if cell is None:
                    self.registers[rd] = 8736548
                else:
                    b = cell[0].to_bytes(2, byteorder='little', signed=False)
                    self.registers[rd] = int.from_bytes(b, byteorder='little', signed=False)
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
            rd, rs1, offset = parts[1], parts[2], int(parts[3])
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
            rd, rs1, offset = parts[1], parts[2], int(parts[3])
            address = self.registers[rs1] + offset

            self.correct_memory_address(address)

            cell = self.memory.get(address)
            if cell is None or cell[1] != "mem":
                self.memory[address] = (self.registers[rd] & 0xFF, "data")
                self.lru_cache.add(address, "mem")
                self.bitp_lru_cache.add(address, "mem")
            else: assert(False)

        elif opcode == "sh":
            rd, rs1, offset = parts[1], parts[2], int(parts[3])

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

if __name__ == "__main__":
    machine = RiscVSimulator()
    _, flag, filename = sys.argv
    if (flag == "b"):
        machine.load_instructions(f"test_asm/{filename}.asm")
        lru_arg, bitplru_arg = machine.execute()
        arg = lru_arg + bitplru_arg
        fmt_0 = "replacement\thit rate\thit rate (inst)\thit rate (data)\n"
        fmt_1 = "        LRU\t%3.5f%%\t%3.5f%%\t%3.5f%%\n"
        fmt_2 = "       pLRU\t%3.5f%%\t%3.5f%%\t%3.5f%%\n"
        fmt =  fmt_0 + fmt_1 + fmt_2
        
        
        result = fmt % arg

        with open(f"out_cache_info/{filename}.out", "w") as f:
            f.write(result)
    else:
        machine.load_instructions(filename)
        lru_arg, bitplru_arg = machine.execute()
        arg = lru_arg + bitplru_arg
        fmt_0 = "replacement\thit rate\thit rate (inst)\thit rate (data)\n"
        fmt_1 = "        LRU\t%3.5f%%\t%3.5f%%\t%3.5f%%\n"
        fmt_2 = "       pLRU\t%3.5f%%\t%3.5f%%\t%3.5f%%\n"
        fmt =  fmt_0 + fmt_1 + fmt_2
        
        
        result = fmt % arg
        print(result)
