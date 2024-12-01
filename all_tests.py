import os
import sys

def run_files_in_directory(directory):
    if not os.path.exists(directory):
        print(f"Директория {directory} не существует.")
        return

    os.system("rm -r out_cache_info || true")
    os.system("mkdir out_cache_info")
    for filename in os.listdir(directory):
        file_name, extend = filename.split(".")
        if extend == "asm":
            print(file_name)
            os.system(f"python3 main.py b {file_name}")
        

# _, directory_path = sys.argv
directory_path = "test_asm"
run_files_in_directory(directory_path)