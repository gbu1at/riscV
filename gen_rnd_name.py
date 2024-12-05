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
