'''
Hoi4 version 1.0 release
'''
from displayboard import board as Board
import random
from tabulate import tabulate
import math

def nation_info_get():
    #NATION = [first_letters, name, ideology, population, [allies], manpower]
    info = []
    ideologies = ['Fascism', 'Communism', 'Democracy', 'Monarchy']
    ends = ['ia', 'land', 'an', 'istan', 'a', 'tina', 'o', 'al', 'alie', 'ey', 'an', 'om', 'ea']
    consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
    vowels = ['a', 'e', 'i', 'o', 'u']
    name_dice = random.randint(1, 6)
    if name_dice <= 3:
        mid = random.choice(vowels).upper()
    else:
        mid = random.choice(consonants).upper()
    for i in range(name_dice):
        char_dice = random.randint(1, 10)
        if mid[-1] in consonants:
            mid += random.choice(vowels)
        else:
            mid += random.choice(consonants)
    info.append(mid[:3])
    fascism_starts = ["People's Democratic Republic of ", "Empire of ", "Nation of ", "State of ", "Racial State of ", "Dictatorship of ", "Nationalist ", "Greater ", "Blackshirt ", "Nazi ", "Fascist "]
    communism_starts = ["Soviet Republic of ", "People's Republic of ", "Union of ", "Revolutionary ", "People's Union of ", "Provincial Union of ", "Bolshevik ", "Marxist ", "Communist ", "People's democratic state of ", "Social Democratic ", "Socialist " "Provisional Committee of "]
    democracy_starts = ["Republic of ", "United States of ", "Federal States of ", "United ", "Democratic Republic of ", "Plurinational Republic of ", "Federation of ", "Parliamentary Republic of "]
    monarchy_starts = ["Kingdom of ", "Empire of ", "Heavenly Kingdom of ", "Realm of ", "Commonwealth of ", "Kingdom of ", "Kingdom of "]
    ideology = random.choice(ideologies)
    if ideology == 'Fascism':
        start = random.choice(fascism_starts)
    elif ideology == 'Communism':
        start = random.choice(communism_starts)
    elif ideology == 'Democracy':
        start = random.choice(democracy_starts)
    else:
        start = random.choice(monarchy_starts)
    name = start + mid + random.choice(ends)
    population = random.randint(100000, 10000000)
    info.append(name)
    info.append(ideology)
    info.append(population)
    info.append([])
    if ideology == 'Fascism':
        manpower_modifier = 0.1
    elif ideology == 'Communism':
        manpower_modifier = 0.07
    elif ideology == 'Monarchy':
        manpower_modifier = 0.04
    else:
        manpower_modifier = 0.02
    manpower = math.ceil(population * manpower_modifier)
    info.append(manpower)
    return info

def get_first_list(nations_list):
    first_letters_list = []
    for nation in nations_list:
        first_letters_list.append(nation[0])
    return first_letters_list

def create_board(first_letters_list):
    board = Board(4, 4, "")
    count = 0
    for x in range(4):
        for y in range(4):
            board.fill()
    return board

nations_list = []
for i in range(16):
    nations_list.append(nation_info_get())
first_letters_list = get_first_list(nations_list)
print(nations_list)
print(first_letters_list)
board = create_board(first_letters_list)
print(board)

