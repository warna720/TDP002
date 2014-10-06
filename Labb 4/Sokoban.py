#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os.path #For checking if file exists
from random import randint #For random level usage

#Global Variabels
field = []

#Symbol, Character
Player_S, Player_C = '@', 'p'
Box_S, Box_C = 'o', 'b'
Wall_S, Wall_C = '#', 'w'
Floor_S, Floor_C = ' ', 'f'
Storage_S, Storage_C = '.', 's'
B_in_S_S, B_in_S_C = '*', 'i'
P_on_S_S, P_on_S_C = '+', 'o'


"""
'@' = Player  (p)
'o' = Boxes   (b)
'#' = Walls   (w)
' ' = Floor   (f)
'.' = Storage (s)
'*' = B in S  (i)
'+' = P on S  (o)
"""

def add_to_field(obj, x, y):
    """Adds a coordination to the field for later use."""
    obj = obj.lower()
    if len(obj) and obj in "pbwfsio": #If not empty and valid input
        field.append([obj, x, y])
    else:
        print("{} is not a valid object!".format(obj))

def char_to_symbol(char):
    return{
        Player_C: Player_S,
        Box_C: Box_S,
        Wall_C: Wall_S,
        Floor_C: Floor_S,
        Storage_C: Storage_S,
        B_in_S_C: B_in_S_S,
        P_on_S_C: P_on_S_S
        }[char]

def symbol_to_char(symbol):
    return{
        Player_S: Player_C,
        Box_S: Box_C,
        Wall_S: Wall_C,
        Floor_S: Floor_C,
        Storage_S: Storage_C,
        B_in_S_S: B_in_S_C,
        P_on_S_S: P_on_S_C
        }[symbol]

def sort_coords():
    """Sorts coordinations based on x and y."""
    field.sort(key = lambda x: (x[1], x[2]))

def get_field():
    """Converts coords to visual field."""
    visual_field = ""
    sort_coords()
    x = 0
    y = 0
    for column, coord in enumerate(field):
        symbol = char_to_symbol(coord[0])
        if coord[1] == x and coord[2] > y:
            if column != 0:
                y += 1
            visual_field += " " * (coord[2]-y) + symbol
            y += coord[2]-y
        else:
            y = 0
            visual_field += "\n" + " " * (coord[2]-y) + symbol
            x += coord[1]-x
            y += coord[2]-y
        
    return visual_field
            

def sokoban_display():
    """Prints the field."""
    print(get_field())

def sokoban_load(filename):
    """Loads a sokobon file and returns the coordinates for each level."""
    lvls = []
    lvl = []
    if os.path.isfile(filename):
        file = open(filename)
        for x, line in enumerate(file):
            if line == '\n':
                lvls.append(lvl)
                lvl = []
            else:
                for y, symbol in enumerate(line):
                    if symbol not in '\n':
                        char = symbol_to_char(symbol.lower())
                        lvl.append([char, x, y])
        file.close()
    lvls.append(lvl)
    return lvls


def get_player_index():
    """Returns the coordination index for the player position."""
    return next(i for i, coord in enumerate(field) if Player_C in coord or P_on_S_C in coord)

def get_player_coords():
    """Returns the coordinations for the player position."""
    return field[get_player_index()]

def get_index_of_coords(x, y):
    """Returns coordiantion index based on x and y."""
    return next(i for i, coord in enumerate(field) if x in coord[1:2] and y in coord[2:3])

def get_coords_symbol(x, y):
    """Returns coordination symbol based on x and y."""
    pos = get_index_of_coords(x, y)
    return field[pos][0]

def get_moved_coords(x, y, direction):
    """Returns new coordinations based on user input (direction)."""
    if direction == 'a' or direction == 'l':
        y -= 1
    elif direction == 'd' or direction == 'r':
        y += 1
    elif direction == 'w' or direction == 'u':
        x -= 1
    elif direction == 's' or direction == 'd':
        x += 1
    return x, y

