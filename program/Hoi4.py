'''
Hoi4 version 1.0 release
'''
from displayboard import board as Board
import random
from tabulate import tabulate
import math


#new data structure: ['first three letters', 'index', 'name', 'ideology', 'population', 'manpower', [allies], total_losses, 'player_nation']
#nations_list is  list of lists containing those values

def nation_info_get(index):
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
    fascism_starts = ["People's Democratic Republic of ", "Empire of ", "Nation of ", "State of ", "Racial State of ", "Dictatorship of ", "Nationalist ", "Greater ", "Blackshirt ", "Nazi ", "Fascist "]
    communism_starts = ["Soviet Republic of ", "People's Republic of ", "Union of ", "Revolutionary ", "People's Union of ", "Provincial Union of ", "Bolshevik ", "Marxist ", "Communist ", "People's democratic state of ", "Social Democratic ", "Socialist ", "Provisional Committee of "]
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
    if ideology == 'Fascism':
        manpower_modifier = 0.1
    elif ideology == 'Communism':
        manpower_modifier = 0.07
    elif ideology == 'Monarchy':
        manpower_modifier = 0.04
    else:
        manpower_modifier = 0.02
    manpower = math.ceil(population * manpower_modifier)
    fl_name = name.split(' ')
    first_letters = fl_name[-1][0] + fl_name[-1][1] + fl_name[-1][2]
    #first_letters, index, name, ideology, population, manpower, allies, total losses, is player
    info.append(first_letters)
    info.append(index)
    info.append(name)
    info.append(ideology)
    info.append(population)
    info.append(manpower)
    info.append([])
    info.append(0)
    info.append(False)
    return info

def board_create(nations_list):
    board = Board(4, 4, "")
    count = 0
    for x in range(1, 5):
        for y in range(1, 5):
            board.fill(x, y, (nations_list[count][0]))
            count += 1
    return board

def get_player_index(nations_list):
    for i in range(16):
        if nations_list[i][-1] == True:
            return i

def player_turn(nations_list, board, turns, loss):
    ui = input("Enter your command -: ").lower()
    if ui == "":
        pass #skip turn
    elif "attack" in ui:
        ui = ui.split(' ')
        if ui[1].isdigit() == False or int(ui[1]) < 0 or int(ui[1]) > 15: #checks for command validity
            print("Invalid target to attack")
            player_turn(nations_list, board, turns, loss)
        elif int(ui[1]) in nations_list[get_player_index(nations_list)][6]: #checks for already being allied
            print("You cannot attack an ally")
            player_turn(nations_list, board, turns, loss)
        elif does_border(board, nations_list, (get_player_index(nations_list)), int(ui[1])) == False:
            print("You can only attack nations that you border")
            player_turn(nations_list, board, turns, loss)
        else:
            target_nation = int(ui[1])
            nations_list = attack(nations_list, get_player_index(nations_list), target_nation, board, loss, turns)
    elif "ally" in ui:
        ui = ui.split(' ')
        if ui[1].isdigit() == False or int(ui[1]) < 0 or int(ui[1]) > 15: #checks for command validity
            print("Invalid target to ally")
            player_turn(nations_list, board, turns, loss)
        elif int(ui[1]) in nations_list[get_player_index(nations_list)][6]: #checks for already being allied
            print("Already allied to this nation")
            player_turn(nations_list, board, turns, loss)
        else:
            target_nation = int(ui[1])
            nations_list = ally(nations_list, get_player_index(nations_list), target_nation, board)
        return nations_list 
    elif ui == "help":
        help()
        player_turn(nations_list, board, turns, loss)
    else:
        print("Not a valid input.")
        player_turn(nations_list, board, turns, loss)

