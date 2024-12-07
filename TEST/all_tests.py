import sys
sys.path.insert(1, '../RiskV')
from RiskVSimulator import *
import os
import sys

def run_files_in_directory(directory):
    if not os.path.exists(directory):
        print(f"Директория {directory} не существует.")
        return

    out_dir_name = directory + "_out"
    os.system(f"rm -r {out_dir_name} || true")
    os.system(f"mkdir {out_dir_name}")
    for filename in os.listdir(directory):
        file_name, extend = filename.split(".")
        if extend == "asm":
            print(file_name)
            
            machine = RiscVSimulator()
            
            machine.load_instructions(f"{directory}/{filename}")
            lru_arg, bitplru_arg = machine.execute()
            arg = lru_arg + bitplru_arg
            fmt_0 = "replacement\thit rate\thit rate (inst)\thit rate (data)\n"
            fmt_1 = "        LRU\t%3.5f%%\t%3.5f%%\t%3.5f%%\n"
            fmt_2 = "       pLRU\t%3.5f%%\t%3.5f%%\t%3.5f%%\n"
            fmt =  fmt_0 + fmt_1 + fmt_2
            
            
            result = fmt % arg

            filename_ = "".join(filename.split(".")[:-1])

            with open(f"{out_dir_name}/{filename_}.out", "w") as f:
                f.write(result)
        

_, directory_path = sys.argv
run_files_in_directory(directory_path)