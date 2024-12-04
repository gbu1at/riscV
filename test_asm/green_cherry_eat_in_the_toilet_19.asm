addi s0, zero, 0
addi s1, zero, 0
addi a0, zero, 30
beq  a0,  zero, 28
andi s2, a0, 1
srli a0, a0, 1
beq s2 , zero, 0x4
addi s0, s1, 0
addi s1, s1, 1 
jal zero, -24