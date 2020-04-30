#!/usr/bin/env python3
# gm.py - GrudgeMatch: simple CLI record-keeping for fighting games

import sys, datetime, os, random, json


class Fighters():
    def __init__(self, data):
        '''Manages fighter data'''
        self.data = data['players']


    def get_wl(self, total):
        '''Generates W/L values for fighter rankings'''
        if total[1] == 0: # No matches
            wl = -1
        elif total[0] == total[1]: # Undefeated
            wl = 999999
        else:
            wl = total[0] / (total[1] - total[0])

        return wl


    def sort(self, rank):
        '''Returns fighters.data sorted by rank or n matches'''
        if rank: # W/L ratio
            fighters = {k: v for k, v in sorted(self.data.items(), key=lambda item: self.get_wl(item[1]['total']), reverse=True)}

        else: # A-Z
            fighters = {k: v for k, v in sorted(self.data.items(),  key=lambda item: item[0], reverse=False)}

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


    def add(self, name):
        '''Creates a new fighter record'''
        if name == None:
            print("A New Fighter Approaches!")
            name = input("Fighter Name: ")

        if self.validate_name(name):
            print("\nAdd new fighter " + name + "?")
            if confirm():
                self.data[name] = {"total": [0,0], "last": None, "game": {}}

                print("Fighter " + name + " has entered the game\n")

        else:
            print("Error submitting name, try again?")
            if confirm():
                print()
                self.add(None)
            else:
                print()


    def remove(self, name):
        '''Delete a single fighter record'''
        if name == None:
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
        labels = ["Name", "Wins", "Total", "W/L"]
        head = ["--------------", "----", "-----", "----"]
        print(" {: <15} {: <5} {: <6} {: <4}".format(*labels))
        print(" {: <15} {: <5} {: <6} {: <4}".format(*head))
        for f, stats in ranks.items():
            l = stats["total"][1] - stats["total"][0]

            if stats["total"][1] == 0:
                wl = "N/A"
            elif l == 0:
                wl = "UNDF"
            else:
                wl = str(round(stats["total"][0] / l if l else 0, 2))

            print(" {: <15} {: <5} {: <6} {: <4}".format(f, *stats["total"], wl))
        print()



class Games():
    def __init__(self, data):
        '''Manages game data'''
        self.data = data['games']


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


    def add(self, name):
        '''Adds a new game to the game list'''
        if name == None:
            print("A New Challenge Draws Near!")
            name = input("Game Name: ")

        if self.validate_name(name):
            print("\nAdd new game " + name + "?")
            if confirm():
                self.data[name] = 0
                print(name + " has been added to games library\n")

        else:
            print("Error submitting name, try again?")
            if confirm():
                print()
                self.add(None)
            else:
                print()


    def remove(self, name):
        '''Deletes a single game from the game list'''
        if name == None:
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
        head = ["------------------------------", "-------"]
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
        if not os.path.isfile(os.path.join('data', 'records.csv')):
            with open(os.path.join('data', 'records.csv'), 'a') as recordsFile:
                recordsFile.write('date,game,p1,p2,win\n')
                record = ",".join(match) + "\n"
                recordsFile.write(record)

        else:
            record = ",".join(match) + "\n"
            with open(os.path.join('data', 'records.csv'), 'a') as recordsFile:
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
                    rematch = True
                    while rematch:
                        self.draw(p1, p2, g)
                        match = self.record(p1, p2, g)
                        if match != None:
                            self.save(match)
                            update_data(fighters, games, match)
                            print()

                            print("Begin a rematch?")
                            if not confirm():
                                rematch = False
                                print()

                        else:
                            rematch = False

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


    def parse_add(self, fighters, games, cmd):
        if len(cmd) < 2:
            add_menu(fighters, games)

        elif len(cmd) == 2:
            if cmd[1].lower() in ["game", "games", "g"]:
                print()
                games.add(None)
                write_games(games.data)
            elif cmd[1].lower() in ["fighter", "fighters", "f"]:
                print()
                fighters.add(None)
                write_fighters(fighters.data)
            else:
                print("Invalid Option - returning to main menu\n")

        else:
            if cmd[1].lower() in ["game", "games", "g"]:
                games.add(cmd[2])
                write_games(games.data)
            elif cmd[1].lower() in ["fighter", "fighters", "f"]:
                fighters.add(cmd[2])
                write_fighters(fighters.data)
            else:
                print("Invalid Option - returning to main menu\n")


    def parse_rm(self, fighters, games, cmd):
        if len(cmd) < 2:
            remove_menu(fighters, games)

        elif len(cmd) == 2:
            if cmd[1].lower() in ["game", "games", "g"]:
                print()
                games.remove(None)
                write_games(games.data)
            elif cmd[1].lower() in ["fighter", "fighters", "f"]:
                print()
                fighters.remove(None)
                write_fighters(fighters.data)
            else:
                print("Invalid Option - returning to main menu\n")

        else:
            if cmd[1].lower() in ["game", "games", "g"]:
                games.remove(cmd[2])
                write_games(games.data)
            elif cmd[1].lower() in ["fighter", "fighters", "f"]:
                fighters.remove(cmd[2])
                write_fighters(fighters.data)
            else:
                print("Invalid Option - returning to main menu\n")


    def parse(self, fighters, games, match, cmd):
        '''Parses list of commands and executes features'''
        if cmd[0].lower() in ["exit","quit","q"]:
            print("Exiting GrudgeMatch\n")
            sys.exit()

        elif cmd[0].lower() in ["help","h","?",""]:
            print_help()

        elif cmd[0].lower() in ["match", "m", "run"]:
            match.conduct(fighters, games)

        elif cmd[0].lower() in ["add", "new"]:
            self.parse_add(fighters, games, cmd)

        elif cmd[0].lower() in ["remove", "rm"]:
            self.parse_rm(fighters, games, cmd)

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
            write_games(games.data)
            write_fighters(fighters.data)
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
    print(" QUIT - Exit GrudgeMatch\n")


