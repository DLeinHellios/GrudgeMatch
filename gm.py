#!/usr/bin/env python3
# gm.py - GrudgeMatch, simple CLI recordkeeping for fighting games

import sys, json


#----- Information -----
def print_help():
    '''Prints command list'''
    print("============= COMMAND LIST =============")
    print("HELP - Print command information")
#    print("MATCH - Initiate a match between two fighters")
    print("ADD - Add a new fighter or game")
    print("REMOVE - Remove a fighter or game")
    print("RANK - Ranks fighters by their records")
    print("GAMES - Ranks games by number of matches on record")
#    print("GIFT - Add money to a fighter's account balance")
    print("QUIT - Exit GrudgeMatch")
    print("========================================")


#----- Data -----
def sort_data(data):
    '''Accepts data dictionary, returns sorted by w/l record'''
    pass


def write_data(backup, data):
    '''Writes data to JSON file and backup file'''
    if not backup:
        with open('data.json', 'w', encoding='utf-8') as dataFile:
            json.dump(data, dataFile, ensure_ascii=False, indent=4)

    else:
        with open('.data.json.backup', 'w', encoding='utf-8') as dataFile:
            json.dump(data, dataFile, ensure_ascii=False, indent=4)


def load_data():
    '''Loads data from data.json or backup, creates blank data.json if missing'''
    try:
        with open('data.json') as dataFile:
            data = json.load(dataFile)

    except:
        try:
            with open('.data.json.backup') as dataFile:
                data = json.load(dataFile)
                write_data(False, data)

        except:
            data = {"fighters":{}, "games":{}}
            write_data(False, data)

    return data["fighters"], data["games"]


#----- Features -----
def confirm():
    '''Confirm user input, returns bool'''
    choice = input("Please confirm <y/n>: ")
    confirmed = False
    if choice[0].lower() == "y":
        confirmed = True

    return confirmed


def add_fighter():
    '''Adds a fighter to roster'''
    print("A New Fighter Approaches!")
    name = input("Fighter Name: ")

    if name not in fighters.keys() and name != '':
        print("========================================")
        print("Add new fighter " + name + "?")
        if confirm():
            fighters[name] = {
            "balance": 0,
            "wins": 0,
            "losses": 0,
            "matches": 0}

            write_data(False, {"fighters":fighters, "games":games})
            print("Fighter " + name + " has entered the game")

        print("========================================")

    else:
        print("Sorry, that name is unavailable, enter another?")
        if confirm():
            add_fighter()
        print("========================================")


def add_game():
    '''Adds a new game to the game list'''
    print("A New Challenge Draws Near!")
    name = input("Game Name: ")

    if name not in games.keys() and name != '':
        print("========================================")
        print("Add new game " + name + "?")
        if confirm():
            games[name] = 0

            write_data(False, {"fighters":fighters, "games":games})
            print(name + " has been added to games")

        print("========================================")

    else:
        print("Sorry, that name is unavailable, enter another?")
        if confirm():
            add_game()
        print("========================================")


def add_menu():
    '''Menu to select whether to add fighter or game'''
    print("What to add?")
    print(" 1) New Fighter")
    print(" 2) New Game")
    choice = input("> ")
    print("========================================")

    if choice == "1":
        add_fighter()
    elif choice == "2":
        add_game()
    else:
        print("Invalid Option - returning to main menu")
        print("========================================")


def remove_fighter():
    '''Remove a single fighter from the roster'''
    print("Remove a fighter")
    name = input("Fighter Name: ")

    if name in fighters.keys():
        print("========================================")
        print("Remove fighter " + name + "?")
        if confirm():
            del fighters[name]
            write_data(False, {"fighters":fighters, "games":games})
            print(name + " has been stricken from the records")

        print("========================================")

    else:
        print("Invalid Name - returning to main menu")
        print("========================================")


def remove_game():
    '''Removes a single game from the game list'''
    print("Remove a game")
    name = input("Game Name: ")

    if name in games.keys():
        print("========================================")
        print("Remove game " + name + "?")
        if confirm():
            del games[name]
            write_data(False, {"fighters":fighters, "games":games})
            print(name + " has been stricken from the records")

        print("========================================")

    else:
        print("Invalid Game - returning to main menu")
        print("========================================")


def remove_menu():
    '''Menu to select whether to remove fighter or game'''
    print("What to remove?")
    print(" 1) Remove Fighter")
    print(" 2) Remove Game")
    choice = input("> ")
    print("========================================")

    if choice == "1":
        remove_fighter()
    elif choice == "2":
        remove_game()
    else:
        print("Invalid Option - returning to main menu")
        print("========================================")


def rank_fighters():
    '''List all fighters by their records'''
    for key in fighters:
        print(key)
    print("========================================")
        # TODO - print stats, formatted


def rank_games():
    '''Lists all games by matches on record'''
    for key in games:
        print(key)
    print("========================================")
        # TODO - print plays, formatted


#----- Commands -----
def cmd_input():
    '''Collect command input to pass to parser'''
    cmd = input("> ")
    cmd = cmd.split(" ")
    return cmd


def cmd_parse(cmd):
    '''Parses list of commands and executes features'''
    if cmd[0].lower() in ["exit","quit","q"]:
        sys.exit()

    elif cmd[0].lower() in ["help","h","?",""]:
        print_help()

    elif cmd[0].lower() in ["add", "new"]:
        add_menu()

    elif cmd[0].lower() in ["remove", "rm"]:
        remove_menu()

    elif cmd[0].lower() in ["rank", "list", "ls"]:
        rank_fighters()

    elif cmd[0].lower() in ["game", "games"]:
        rank_games()

    else:
        print("Invalid command! Type HELP for a list of commands")
        print("========================================")


#----------------------
def setup():
    global fighters, games # Global data objects
    fighters, games = load_data()
    write_data(True, {"fighters":fighters, "games":games}) # Save backup
    print("GrudgeMatch - Lets get down to business!")


def main():
    setup() # Runs once
    while True: # Main loop
        print("Type HELP for a list of commands, QUIT to exit")
        cmd_parse(cmd_input())


#=============================================
if __name__ == "__main__":
    main()
