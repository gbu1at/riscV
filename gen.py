from random import randint
import random
import sys
from gen_rnd_name import generate_funny_name
from main import *

def generate_test(N, dir="unusual_tests"):
    def get_generate_instruction(N):
        X = random.randint(0, 10000)

        def shift_rnd():
            return random.randint(0, 5)

        def num_rnd():
            return random.randint(0, 2**20)

        def f1():
            return [f"addi x18, zero, {shift_rnd()}", "sll x9, x9, x18", "xor x18, x18, x18"]

        def f2():
            return [f"addi x18, zero, {shift_rnd()}", "srl x9, x9, x18", "xor x18, x18, x18"]

        def f3():
            return [f"xori x9, x9, {num_rnd()}"]

        def f4():
            return [f"slli x9, x9, {shift_rnd()}"]

        def f5():
            return [f"srli x9, x9, {shift_rnd()}"]

        def f9():
            return [f"sub x9, zero, x9"]

        def f10():
            return [f"ori x9, x9, {num_rnd()}"]

        def f11():
            return [f"addi x9, zero, {num_rnd()}"]

        def f12():
            return [f"addi x18, zero, {shift_rnd()}", "sra x9, x9, x18", "xor x18, x18, x18"]


        def get_command():
            cmd = [f1, f2, f3, f4, f5, f9, f10, f11, f12]
            f = random.choice(cmd)
            return f()

        instructions = [f"addi x9, zero, {X}"]

        for i in range(N):
            group_cmd = get_command()
            instructions.extend(group_cmd)

        RESULT = random.randint(0, 1e9)

        instructions.append("ebreak")
        instructions.append(f"addi x18, zero, {RESULT}")
        instructions.append(f"beq x9, x18, 10000")

        for i in range(1000):
            instructions.append("addi zero, zero, 0")

        return instructions



    def instructions_set_result(new_result):
        for i, line in enumerate(instructions):
            if line == "beq x9, x18, 10000":
                idx = i - 1
                instructions[idx] = f"addi x18, zero, {new_result}"
                break

    filename = dir + "/" + generate_funny_name()

    print(filename)
    
    instructions = get_generate_instruction(N)

    with open(filename, "w") as file:
        for instruction in instructions:
            file.write(instruction + "\n")

    machine = RiscVSimulator()

    machine.load_instructions(filename)
    lru_arg, bitplru_arg = machine.execute()

    new_result = machine.registers["x9"]
    instructions_set_result(new_result)

    with open(filename, "w") as file:
        for instruction in instructions:
            file.write(instruction + "\n")


_, N, M, SEED = sys.argv
M = int(M)
N = int(N)
SEED = int(SEED)

random.seed(SEED)

for i in range(N):
    generate_test(M)