def computer_turn(nations_list, board, turns, loss):
    for nation in nations_list:
        nations_list = check_indices(nations_list)
        if nation[-1] == False:
            #do computer turn -> can_ally, then can_attack, then skip
            possible_alliances = can_ally(nations_list, board, nation)
            #after this, find the one with the most manpower
            if len(possible_alliances) == 0:
                possible_enemies = can_attack(nations_list, board, nation)
                if len(possible_enemies) == 0:
                    pass
                elif len(possible_enemies) == 1:
                    enemy_index = possible_enemies[0][0]
                    nations_list = attack(nations_list, nation[1], enemy_index, board, loss, turns)
                else:
                    total_manpowers = []
                    for possible_enemy in possible_enemies:
                        total_manpowers.append(possible_enemy[1])
                    min_manpower = min(total_manpowers)
                    min_index = total_manpowers.index(min_manpower)
                    enemy_index = possible_enemies[min_index][0]
                    nations_list = attack(nations_list, nation[1], enemy_index, board, loss, turns)
            elif len(possible_alliances) == 1:
                if possible_alliances[0] in nation[6]:
                    possible_enemies = can_attack(nations_list, board, nation)
                    if len(possible_enemies) == 0:
                        pass
                    elif len(possible_enemies) == 1:
                        enemy_index = possible_enemies[0][0]
                        nations_list = attack(nations_list, nation[1], enemy_index, board, loss, turns)
                    else:
                        total_manpowers = []
                        for possible_enemy in possible_enemies:
                            total_manpowers.append(possible_enemy[1])
                        min_manpower = min(total_manpowers)
                        min_index = total_manpowers.index(min_manpower)
                        enemy_index = possible_enemies[min_index][0]
                        nations_list = attack(nations_list, nation[1], enemy_index, board, loss, turns)
                else:
                    nations_list = ally(nations_list, nation[1], possible_alliances[0], board)
            else:
                highest_manpower = 0
                winner = ''
                for possible_alliance in possible_alliances:
                    cur_manpower = nations_list[possible_alliance][5]
                    if cur_manpower > highest_manpower:
                        winner = possible_alliance
                        highest_manpower = cur_manpower
                nations_list = ally(nations_list, nation[1], winner, board)

def can_ally(nations_list, board, computer_nation):
    possible_alliances = []
    for nation in nations_list:
        offer_ideology = computer_nation[3]
        target_ideology = nation[3]
        if target_ideology == 'Fascism' or offer_ideology == 'Fascism':
            opinion = -100
        else:
            opinion = -20
        if target_ideology == 'Communism':
            if offer_ideology == 'Communism':
                opinion += 15
        elif target_ideology == 'Democracy':
            if offer_ideology == 'Democracy':
                opinion += 20
            elif offer_ideology == 'Monarchy':
                opinion += 10
        elif target_ideology == 'Monarchy':
            if offer_ideology == 'Monarchy':
                opinion += 10
            elif offer_ideology == 'Democracy':
                opinion += 10
        if (does_border(board, nations_list, computer_nation[1], nation[1])) == True:
            opinion += 10
        if opinion >= 0 and (nation[1] not in computer_nation[6]) == True and (nation[1] == computer_nation[1]) == False:
            possible_alliances.append(nation[1])
        else:
            pass #rejected alliances
    return possible_alliances

def can_attack(nations_list, board, computer_nation):
    possible_enemies = []
    computer_index = computer_nation[1]
    allied_manpower = computer_nation[5]
    #sums up the allied manpower
    for ally in computer_nation[6]: #remember that attacking ally is an integer, the index of each ally
        allied_manpower += nations_list[ally][5]
    for nation in nations_list:
        #finds the total manpower of all possible enemies and attacks the one with the lowest manpower
        if nation[1] == computer_index:
            pass
        elif nation[1] in computer_nation[6]:
            pass
        elif does_border(board, nations_list, nation[1], computer_index) == False:
            pass
        else:
            enemy_manpower = nation[5]
            for enemy in nation[6]:
                enemy_manpower += nations_list[enemy][5]
            if enemy_manpower >= allied_manpower:
                pass #<- this is how the computer will skip a turn eventually, back in computer turns
            else:
                possible_enemies.append((nation[1], enemy_manpower))
    return possible_enemies

def does_border(board, nations_list, nation_1, nation_2):
    #does border works on the first letters id in the base code, and will have to in this revised version
    nation_1_ID = nations_list[nation_1][0]
    nation_2_ID = nations_list[nation_2][0]
    for x in range(1, 5):
        for y in range(1, 5):
            if board.at_coord(x, y) == nation_1_ID:
                above = [x, y + 1] #y could be above 4
                below = [x, y - 1] #y could be below 1
                left = [x - 1, y] #x could be below 1
                right = [x + 1, y] #x could be above 4
                if 5 in above:
                    pass
                else:
                    if board.at_coord(above[0], above[1]) == nation_2_ID:
                        return True
                if 0 in below:
                    pass
                else:
                    if board.at_coord(below[0], below[1]) == nation_2_ID:
                        return True
                if 0 in left:
                    pass
                else:
                    if board.at_coord(left[0], left[1]) == nation_2_ID:
                        return True
                if 5 in right:
                    pass
                else:
                    if board.at_coord(right[0], right[1]) == nation_2_ID:
                        return True
    return False

