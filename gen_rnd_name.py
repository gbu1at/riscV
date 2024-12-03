import random

# Функция для генерации забавного названия
def generate_funny_name():
    funny_1_words = ["funny",
                    "fun", 
                    "cool",
                    "unusual",
                    "pink",
                    "green",
                    "black" ]
    
    funny_2_words = ["cucumber",
                    "pepper",
                    "cat",
                    "tomato",
                    "cherry" ]

    funny_3_words = ["stroll" ,
                    "drink" ,
                    "eat" ,
                    "sniff",
                    ]
    
    funny_4_words = ["in_the_garden",
                    "in_the_toilet",
                    "in_the_forest",
                    "behind_garages",
                    "in_the_basement"]

    funny_name = f"{random.choice(funny_1_words)}_{random.choice(funny_2_words)}_{random.choice(funny_3_words)}_{random.choice(funny_4_words)}_{random.randint(1, 1000)}.asm"
    return funny_name

# print(generate_funny_name())

# # Основная функция для переименования файлов
# def rename_files_in_directory(directory):
#     try:
#         for filename in os.listdir(directory):
#             file_path = os.path.join(directory, filename)
#             if os.path.isfile(file_path):  # Проверяем, что это файл
#                 new_name = generate_funny_name(filename)
#                 new_file_path = os.path.join(directory, new_name)
#                 os.rename(file_path, new_file_path)  # Переименовываем файл
#                 print(f"Переименован: {filename} -> {new_name}")
#     except Exception as e:
#         print(f"Произошла ошибка: {e}")

# # Укажите путь к директории, где находятся файлы
# directory_path = "/Users/apple/Desktop/risk_v_project/risk_v_project/test_asm"
# rename_files_in_directory(directory_path)