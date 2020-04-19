#!/usr/bin/env python3
# gm.py - GrudgeMatch, simple CLI recordkeeping for fighting games

import sys, json


#----- Information -----
def print_help():
    '''Prints command list'''
    print("============= COMMAND LIST =============")
    print(" HELP - Print command information")
#    print(" MATCH - Initiate a match between two fighters")
    print(" ADD - Add a new fighter or game")
    print(" REMOVE - Remove a fighter or game")
    print(" LIST - Lists fighters by number of matches")
    print(" RANK - Ranks fighters by their records")
    print(" GAMES - Lists games by number of matches on record")
#    print(" DEPOSIT - Add money to a fighter's account balance")
    print(" QUIT - Exit GrudgeMatch")
    print("========================================")


#----- Data -----
def sort_fighters(rank, fighters):
    '''Accepts and returns fighters sorted by either rank or number of matches'''
    if rank: # Sort by w/l
        fighters = {k: v for k, v in sorted(fighters.items(), key=lambda item: item[1]["wins"]/item[1]["matches"] if item[1]["matches"] else 0, reverse = True)}

    else: # Sort by # of matches
        fighters = {k: v for k, v in sorted(fighters.items(), key=lambda item: item[1]["matches"], reverse = True)}

    return fighters


def sort_games(games):
    '''Accepts and returns games sorted by number of matches'''
    games = {k: v for k, v in sorted(games.items(), key=lambda item: item[1], reverse = True)}

    return games


def write_data(backup):
    '''Writes data to JSON file and backup file'''
    global fighters, games

    fighters = sort_fighters(False, fighters)
    games = sort_games(games)
    data = {"fighters":fighters, "games":games}

    if not backup:
        with open('data.json', 'w', encoding='utf-8') as dataFile:
            json.dump(data, dataFile, ensure_ascii=False, indent=4)

    else:
        with open('.data.json.backup', 'w', encoding='utf-8') as dataFile:
            json.dump(data, dataFile, ensure_ascii=False, indent=4)


def read_data():
    '''Loads data from data.json or backup, creates blank data.json if missing'''
    try:
        with open('data.json') as dataFile:
            data = json.load(dataFile)

    except:
        try:
            with open('.data.json.backup') as dataFile:
                data = json.load(dataFile)
                write_data(False)

        except:
            data = {"fighters":{}, "games":{}}
            write_data(False)

    return data["fighters"], data["games"]


#----- Features -----
def confirm():
    '''Confirm user input, returns bool'''
    choice = input("Please confirm <y/n>: ")
    confirmed = False
    if choice[0].lower() == "y":
        confirmed = True

    return confirmed


def select_fighter():
    '''Displays menu for selecting fighters from list, accepts input and returns selection'''
    fighterList = []
    selection = None
    c = 1

    for f, matches in fighters.items():
        print(" " + str(c) + ") " + f)
        fighterList.append(f)
        c += 1

    choice = input("> ")
    if choice.isdigit() and int(choice) <= len(fighterList):
        selection = fighterList[int(choice) - 1]

    return selection


def select_game():
    '''Displays menu for selecting games from list, accepts input and returns selection'''
    gameList = []
    selection = None
    c = 1

    for g, matches in games.items():
        print(" " + str(c) + ") " + g)
        gameList.append(g)
        c += 1

    choice = input("> ")
    if choice.isdigit() and int(choice) <= len(gameList):
        selection = gameList[int(choice) - 1]

    return selection


def add_fighter():
    '''Adds a fighter to roster'''
    print("A New Fighter Approaches!")
    name = input("Fighter Name: ")

    if name not in fighters.keys() and name != '':
        print("========================================")
        print("Add new fighter " + name + "?")
        if confirm():
            fighters[name] = {
            "wins": 0,
            "matches": 0,
            "balance": 0}

            write_data(False)
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

            write_data(False)
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

    if choice.lower() in ["1", "fighter", "fighters"]:
        add_fighter()
    elif choice.lower() in ["2", "game", "games"]:
        add_game()
    else:
        print("Invalid Option - returning to main menu")
        print("========================================")


def remove_fighter():
    '''Remove a single fighter from the roster'''
    print("Remove a fighter")
    name = select_fighter()

    if name in fighters.keys():
        print("========================================")
        print("Remove fighter " + name + "?")
        if confirm():
            del fighters[name]
            write_data(False)
            print(name + " has been stricken from the records")

        print("========================================")

    else:
        print("Invalid Name - returning to main menu")
        print("========================================")


def remove_game():
    '''Removes a single game from the game list'''
    print("Remove a game")
    name = select_game()

    if name in games.keys():
        print("========================================")
        print("Remove game " + name + "?")
        if confirm():
            del games[name]
            write_data(False)
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

    if choice.lower() in ["1", "fighter", "fighters"]:
        remove_fighter()
    elif choice.lower() in ["2", "game", "games"]:
        remove_game()
    else:
        print("Invalid Option - returning to main menu")
        print("========================================")


def list_fighters():
    '''List all fighters by thenumber of matches played'''
    labels = ["Name", "Wins", "Matches", "Balance"]
    head = ["----", "----", "-------", "-------"]
    print(" {: <10} {: <5} {: <8} {: <8}".format(*labels))
    print(" {: <10} {: <5} {: <8} {: <8}".format(*head))
    for f, stats in fighters.items():
        print(" {: <10} {: <5} {: <8} ${: <8}".format(f, *stats.values()))
    print("========================================")


def rank_fighters():
    '''List all fighters by their w/l records'''
    global fighters
    ranks = sort_fighters(True, fighters)

    labels = ["Name", "Wins", "Matches", "Balance"]
    head = ["----", "----", "-------", "-------"]
    print(" {: <10} {: <5} {: <8} {: <8}".format(*labels))
    print(" {: <10} {: <5} {: <8} {: <8}".format(*head))
    for f, stats in ranks.items():
        print(" {: <10} {: <5} {: <8} ${: <8}".format(f, *stats.values()))
    print("========================================")


def rank_games():
    '''Lists all games by matches on record'''
    print("========================================")
    labels = ["Name", "Matches"]
    head = ["----", "-------"]
    print(" {: <18} {: <5}".format(*labels))
    print(" {: <18} {: <5}".format(*head))
    for g, matches in games.items():
        print(" {: <18} {: <5}".format(g, matches))
    print("========================================")


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

    elif cmd[0].lower() in ["list", "ls"]:
        list_fighters()

    elif cmd[0].lower() in ["rank", "ranks"]:
        rank_fighters()

    elif cmd[0].lower() in ["game", "games"]:
        rank_games()

    elif cmd[0].lower() in ["save", "s"]:
        write_data(False)
        print("Data has been saved")
        print("========================================")

    else:
        print("Invalid command! Type HELP for a list of commands")
        print("========================================")


#----------------------
def setup():
    global fighters, games # Global data objects
    fighters, games = read_data()
    write_data(True) # Save backup
    print("GrudgeMatch - Lets get down to business!")


def main():
    setup() # Runs once
    while True: # Main loop
        print("Type HELP for a list of commands, QUIT to exit")
        cmd_parse(cmd_input())


#=============================================
if __name__ == "__main__":
    main()