def ally(nations_list, offer_nation, target_nation, board):
    offer_ideology = nations_list[offer_nation][3]
    target_ideology = nations_list[target_nation][3]
    if target_ideology == 'Fascism' or offer_ideology == 'Fascism':
        return print("They rejected our offer for an alliance!") #if either is fascist, allies are not allowed
    else:
        opinion = - 20 #sets the opinion. Assumes neither are fascist as fascist nations cant ally
    if target_ideology == 'Communism':
        if offer_ideology == 'Communism':
            opinion += 15
    elif target_ideology == 'Democracy':
        if offer_ideology == 'Democracy':
            opinion += 20
        elif offer_ideology == 'Monarchy':
            opinion += 10
    elif target_ideology == 'Monarchy':
        if offer_ideology == 'Monarchy':
            opinion += 10
        elif offer_ideology == 'Democracy':
            opinion += 10
    if (does_border(board, nations_list, offer_nation, target_nation)) == True:
        opinion += 10
    if opinion >= 0:
        print("Alliance formed between " + nations_list[offer_nation][2] + " and " + nations_list[target_nation][2] + "!")
        nations_list[offer_nation][6].append(target_nation)
        nations_list[target_nation][6].append(offer_nation)
        return nations_list
    else:
        print("They rejected our offer for an alliance!")
        return nations_list

def attack(nations_list, attacking_nation, target_nation, board, loss, turns):
    involved_nations = [attacking_nation, target_nation]
    manpower_attacking = nations_list[attacking_nation][5]
    manpower_defending = nations_list[target_nation][5]
    for attacking_ally in nations_list[attacking_nation][6]: #remember that attacking ally is an integer, the index of each ally
        manpower_attacking += nations_list[attacking_ally][5]
        involved_nations.append(attacking_ally)
    for defending_ally in nations_list[target_nation][6]: #remember that defending ally is an integer, the index of each ally
        manpower_defending += nations_list[defending_ally][5]
        involved_nations.append(defending_ally)
    loss_dice = random.randint(4, 8)
    #now we go through remaining nations and reduce their manpower by the loss dice amount BY ADDING IT TO TOTAL LOSSES
    if manpower_defending > manpower_attacking:
        print(nations_list[target_nation][2] + " defeated " + nations_list[attacking_nation][2])
        involved_nations.pop(0)
        if nations_list[attacking_nation][-1] == True:
            return player_loss(target_nation, turns, nations_list)
        for nation in involved_nations:
            cur_manpower = nations_list[nation][5]
            losses = math.floor((loss_dice/(100)) * (cur_manpower))
            nations_list[nation][-2] += losses
            nation_name = nations_list[nation][2]
            print(nation_name + " lost", losses)
        loser_ID = nations_list[attacking_nation]
        winner_ID = nations_list[target_nation]
        for x in range(1, 5):
            for y in range(1, 5):
                if board.at_coord(x, y) == loser_ID:
                    board.fill(x, y, winner_ID)
        #now this sections sorts out the exchange of indexes
        nations_list.pop(attacking_nation)
        for nation in nations_list:
            #index checker -> first checks if the index is higher than the target index, which, if it is, deletes one
            #then checks the list of allies. If the list of allies includes the target index, it is removed, if it includes any index higher, those indexes are subtracted by one
            cur_index = nation[1]
            if cur_index > attacking_nation:
                nation[1] -= 1
            for ally in nation[6]:
                if ally == attacking_nation:
                    nation[6].pop(nation[6].index(attacking_nation))
                elif ally > attacking_nation:
                    nation[6][nation[6].index(ally)] -= 1
    elif manpower_defending < manpower_attacking:
        print(nations_list[attacking_nation][2] + " defeated " + nations_list[target_nation][2])
        involved_nations.pop(1)
        for nation in involved_nations:
            cur_manpower = nations_list[nation][5]
            losses = math.floor((loss_dice/(100)) * (cur_manpower))
            nations_list[nation][-2] += losses
            nation_name = nations_list[nation][2]
            print(nation_name + " lost", losses)
        loser_ID = nations_list[target_nation][0]#this section is devoted to the exchange of land
        winner_ID = nations_list[attacking_nation][0]
        for x in range(1, 5):
            for y in range(1, 5):
                if board.at_coord(x, y) == loser_ID:
                    board.fill(x, y, winner_ID)
        #now this sections sorts out the exchange of indexes
        nations_list.pop(target_nation)
        for nation in nations_list:
            #index checker -> first checks if the index is higher than the target index, which, if it is, deletes one
            #then checks the list of allies. If the list of allies includes the target index, it is removed, if it includes any index higher, those indexes are subtracted by one
            cur_index = nation[1]
            if cur_index > target_nation:
                nation[1] -= 1
            for ally in nation[6]:
                if ally == target_nation:
                    nation[6].pop(nation[6].index(target_nation))
                elif ally > target_nation:
                    nation[6][nation[6].index(ally)] -= 1
    else:
        print("Stalemate! Everyone loses manpower to no gain.")
        for nation in involved_nations:
            cur_manpower = nations_list[nation][5]
            losses = math.floor((loss_dice/(100)) * (cur_manpower))
            nations_list[nation][-2] += losses
            nation_name = nations_list[nation][2]
            print(nation_name + " lost", losses)
    return nations_list
    
