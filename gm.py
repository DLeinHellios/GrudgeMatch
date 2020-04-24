#!/usr/bin/env python3
# gm.py - GrudgeMatch, simple CLI recordkeeping for fighting games

import sys, datetime, os, json


class Fighters():
    def __init__(self, data):
        '''Manages fighter data'''
        self.data = data


    def sort(self, rank):
        '''Returns fighters.data sorted by rank or n matches'''
        if rank: # Sort by w/l ratio
            fighters = {k: v for k, v in sorted(self.data.items(), key=lambda item: item[1]["wins"]/item[1]["matches"] if item[1]["matches"] else 0, reverse = True)}

        else: # Sort by number of matches
            fighters = {k: v for k, v in sorted(self.data.items(), key=lambda item: item[1]["matches"], reverse = True)}

        return fighters


    def select(self, exclude):
        '''Displays menu for selecting fighters from list, accepts input and returns selection as str'''
        sortedFighters = self.sort(False)
        fighterList = []
        selection = None
        c = 1

        for f, matches in sortedFighters.items():
            if f != exclude:
                print(" " + str(c) + ") " + f)
                fighterList.append(f)
                c += 1

        choice = input("> ")
        if choice.isdigit() and int(choice) <= len(fighterList):
            selection = fighterList[int(choice) - 1]

        return selection


    def validate_name(self, name):
        '''Returns bool indicating name is valid'''
        valid = True
        if "," in name:
            valid = False
            print("Error - name contains restricted character ','")

        if name in self.data.keys():
            valid = False
            print("Error - name already in use")

        if name == "":
            valid = False
            print("Error - please enter a fighter name")

        if len(name) > 14:
            valid = False
            print("Error - name exceeds max characters (14)")

        return valid


    def add(self):
        '''Creates a new fighter record'''
        print("A New Fighter Approaches!")
        name = input("Fighter Name: ")

        if self.validate_name(name):
            print("\nAdd new fighter " + name + "?")
            if confirm():
                self.data[name] = {
                    "wins": 0,
                    "matches": 0}
                print("Fighter " + name + " has entered the game\n")

        else:
            print("Error submitting name, try again?\n")
            if confirm():

                self.add()



    def remove(self):
        '''Delete a single fighter record'''
        print("Remove a fighter")
        name = self.select(None)

        if name in self.data.keys():
            print("\nRemove fighter " + name + "?")
            if confirm():
                del self.data[name]
                print(name + " has been stricken from the records")

            print()

        else:
            print("Invalid Fighter - returning to main menu\n")


    def list(self, rank):
        '''Prints list of fighters sorted by rank or n matches'''
        ranks = self.sort(rank)
        print()
        labels = ["Name", "Wins", "Matches"]
        head = ["----", "----", "-------"]
        print(" {: <15} {: <5} {: <8}".format(*labels))
        print(" {: <15} {: <5} {: <8}".format(*head))
        for f, stats in ranks.items():
            print(" {: <15} {: <5} {: <8}".format(f, *stats.values()))
        print()



class Games():
    def __init__(self, data):
        '''Manages game data'''
        self.data = data


    def sort(self, rank):
        '''Returns game data sorted by matches played or alphabetically'''
        if rank: # Sort by number of matches
            games = {k: v for k, v in sorted(self.data.items(), key=lambda item: item[1], reverse = True)}

        else: # A-Z
            games = {k: v for k, v in sorted(self.data.items(), key=lambda item: item[0])}

        return games


    def select(self):
        '''Displays menu for selecting games from list, accepts input and returns selection as str'''
        sortedGames = self.sort(True)
        gameList = []
        selection = None
        c = 1

        for g, matches in sortedGames.items():
            print(" " + str(c) + ") " + g)
            gameList.append(g)
            c += 1

        choice = input("> ")
        if choice.isdigit() and int(choice) <= len(gameList):
            selection = gameList[int(choice) - 1]

        return selection


    def validate_name(self, name):
        '''Returns bool indicating name is valid'''
        valid = True
        if "," in name:
            valid = False
            print("Error - name contains restricted character ','")

        if name in self.data.keys():
            valid = False
            print("Error - name already in use")

        if name == "":
            valid = False
            print("Error - please enter a game title")

        if len(name) > 30:
            valid = False
            print("Error - name exceeds max characters (30)")

        return valid



    def add(self):
        '''Adds a new game to the game list'''
        print("A New Challenge Draws Near!")
        name = input("Game Name: ")

        if self.validate_name(name):
            print("\nAdd new game " + name + "?")
            if confirm():
                self.data[name] = 0
                print(name + " has been added to games library\n")

        else:
            print("Error submitting name, try again?\n")
            if confirm():
                self.add()


    def remove(self):
        '''Removes a single game from the game list'''
        print("Remove a game")
        name = self.select()

        if name in self.data.keys():
            print("\nRemove game " + name + "?")
            if confirm():
                del self.data[name]
                print(name + " has been stricken from the records")

            print()

        else:
            print("Invalid Game - returning to main menu\n")


    def list(self, rank):
        '''Lists all games by matches on record'''
        ranks = self.sort(rank)
        print()
        labels = ["Name", "Matches"]
        head = ["----", "-------"]
        print(" {: <31} {: <5}".format(*labels))
        print(" {: <31} {: <5}".format(*head))
        for g, matches in ranks.items():
            print(" {: <31} {: <5}".format(g, matches))
        print()



