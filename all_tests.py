import os

def run_files_in_directory(directory):
    if not os.path.exists(directory):
        print(f"Директория {directory} не существует.")
        return

    for filename in os.listdir(directory):
        file_name, extend = filename.split(".")
        if extend == "asm":
            print(file_name)
            os.system(f"python3 main.py {file_name}")
        

directory_path = 'test_asm'
run_files_in_directory(directory_path)