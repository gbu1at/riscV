lui x5, 0x12345
auipc x0, 0x1F
jal x1, 0x9C
jalr x2, x3, 0x10
beq x4, x5, -88
bne x6, x7, 64
blt x8, x9, -32
bge x10, x11, 40
bltu x12, x13, -16
bgeu x14, x15, 24
lh x16, 4, x13
lw x18, 8, x19
lb x20, 12, x21
lbu x22, 16, x23
lhu x24, 20, x25
sw x26, -36, x27
sb x28, -40, x29
sh x30, -44, x31
addi x5, x5, 400
slti x6, x7, 100
sltiu x8, x9, 200
xori x10, x11, 0xFF
ori x12, x13, 0x0F
andi x14, x15, 0xF0
slli x16, x17, 2
srli x18, x19, 3
srai x20, x21, 1
add x22, x23, x24
sub x25, x26, x27
sll x28, x29, x30
slt x31, x5, x6
sltu x0, x1, x2
xor x3, x4, x5
srl x6, x7, x8
sra x9, x10, x11
or x12, x13, x14
and x15, x16, x17
ecall
ebreak
mul x18, x19, x20
mulh x21, x22,x23
mulhsu x24,x25,x26
mulhu x27,x28,x29
div x30,x31,x5
divu x6,x7,x8
rem x9,x10,x11
remu x12,x13,x14
