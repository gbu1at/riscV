from random import randint
import random
import sys
from gen_rnd_name import generate_funny_name
import sys
sys.path.insert(1, '../RiskV')
from RiskVSimulator import *
import os


def generate_test(N, dir="unusual_tests"):

    def get_generate_instruction(N):
        X = random.randint(0, 2 ** 11)

        def num_rnd():
            return random.randint(-2**10, 2**10)

        def f_xori():
            return [f"xori x9, x9, {num_rnd()}"]

        def f_addi():
            return [f"addi x9, x9, {num_rnd()}"]

        def f_ori():
            return [f"ori x9, x9, {num_rnd()}"]

        def f_andi():
            return [f"andi x9, x9, {num_rnd()}"]

        def f_slli():
            return [f"slli x9, x9, {num_rnd()}"]

        def f_srli():
            return [f"srli x9, x9, {num_rnd()}"]

        def f_srai():
            return [f"srai x9, x9, {num_rnd()}"]

        def f_add():
            return [f"addi x18, x18, {num_rnd()}", f"add x9, x9, x18", f"xor x18, x18, x18"]

        def f_sub():
            return [f"addi x18, x18, {num_rnd()}", f"sub x9, x9, x18", f"xor x18, x18, x18"]

        def f_sll():
            return [f"addi x18, x18, {num_rnd()}", f"sll x9, x9, x18", f"xor x18, x18, x18"]

       
        def f_fence():
            return ["fence zero, zero"]

        def f_ecall():
            return ["ecall"]

        def f_ebreak():
            return ["ebreak"]

        def f_srl():
            return [
                f"addi x18, x18, {num_rnd()}",
                f"srl x9, x9, x18",
                f"xor x18, x18, x18"
            ]

        def f_sra():
            return [
                f"addi x18, x18, {num_rnd()}",
                f"sra x9, x9, x18",
                f"xor x18, x18, x18"
            ]

        def f_slt():
            return [
                f"addi x18, x18, {num_rnd()}",
                f"slt x9, x9, x18",
                f"xor x18, x18, x18"
            ]

        def f_sltu():
            return [
                f"addi x18, x18, {num_rnd()}",
                f"sltu x9, x9, x18",
                f"xor x18, x18, x18"
            ]

        def f_xor():
            return [
                f"addi x18, x18, {num_rnd()}",
                f"xor x9, x9, x18",
                f"xor x18, x18, x18"
            ]

        def f_or():
            return [
                f"addi x18, x18, {num_rnd()}",
                f"or x9, x9, x18",
                f"xor x18, x18, x18"
            ]

        def f_and():
            return [
                f"addi x18, x18, {num_rnd()}",
                f"and x9, x9, x18",
                f"xor x18, x18, x18"
            ]

        def f_mul():
            return [
                f"addi x18, x18, {num_rnd()}",
                f"mul x9, x9, x18",
                f"xor x18, x18, x18"
            ]

        def f_mulh():
            return [
                f"addi x18, x18, {num_rnd()}",
                f"mulh x9, x9, x18",
                f"xor x18, x18, x18"
            ]

        def f_mulhsu():
            return [
                f"addi x18, x18, {num_rnd()}",
                f"mulhsu x9, x9, x18",
                f"xor x18, x18, x18"
            ]

        def f_mulhu():
            return [
                f"addi x18, x18, {num_rnd()}",
                f"mulhu x9, x9, x18",
                f"xor x18, x18, x18"
            ]

        def f_div():
            return [
                f"addi x18, x18, {num_rnd()}",
                f"div x9, x9, x18",
                f"xor x18, x18, x18"
            ]

        def f_divu():
            return [
                f"addi x18, x18, {num_rnd()}",
                f"divu x9, x9, x18",
                f"xor x18, x18, x18"
            ]

        def f_rem():
            return [
                f"addi x18, x18, {num_rnd()}",
                f"rem x9, x9, x18",
                f"xor x18, x18, x18"
            ]

        def f_remu():
            return [
                f"addi x18, x18, {num_rnd()}",
                f"remu x9, x9, x18",
                f"xor x18, x18, x18"
            ]





        def get_command():
            cmd = [
                f_xori,
                f_addi,
                f_ori,
                f_andi,
                f_slli,
                f_srli,
                f_srai,
                f_add,
                f_sub,
                f_sll,
                f_fence,
                f_ecall,
                f_ebreak,
                f_srl,
                f_sra,
                f_slt,
                f_sltu,
                f_xor,
                f_or,
                f_and,
                f_mul,
                f_mulh,
                f_mulhsu,
                f_mulhu,
                f_div,
                f_divu,
                f_rem,
                f_remu
            ]

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

        for i in range(8):
            instructions.append("sw zero, 0, zero")

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


_, N, M, SEED, dir_name = sys.argv
M = int(M)
N = int(N)
SEED = int(SEED)

random.seed(SEED)

os.system(f"rm -rf {dir_name} 2>/dev/null || true")
os.system(f"mkdir {dir_name} 2>/dev/null || true")

for i in range(N):
    generate_test(M, dir_name)