def get_tagline():
    '''Returns a random tagline, for fun'''
    tag = random.choice([
        "Try that on my command line!",
        "We're checking the tapes",
        "Wiggity Washed",
        "Sonic Boom!",
        "Round 1: Fight",
        "Perfect KO!",
        "C-C-C-Combo Breaker!",
        "Finish Him!",
        "Bring on the cheese",
        "Ultra Ver.1.x.x: Turbo",
        "My buttons don't work",
        "Wakeup Uppercut",
        "Whens Mahvel",
        "Clip that sh*t"
        "Super Ver.1.x.x: Turbo",
        "Bring on the salty runback",
        "Just pick a top-tier",
        "Get ready for the next battle!"
    ])

    return tag


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

    if choice.lower() in ["1", "fighter", "fighters", "f"]:
        fighters.add(None)
        write_fighters(fighters.data)
    elif choice.lower() in ["2", "game", "games", "g"]:
        games.add(None)
        write_games(games.data)
    else:
        print("Invalid Option - returning to main menu\n")


def remove_menu(fighters, games):
    '''Menu to control remove method flow if not specified as argument to parser'''
    print("What to remove?")
    print(" 1) Remove Fighter")
    print(" 2) Remove Game")
    choice = input("> ")

    if choice.lower() in ["1", "fighter", "fighters", "f"]:
        fighters.remove(None)
        write_fighters(fighters.data)
    elif choice.lower() in ["2", "game", "games", "g"]:
        games.remove(None)
        write_games(games.data)
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
def write_fighters(fighters):
    '''Writes data to players.json'''
    data = {'players':fighters}
    with open(os.path.join('data', 'players.json'), 'w', encoding='utf-8') as fFile:
        json.dump(data, fFile, ensure_ascii=False, indent=2)


def write_games(games):
    '''Writes data to games.json'''
    data = {'games':games}
    with open(os.path.join('data', 'games.json'), 'w', encoding='utf-8') as gFile:
        json.dump(data, gFile, ensure_ascii=False, indent=2)


def update_data(fighters, games, match):
    '''Updates fighter and game data post-match'''
    g = match[1]
    d,g,p1,p2,w = match[0],match[1],match[2],match[3],match[4]

    fighters.data[p1]['total'][1] += 1
    fighters.data[p2]['total'][1] += 1
    fighters.data[w]['total'][0] += 1

    today = datetime.date.today()
    fighters.data[p1]['last'] = today.strftime("%m/%d/%Y")
    fighters.data[p2]['last'] = today.strftime("%m/%d/%Y")

    if g in fighters.data[p1]['game'].keys():
        fighters.data[p1]['game'][g][1] += 1
    else:
        fighters.data[p1]['game'][g] = [0,1]

    if g in fighters.data[p2]['game'].keys():
        fighters.data[p2]['game'][g][1] += 1
    else:
        fighters.data[p2]['game'][g] = [0,1]

    fighters.data[w]['game'][g][0] += 1
    games.data[g] += 1

    write_fighters(fighters.data)
    write_games(games.data)


def create_fighter_file():
    '''Creates blank fighter file'''
    f = {"players":{}}
    with open(os.path.join('data', 'players.json'), 'w', encoding='utf-8') as fFile:
        json.dump(f, fFile, ensure_ascii=False, indent=2)

    return f


def create_game_file():
    '''Creates blank game file'''
    g = {"games":{}}
    with open(os.path.join('data', 'games.json'), 'w', encoding='utf-8') as gFile:
        json.dump(g, gFile, ensure_ascii=False, indent=2)

    return g


def read_data():
    '''Loads data from data.json or backup, creates blank data.json if missing'''
    try:
        with open(os.path.join('data', 'players.json')) as fFile:
            fighters = json.load(fFile)
    except:
        fighters = create_fighter_file()

    try:
        with open(os.path.join('data', 'games.json')) as gFile:
            games = json.load(gFile)
    except:
        games = create_game_file()

    return fighters, games


#----------------------
def setup():
    parser = Parser()
    fData,gData = read_data()
    fighters = Fighters(fData)
    games = Games(gData)
    match = Match()
    tagline = get_tagline()
    print("GrudgeMatch - " + tagline)

    return parser, fighters, games, match


def main():
    try:
        parser, fighters, games, match = setup() # Runs once
        while True: # Main loop
            print("Type HELP for a list of commands, QUIT to exit")
            parser.parse(fighters, games, match, parser.command())

    except KeyboardInterrupt:
        print("\nExiting GrudgeMatch\n")


#=============================================
if __name__ == "__main__":
    main()
