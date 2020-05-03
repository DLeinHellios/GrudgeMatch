import os, json, sys

class Players:
    def __init__(self):
        '''Contains and manages all player entries'''
        self.all = self.load() # Holds all player dicts


    def create_blank_file(self):
        '''Creates blank player file, returns blank player dict'''
        blank = {"players":{}}
        with open(os.path.join('data', 'players.json'), 'w', encoding='utf-8') as pFile:
            json.dump(blank, pFile, ensure_ascii=False, indent=2)

        return blank


    def load(self):
        '''Loads players.json, returns main player data dictionary'''
        if os.path.isfile(os.path.join('data', 'players.json')):
            try:
                with open(os.path.join('data', 'players.json')) as pFile:
                    all = json.load(pFile)
            except:
                print("ERROR - Player data file unreadable, does it contain errors?")
                #TODO - Add option to create blank file
                sys.exit()

        else:
            # Create a blank player file
            all = self.create_blank_file()

        return all['players']


    def save(self):
        '''Writes to data/players.json'''
        data = {'players':fighters}
        with open(os.path.join('data', 'players.json'), 'w', encoding='utf-8') as pFile:
            json.dump(data, pFile, ensure_ascii=False, indent=2)


    def invalidate_name(self, name):
        '''Returns a 0 for valid names, 1+ for error codes'''
        reserved = [
            '0','1','2','3','4','5','6','7','8','9',
            'default', 'player', 'name', ''
        ]

        illegal = [
            ',', '\\', '.'
        ]

        invalid = 0

        if name in reserved:
            # Name is on reserved list
            invalid = 1

        for i in illegal:
            if i in name:
                # Name uses an illegal character
                invalid = 2

        if len(name) > 14:
            # Name is too long
            invalid = 3

        return invalid


    def add(self, name):
        '''Creates a new player entry'''
        if not self.invalidate_name(name):
            self.all[name] = {"total": [0,0], "last": None, "game": {}}



class Games:
    def __init__(self):
        '''Contains and manages all game entries'''
        self.all = self.load() # Holds all game dicts


    def create_blank_file(self):
        '''Creates blank game file, returns blank player dict'''
        blank = {"games":{}}
        with open(os.path.join('data', 'games.json'), 'w', encoding='utf-8') as gFile:
            json.dump(blank, gFile, ensure_ascii=False, indent=2)

        return blank


    def load(self):
        '''Loads games.json, returns main games data dictionary'''
        if os.path.isfile(os.path.join('data', 'games.json')):
            try:
                with open(os.path.join('data', 'games.json')) as gFile:
                    all = json.load(gFile)
            except:
                print("ERROR - Game file unreadable, does it contain errors?")
                #TODO - Add option to create blank file
                sys.exit()

        else:
            # Create a blank player file
            all = self.create_blank_file()

        return all['games']



class Data:
    def __init__(self):
        #self.config = Config()
        self.players = Players()
        self.games = Games()
        #self.records = Records()


    def save_all(self):
        #self.config.save()
        #self.players.save()
        #self.games.save()

        pass