def change_index_symbol(op_index, s1, s2, s3, s4):
    """Changes symbol on requested coordination with two alternatives."""
    if field[op_index][0] == s1:
        field[op_index][0] = s2
    elif field[op_index][0] == s3:
        field[op_index][0] = s4

def move_player(direction):
    """Moves player."""
    player_index = get_player_index()
    x, y = field[player_index][1], field[player_index][2]
    x, y = get_moved_coords(x, y, direction)
    new_index = get_index_of_coords(x, y)

    if player_can_move(x, y, direction):
        #If box in front, move box.
        if field[new_index][0] == Box_C or field[new_index][0] == B_in_S_C:
            move_box(x, y, direction)

        #Change symbol for old player position
        change_index_symbol(player_index,
                            P_on_S_C, Storage_C,
                            Player_C, Floor_C)

        #Change symbol for new player position
        change_index_symbol(new_index,
                            Storage_C, P_on_S_C,
                            Floor_C, Player_C)
    
def move_box(x, y, direction):
    """Moves box."""
    box_index = get_index_of_coords(x, y)

    #Change symbol for old box position
    change_index_symbol(box_index,
                        B_in_S_C, Storage_C,
                        Box_C, Floor_C)
    
    x, y = get_moved_coords(x, y, direction)
        
    new_box_index = get_index_of_coords(x, y)
    symbol = field[new_box_index][0]

    #Change symbol for new box position
    change_index_symbol(new_box_index,
                        Storage_C, B_in_S_C,
                        Floor_C, Box_C)

def player_can_move(x, y, direction):
    """Checks if player can move."""
    new_coord_symbol = get_coords_symbol(x, y)
    if new_coord_symbol in (Floor_C + Storage_C): #If next position is floor or storage
        return True
    elif new_coord_symbol in (Box_C + B_in_S_C):  #If next position is box or box in storage
        return box_can_move(x, y, direction)
    return False
    
def box_can_move(x, y, direction):
    """Checks if box can move."""
    x, y = x, y
    x, y = get_moved_coords(x, y, direction)
    symbol = get_coords_symbol(x, y)

    if symbol in (Floor_C + Storage_C): #If next position for box is storage or floor
        return True
    return False

def get_all_levels():
    """Returns all coordinations for the 50 levels from level file."""
    return sokoban_load('levels/sokoban_levels.sokoban')

def get_level(lvl):
    """Returns chosen level."""
    levels = get_all_levels()
    return levels[lvl-1]

def get_random_lvl():
    """Returns a random level."""
    levels = get_all_levels()
    return levels[randint(0, 49)]

def unfinished():
    """Checks if level complete."""
    #If no more storage left and player is not standing on storage
    return Storage_C in [j for i in field for j in i] or P_on_S_C in [j for i in field for j in i]

def start_game():
    """Starts and continues game until it is finished."""
    directon = ""
    while unfinished():
        sokoban_display()
        direction = input("Make your move (l)eft, (r)ight, (u)p, (d)own or wasd: ").lower()
        move_player(direction)
        print()
    sokoban_display()
    print("\nCongratulations, Level Complete!")

def choose_lvl():
    """A menu system for the player."""
    global field
    selected = 0
    while not 1 <= selected <= 2:
        print("Welcome to Sokoban, please choose a level.")
        print("1.\tRandom Level")
        print("2.\tChoose Level")
        selected = int(input())
    if selected == 2:
        lvl = 0
        while not 1 <= lvl <= 50:
            lvl = int(input("Select a level between 1-50: "))
        field = get_level(lvl)
    else:
        field = get_random_lvl()
        
if __name__ == '__main__':
    #Dev option
    #field = [ ['b', 1, 2], ['p', 1, 3], ['w', 0, 0], ['w', 0, 1], ['w', 0, 2], ['w', 0, 3], ['w', 0, 4], ['w', 1, 0], ['s', 1, 1], ['f', 1, 4], ['w', 1, 5], ['w', 2, 0], ['w', 2, 1], ['w', 2, 2], ['w', 2, 3], ['w', 2, 4]]

    choose_lvl()
    start_game()
