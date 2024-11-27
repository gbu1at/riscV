from random import randint
N = 1000

instructions = []

instructions.append("xor s1, s1, s1\n")
instructions.append("xor s2, s2, s2\n")

for i in range(N):
    instructions.append("sw s1, s2, 0\n")
    instructions.append("addi s2, s2, 4\n")
    instructions.append("addi s1, s1, 8746384\n")

instructions.append("xor s3, s3, s3\n")
instructions.append("addi s2, s2, -4\n")

for i in range(N):
    instructions.append("lw s1, s2, 0\n")
    instructions.append("addi s2, s2, -4\n")
    instructions.append("add s3, s3, s1\n")

file_name = "test_asm/test_asm_sum_array/sum_array4.asm"
with open(file_name, "w") as file:
    for instruction in instructions:
        file.write(instruction)
