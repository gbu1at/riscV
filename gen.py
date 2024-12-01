from random import randint


PC = 0x10000


X = 0b100010001
Y = 0b1

instructions = [
                f"addi x1, zero, {X}",
                f"addi x3, zero, {Y}",
                "sw x1, zero, 0",
                "lb x2, zero, 0",
                "beq x2, x3, 1000",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0",
                "addi x0, x0, 0"]


file_name = "test_asm/20.asm"
with open(file_name, "w") as file:
    for instruction in instructions:
        file.write(instruction + "\n")