def update_manpowers(nations_list):
    #take nation, take current pop -> update; then update manpower using same math
    for nation in nations_list:
        cur_pop = nation[4]
        cur_pop = math.ceil(cur_pop*1.02)
        cur_losses = nation[-2]
        if nation[3] == 'Fascism':
            manpower_modifier = 0.1
        elif nation[3] == 'Communism':
            manpower_modifier = 0.07
        elif nation[3] == 'Monarchy':
            manpower_modifier = 0.04
        else:
            manpower_modifier = 0.02
        new_manpower = (math.ceil(cur_pop * manpower_modifier))-cur_losses
        nation[4] = cur_pop
        nation[5] = new_manpower
    return nations_list

def check_indices(nations_list):
    max_index = len(nations_list) - 1
    #check every nations alliances for duplicates and any alliance that is higher than the max index (just delete those)
    for nation in nations_list:
        no_dupe_allies = []
        for ally in nation[6]:
            if (ally not in no_dupe_allies) == True:
                no_dupe_allies.append(ally)
        nation[6] = no_dupe_allies
        for ally in nation[6]:
            if ally > max_index:
                faulty_ally_index = nation[6].index(ally)
                nation[6][faulty_ally_index] -= 1
    return nations_list

        
def win_check(nations_list, turns):
    if len(nations_list) == 1 and nations_list[0][-1] == True: #win by defeating everyone else
        player_win(turns, nations_list, 'Domination')
    else:
        num_of_allies = len(nations_list[get_player_index(nations_list)][6]) #win by being allied to all other players
        if num_of_allies == (len(nations_list) - 1):
            player_win(turns, nations_list, 'Diplomatic')
    return False

def player_loss(attacking_nation, turns, nations_list):
    winning_ai = nations_list[attacking_nation][2]
    print("You were defeated by " + winning_ai + "!")
    print("You were defeated in", turns, "turns.")
    quit()

def player_win(turns, nations_list, win_type):
    player_nation_ = nations_list[get_player_index(nations_list)]
    print("You won!")
    print("You started as " + player_nation_[2])
    print("You won in", turns, "turns.")
    quit()

def help():
    printer = ("----------------------")
    print(printer)
    print("Game will now begin: ")
    print(printer)
    print("Commands:")
    print('"attack [nation number]", attacks another nation and their allies (calls in your allies too).')
    print('"ally [nation number]", sends an alliance request to another nation (they can decline).')
    print('"", entering nothing will skip your turn. Manpower will still regenerate but no decisions will be made.')
    print('"help", will print this information again and not take up your turn.')
    return(print(printer))

#start up routine
print("Welcome to Budget HOI4")
nations_list = [] #initiates nations list
index_list_for_check = []
for i in range(16):
    info = nation_info_get(i)
    while info[0] in index_list_for_check:
        info = nation_info_get(i)
    index_list_for_check.append(info[0])
    nations_list.append(info) #iteratively creates 16 nations using the nation_info_get function
print(tabulate(nations_list, headers=["ID:", "Index", "Name:", "Ideology:", "Population:", "Manpower: ", "Allies:", "Total Losses:", "Player Nation:"]))
print("----------------------")
print("Your map: ")
board = board_create(nations_list)
print(board)
print("----------------------")
print("You must now pick a nation.")
for i in range(len(nations_list)):
    string = ""
    string += str(i) + ".   " + nations_list[i][0]
    print(string)
player_nation = int(input("Enter the number nation you wish to play -: "))
nations_list[player_nation][-1] = True
help()
turns = 0
loss = False
while loss == False:
    turns += 1
    print("Turn", turns)
    print(tabulate(nations_list, headers=["ID:", "Index:", "Name:", "Ideology:", "Population:", "Manpower: ", "Allies:", "Total Losses:", "Player Nation:"]))
    print("Current Map:")
    print("----------------------")
    print(board)
    print("----------------------")
    #print out player information here
    player_index = get_player_index(nations_list)
    player_name = nations_list[player_index][2]
    player_ideology = nations_list[player_index][3]
    player_manpower = nations_list[player_index][5]
    player_allies = nations_list[player_index][6]
    print("Nation:", player_name)
    print("Ideology:", player_ideology)
    print("Manpower:", player_manpower)
    print("Allies:", player_allies)
    print("----------------------")
    player_turn(nations_list, board, turns, loss)
    win_check(nations_list, turns)
    computer_turn(nations_list, board, turns, loss)
    nations_list = update_manpowers(nations_list)