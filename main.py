import sys
from setting import *
from Cache import *
from RiskVSimulator import *
from encoding_instructions import *
from functions import *



if __name__ == "__main__":
    machine = RiscVSimulator()
    _, *args = sys.argv
    

    filename = ""
    bin_filename = ""

    write_in_bin_file = False

    if len(args) == 2:
        if args[0] == "--asm":
            filename = args[1]
        else: assert(False)

    if len(args) == 4:
        if args[0] == "--asm" and args[2] == "--bin":
            filename = args[1]
            bin_filename = args[3]
            write_in_bin_file = True
        elif args[2] == "--asm" and args[0] == "--bin":
            filename = args[3]
            bin_filename = args[1]
            write_in_bin_file = True
        else: assert(False)

    instructions = machine.load_instructions(filename)

    lru_arg, bitplru_arg = machine.execute()
    arg = lru_arg + bitplru_arg
    fmt_0 = "replacement\thit rate\thit rate (inst)\thit rate (data)\n"
    fmt_1 = "        LRU\t%3.5f%%\t%3.5f%%\t%3.5f%%\n"
    fmt_2 = "       pLRU\t%3.5f%%\t%3.5f%%\t%3.5f%%\n"
    fmt =  fmt_0 + fmt_1 + fmt_2
    
    
    result = fmt % arg
    print(result)


    if write_in_bin_file:
        with open(bin_filename, "w") as file:
            for inst in instructions:
                inst_bin_str = encode_riscv_instruction(inst)
                inst_hex_str = binary_to_hex(inst_bin_str)
                file.write(inst_hex_str.lower() + "\n")