class Match:
    def check(self, fighters, games):
        '''Checks if enough data is present to conduct a match, returns bool if match can be played'''
        valid = True
        if len(fighters.data) < 2:
            print("Error - Please register at least 2 fighters")
            valid = False

        elif len(games.data) < 1:
            print("Error - Please register at least 1 game")
            valid = False

        if not valid:
            print("Invalid Selection - returning to main menu\n")

        return valid


    def save(self, match):
        '''Saves the match record to records.csv'''
        if not os.path.isfile("records.csv"):
            with open('records.csv', 'a') as recordsFile:
                recordsFile.write("date,game,p1,p2,win\n")
                record = ",".join(match) + "\n"
                recordsFile.write(record)

        else:
            record = ",".join(match) + "\n"
            with open('records.csv', 'a') as recordsFile:
                recordsFile.write(record)

        print("\n" + match[4] + " has been declared the victor in " + match[1])
        print("The match record has been saved, returning to main menu")


    def record(self, p1, p2, g):
        '''Collects victory information, updates data.json, and writes entry in records.csv'''
        print("Who won the match?")
        print(" 1) " + p1)
        print(" 2) " + p2)
        selection = input("> ")
        if selection not in ["1", "2"]:
            print("\nInvalid Selection - abort match recording?")
            if confirm():
                print()
                return None
            else:
                self.record(p1, p2, g)

        else:
            win = [p1,p2][int(selection) - 1]
            today = datetime.date.today()
            match = [today.strftime("%m/%d/%Y"),g,p1,p2,win]

            return match


    def draw(self, p1, p2, g):
        '''Draws match ongoing - this is where you fight'''
        print("========================================")
        print("          Player 1: " + p1)
        print(r'             _    _______')
        print(r'            | |  / / ___/')
        print(r'            | | / /\__ \ ')
        print(r'            | |/ /___/ / ')
        print(r'            |___//____/  ')
        print()
        print("          Player 2: " + p2)
        print('         -----------------')
        print("         "  + g)
        print("========================================")
        input("Press <enter> to submit match results")


    def conduct(self, fighters, games):
        '''Conducts a single match, start to finish'''
        if self.check(fighters, games):
            print("\nLet's get ready for action")
            print("Select a game")
            g = games.select()
            print("\nSelect Player 1")
            p1 = fighters.select(None)
            print("\nSelect Player 2")
            p2 = fighters.select(p1)

            if g != None and p1 != None and p2 != None:
                print("\nBegin match between " + p1 + " and " + p2 + " in " + g + "?")
                if confirm():
                    self.draw(p1, p2, g)
                    match = self.record(p1, p2, g)
                    if match != None:
                        self.save(match)
                        update_data(fighters, games, match)
                        print()

            else:
                print("Invalid Match Options - try again?")
                if confirm():
                    self.conduct(fighters, games)



class Parser:
    def command(self):
        '''Collect command input to pass to parser'''
        cmd = input("> ")
        cmd = cmd.split(" ")
        return cmd


    def parse(self, fighters, games, match, cmd):
        '''Parses list of commands and executes features'''
        if cmd[0].lower() in ["exit","quit","q"]:
            sys.exit()

        elif cmd[0].lower() in ["help","h","?",""]:
            print_help()

        elif cmd[0].lower() in ["match", "fight", "challenge"]:
            match.conduct(fighters, games)

        elif cmd[0].lower() in ["add", "new"]:
            if len(cmd) < 2:
                add_menu(fighters, games)
            else:
                if cmd[1].lower() in ["game", "games"]:
                    print()
                    games.add()
                    write_data(fighters, games, False)
                elif cmd[1].lower() in ["fighter", "fighters"]:
                    print()
                    fighters.add()
                    write_data(fighters, games, False)
                else:
                    print("Invalid Option - returning to main menu\n")

        elif cmd[0].lower() in ["remove", "rm"]:
            if len(cmd) < 2:
                remove_menu(fighters, games)
            else:
                if cmd[1].lower() in ["game", "games"]:
                    games.remove()
                    write_data(fighters, games, False)
                elif cmd[1].lower() in ["fighter", "fighters"]:
                    fighters.remove()
                    write_data(fighters, games, False)
                else:
                    print("Invalid Option - returning to main menu\n")

        elif cmd[0].lower() in ["list", "ls"]:
            if len(cmd) < 2:
                list_menu(fighters, games)
            else:
                if cmd[1].lower() in ["game", "games"]:
                    games.list(False)
                elif cmd[1].lower() in ["fighter", "fighters"]:
                    fighters.list(False)
                else:
                    print("Invalid Option - returning to main menu\n")

        elif cmd[0].lower() in ["rank", "ranks"]:
            if len(cmd) < 2:
                rank_menu(fighters, games)
            else:
                if cmd[1].lower() in ["game", "games"]:
                    games.list(True)
                elif cmd[1].lower() in ["fighter", "fighters"]:
                    fighters.list(True)
                else:
                    print("Invalid Option - returning to main menu\n")

        elif cmd[0].lower() in ["save", "s"]:
            write_data(fighters, games, False)
            print("Data has been saved\n")

        else:
            print("Invalid Command! Type HELP for a list of commands\n")



