import unittest
from main import RiscVSimulator, to_int32

class TestRiscVSimulator(unittest.TestCase):
    def setUp(self):
        ...

    def test_load_instructions(self):
        self.simulator = RiscVSimulator()

        instructions = [
            "addi a0, zero, 10",  # Загрузить 10 в a0
            "addi a1, zero, 20",  # Загрузить 20 в a1
            "add a2, a0, a1",      # a2 = a0 + a1 (10 + 20)
            "sub a3, a1, a0",      # a3 = a1 - a0 (20 - 10)
            "mul a4, a0, a1",      # a4 = a0 * a1 (10 * 20)
            "div a5, a1, a0",      # a5 = a1 / a0 (20 / 10)
            "rem a6, a1, a0"       # a6 = a1 % a0 (20 % 10)
        ]

        with open("test.asm", 'w') as f:
            for instruction in instructions:
                f.write(instruction + '\n')

        self.simulator.load_instructions("test.asm")


        self.simulator.execute()

        self.assertEqual(self.simulator.registers["a0"], 10)
        self.assertEqual(self.simulator.registers["a1"], 20)
        self.assertEqual(self.simulator.registers["a2"], 30)  # 10 + 20
        self.assertEqual(self.simulator.registers["a3"], 10)  # 20 - 10
        self.assertEqual(self.simulator.registers["a4"], 200) # 10 * 20
        self.assertEqual(self.simulator.registers["a5"], 2)   # 20 / 10
        self.assertEqual(self.simulator.registers["a6"], 0)   # 20 % 10

    def test_memory_operations(self):
        self.simulator = RiscVSimulator()

        instructions = [
            "addi t0, zero, 100",   # t0 = 100
            "sw t0, sp, 0",          # Сохранить байты из t0 по адресу sp
            "lw t1, sp, 0",          # Загрузить байты из адреса sp в t1
            "sw t1, sp, 4"           # Сохранить байты из t1 по адресу sp + 4
        ]

        with open("test.asm", 'w') as f:
            for instruction in instructions:
                f.write(instruction + '\n')

        self.simulator.load_instructions("test.asm")
        self.simulator.execute()

        self.assertEqual(self.simulator.memory[self.simulator.registers["sp"]], (100, "data"))
        self.assertEqual(self.simulator.memory[self.simulator.registers["sp"] + 4], (100, "data"))

    def test_arithmetic_operations(self):
        self.simulator = RiscVSimulator()

        instructions = [
            "addi t0, zero, -8",   # t0 = -8
            "srli t1, t0, 2",       # t1 = -8 >> 2 (логический сдвиг вправо)
            "srai t2, t0, 2",       # t2 = -8 >> 2 (арифметический сдвиг вправо)
            "slt t3, t0, t1",      # Проверка: t3 = (t0 < t1)
            "sltu t4, t1, t2"      # Беззнаковое сравнение: t4 = (t1 < t2)
        ]

        with open("test.asm", 'w') as f:
            for instruction in instructions:
                f.write(instruction + '\n')

        self.simulator.load_instructions("test.asm")
        self.simulator.execute()

        self.assertEqual(self.simulator.registers["t3"], int(-8 < (100 >> 2)))   # Проверка знакового сравнения
        self.assertEqual(self.simulator.registers["t4"], int((100 >> 2) < (-8 >> 2)))   # Проверка беззнакового сравнения
    
    def test_sum_array1(self):
        self.simulator = RiscVSimulator()
        self.simulator.load_instructions("test_asm/test_asm_sum_array/sum_array1.asm")
        self.simulator.execute()
        self.assertEqual(self.simulator.registers["s3"], sum([i for i in range(10)])) 

    def test_sum_array2(self):
        self.simulator = RiscVSimulator()
        self.simulator.load_instructions("test_asm/test_asm_sum_array/sum_array2.asm")
        self.simulator.execute()
        self.assertEqual(self.simulator.registers["s3"], sum([i for i in range(100)])) 

    def test_sum_array3(self):
        self.simulator = RiscVSimulator()
        self.simulator.load_instructions("test_asm/test_asm_sum_array/sum_array3.asm")
        self.simulator.execute()
        self.assertEqual(self.simulator.registers["s3"], sum([i for i in range(1000)])) 

    def test_sum_array4(self):
        self.simulator = RiscVSimulator()
        self.simulator.load_instructions("test_asm/test_asm_sum_array/sum_array4.asm")
        self.simulator.execute()
        self.assertEqual(self.simulator.registers["s3"], to_int32(sum([i * 8746384 for i in range(1000)]))) 


class TestToInt32(unittest.TestCase):
    def test_positive_values(self):
        self.assertEqual(to_int32(0), 0)                     
        self.assertEqual(to_int32(1), 1)                    
        self.assertEqual(to_int32(2147483647), 2147483647)
        self.assertEqual(to_int32(2147483648), -2147483648)

    def test_negative_values(self):
        self.assertEqual(to_int32(-1), -1)                  
        self.assertEqual(to_int32(-2147483648), -2147483648)
        self.assertEqual(to_int32(-2147483649), 2147483647)

    def test_overflow_values(self):
        self.assertEqual(to_int32(4294967295), -1)
        self.assertEqual(to_int32(4294967296), 0)
        self.assertEqual(to_int32(4294967297), 1)

    def test_large_positive_values(self):
        self.assertEqual(to_int32(10000000000), 1410065408)

    def test_large_negative_values(self):
        self.assertEqual(to_int32(-10000000000), -1410065408)

if __name__ == "__main__":
    unittest.main()