#----- Menus -----
def print_help():
    '''Prints command list'''
    print("============= COMMAND LIST =============")
    print(" HELP - Print command information")
    print(" MATCH - Initiate a match between two fighters")
    print(" ADD - Add a new fighter or game")
    print(" REMOVE - Remove a fighter or game")
    print(" LIST - Lists fighters by matches, or games by name")
    print(" RANK - Ranks fighters by records, or games by matches")
#    print(" DEPOSIT - Add money to a fighter's account balance")
#    print(" WITHDRAW - Remove money from a fighter's account balance")
    print(" QUIT - Exit GrudgeMatch\n")


def confirm():
    '''Prompts users to confirm an action, returns bool'''
    confirmed = False
    choice = ""
    while choice == "":
        choice = input("Please confirm <y/n>: ")

    if choice[0].lower() == "y":
        confirmed = True

    return confirmed


def add_menu(fighters, games):
    '''Menu to control add method flow if not specified as argument to parser'''
    print("What to add?")
    print(" 1) New Fighter")
    print(" 2) New Game")
    choice = input("> ")

    if choice.lower() in ["1", "fighter", "fighters"]:
        fighters.add()
        write_data(fighters, games, False)
    elif choice.lower() in ["2", "game", "games"]:
        games.add()
        write_data(fighters, games, False)
    else:
        print("Invalid Option - returning to main menu\n")


def remove_menu(fighters, games):
    '''Menu to control remove method flow if not specified as argument to parser'''
    print("What to remove?")
    print(" 1) Remove Fighter")
    print(" 2) Remove Game")
    choice = input("> ")

    if choice.lower() in ["1", "fighter", "fighters"]:
        fighters.remove()
        write_data(fighters, games, False)
    elif choice.lower() in ["2", "game", "games"]:
        games.remove()
        write_data(fighters, games, False)
    else:
        print("Invalid Option - returning to main menu\n")


def list_menu(fighters, games):
    '''Menu to control list method flow if not specified as argument to parser'''
    print("What to list?")
    print(" 1) List Fighters")
    print(" 2) List Games")
    choice = input("> ")

    if choice.lower() in ["1", "fighter", "fighters"]:
        fighters.list(False)
    elif choice.lower() in ["2", "game", "games"]:
        games.list(False)
    else:
        print("Invalid Option - returning to main menu\n")


def rank_menu(fighters, games):
    '''Menu to control rank method flow if not specified as argument to parser'''
    print("What to rank?")
    print(" 1) Rank Fighters")
    print(" 2) Rank Games")
    choice = input("> ")

    if choice.lower() in ["1", "fighter", "fighters"]:
        fighters.list(True)
    elif choice.lower() in ["2", "game", "games"]:
        games.list(True)
    else:
        print("Invalid Option - returning to main menu\n")


#----- Data -----
def write_data(fighters, games, backup):
    '''Writes data to JSON file or backup file, depending on bool backup'''
    data = {"fighters":fighters.data, "games":games.data}

    if not backup:
        with open('data.json', 'w', encoding='utf-8') as dataFile:
            json.dump(data, dataFile, ensure_ascii=False, indent=4)

    else:
        with open('.data.json.backup', 'w', encoding='utf-8') as dataFile:
            json.dump(data, dataFile, ensure_ascii=False, indent=4)


def update_data(fighters, games, match):
    '''Updates fighter and game data post-match'''
    fighters.data[match[2]]['matches'] += 1
    fighters.data[match[3]]['matches'] += 1
    fighters.data[match[4]]['wins'] += 1
    games.data[match[1]] += 1
    write_data(fighters, games, False)


def create_data_file():
    '''Creates blank data file'''
    data = {"fighters":{}, "games":{}}
    with open('data.json', 'w', encoding='utf-8') as dataFile:
        json.dump(data, dataFile, ensure_ascii=False, indent=4)

    return data


def read_data():
    '''Loads data from data.json or backup, creates blank data.json if missing'''
    try:
        with open('data.json') as dataFile:
            data = json.load(dataFile)

    except:
        try:
            with open('.data.json.backup') as dataFile:
                data = json.load(dataFile)
                write_data(data["fighters"], data["games"], False)

        except:
            data = create_data_file()

    return data


#----------------------
def setup():
    parser = Parser()
    data = read_data()
    fighters = Fighters(data['fighters'])
    games = Games(data['games'])
    match = Match()
    write_data(fighters, games, True) # Save backup
    print("GrudgeMatch - Lets get down to business!")

    return parser, fighters, games, match


def main():
    parser, fighters, games, match = setup() # Runs once
    while True: # Main loop
        print("Type HELP for a list of commands, QUIT to exit")
        parser.parse(fighters, games, match, parser.command())


#=============================================
if __name__ == "__main__":
    main()
