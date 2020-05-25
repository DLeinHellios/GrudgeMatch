import os, json, sys

class Players:
    def __init__(self):
        '''Contains and manages all player entries'''
        self.path = os.path.join('data', 'players.json')
        self.load() # Holds all player dicts in self.all


    def create_blank_file(self):
        '''Creates blank player file, returns blank player dict'''
        blank = {"players":{}}
        with open(self.path, 'w', encoding='utf-8') as pFile:
            json.dump(blank, pFile, ensure_ascii=False, indent=2)

        return blank


    def load(self):
        '''Loads players.json, returns main player data dictionary'''
        if os.path.isfile(self.path):
            try:
                with open(self.path) as pFile:
                    all = json.load(pFile)
            except:
                print("ERROR - Player data file unreadable, does it contain errors?")
                #TODO - Add option to create blank file
                sys.exit()

        else:
            # Create a blank player file
            all = self.create_blank_file()

        self.all = all['players']


    def save(self):
        '''Writes to data/players.json'''
        data = {'players':self.all}
        with open(self.path, 'w', encoding='utf-8') as pFile:
            json.dump(data, pFile, ensure_ascii=False, indent=2)


    def invalidate_name(self, name):
        '''Returns a 0 for valid names, 1+ for error codes'''
        reserved = ['0','1','2','3','4','5','6','7','8','9','default','player','name','game','data']
        illegal = [',', '\\', '.', "/", "`", "~"]
        invalid = 0

        if name in self.all.keys(): # Name in use
            invalid = 1
        if name.lower() in reserved: # Name is on reserved list
            invalid = 2
        for i in illegal:
            if i in name: # Name uses illegal character
                invalid = 3
        if len(name) > 10: # Name is too long
            invalid = 4

        return invalid


    def add(self, name):
        '''Creates a new player entry'''
        self.all[name] = {"total": [0,0], "last": None, "game": {}}


    def remove(self, name):
        '''Removes a player entry'''
        del self.all[name]


    def add_match(self, name, game, date):
        '''Adds a single match to a player entry'''
        if name not in self.all.keys(): # Add entry if not present
            self.add(name)

        self.all[name]['total'][1] += 1
        self.all[name]['last'] = date # TODO - add a check for more recent date

        if game not in self.all[name]['game'].keys(): # Add game if first match
            self.all[name]['game'][game] = [0,0]

        self.all[name]['game'][game][1] += 1


    def add_win(self, name, game):
        '''Adds a win to a player entry'''
        # Always call after add_match()!
        self.all[name]['total'][0] += 1
        self.all[name]['game'][game][0] += 1


    def parse_match(self, match):
        '''Parses a match record list and updates player entry'''
        for name in [match[2],match[3]]:
            self.add_match(name, match[1], match[0])

        self.add_win(match[4], match[1])



class Games:
    def __init__(self):
        '''Contains and manages all game entries'''
        self.path = os.path.join('data', 'games.json')
        self.load() # Holds all game dicts in self.all


    def create_blank_file(self):
        '''Creates blank game file, returns blank player dict'''
        blank = {"games":{}}
        with open(os.path.join(self.path), 'w', encoding='utf-8') as gFile:
            json.dump(blank, gFile, ensure_ascii=False, indent=2)

        return blank


    def load(self):
        '''Loads games.json, returns main games data dictionary'''
        if os.path.isfile(self.path):
            try:
                with open(self.path) as gFile:
                    all = json.load(gFile)
            except:
                print("ERROR - Game file unreadable, does it contain errors?")
                #TODO - Add option to create blank file
                sys.exit()

        else:
            # Create a blank player file
            all = self.create_blank_file()

        self.all = all['games']


    def save(self):
        '''Writes to data/games.json'''
        data = {'games':self.all}
        with open(self.path, 'w', encoding='utf-8') as gFile:
            json.dump(data, gFile, ensure_ascii=False, indent=2)


    def invalidate_name(self, name):
        '''Returns a 0 for valid names, 1+ for error codes'''
        reserved = ['0','1','2','3','4','5','6','7','8','9','default','player','name','game','date']
        illegal = [',', '\\', '.', "/", "`", "~"]
        invalid = 0

        if name in self.all.keys(): # Name in-use
            invalid = 1
        if name.lower() in reserved: # Name is on reserved list
            invalid = 2
        for i in illegal:
            if i in name: # Name uses an illegal character
                invalid = 3
        if len(name) > 30: # Name is too long
            invalid = 4

        return invalid


    def add(self, name):
        '''Creates a new game entry'''
        self.all[name] = {"match": 0, "last": None}


    def remove(self, name):
        '''Removes a game entry'''
        del self.all[name]


    def parse_match(self, match):
        '''Parses match record list and updates game entry'''
        if match[1] not in self.all.keys():
            self.add(match[1])

        self.all[match[1]]['match'] += 1
        self.all[match[1]]['last'] = match[0]



class Records:
    def __init__(self):
        '''Match records management object'''
        self.path = os.path.join('data','records.csv')


    def write(self, match):
        '''Writes a match record to records.csv'''
        if not os.path.isfile(self.path):
            with open(os.path.join('data', 'records.csv'), 'a') as rFile:
                rFile.write('date,game,p1,p2,win\n')
                record = ",".join(match) + "\n"
                rFile.write(record)

        else:
            record = ",".join(match) + "\n"
            with open(os.path.join('data', 'records.csv'), 'a') as rFile:
                rFile.write(record)


    def purge_player(self, name):
        '''Removes records of a specified player'''
        pass # TODO


    def purge_game(self, name):
        '''Removes records of a specified game'''
        pass # TODO


    def format(self, record):
        '''Accepts match string from records.csv, converts to list of values'''
        match = record.split(',')
        match[-1] = match[-1][0:-1] # Remove new-line character

        return match


    def read(self):
        '''Reads the records file and returns a list of records, each containing a list of strings'''
        records = []

        try:
            with open(os.path.join('data', 'records.csv')) as rFile:
                for r in rFile:
                    records.append(self.format(r))

            del records[0]

        except:
            records = []

        return records



class Config:
    def __init__(self):
        '''Holds configuration options'''
        self.path = os.path.join('data', 'config.json')
        self.load()


    def create_default_file(self):
        '''Creates the default config file is config is missing or damaged'''
        default = {"config":{
            "hide_sidebar": False,
        }}

        with open(os.path.join(self.path), 'w', encoding='utf-8') as cFile:
            json.dump(default, cFile, ensure_ascii=False, indent=2)

        return default


    def load(self):
        '''Loads games.json, returns main games data dictionary'''
        try:
            with open(self.path) as cFile:
                all = json.load(cFile)

        except:
            # Create a blank player file
            all = self.create_default_file()

        self.all = all['config']


    def save(self):
        '''Saves config data to data/config.json'''
        data = {'config':self.all}
        with open(self.path, 'w', encoding='utf-8') as cFile:
            json.dump(data, cFile, ensure_ascii=False, indent=2)



class Data:
    def __init__(self):
        '''Top-level data management object, holds data on players, games, tags, config, and records'''
        self.config = Config()
        self.players = Players()
        self.games = Games()
        self.records = Records()


    def save_all(self):
        '''Saves players and games'''
        self.players.save()
        self.games.save()


    def record_match(self, match):
        '''Accepts match list and adds to records, players, and games'''
        self.records.write(match)
        self.games.parse_match(match)
        self.players.parse_match(match)
        self.save_all()


    def rebuild(self):
        '''Rebuilds players.json and games.json by parsing all records'''
        try:
            with open(self.records.path, 'r') as rFile:
                self.players.all = {}
                self.games.all = {}

                for line in rFile:
                    if line == 'date,game,p1,p2,win\n':
                        continue

                    match = self.records.format(line)
                    self.games.parse_match(match)
                    self.players.parse_match(match)

            self.save_all()

            return 0 # No error

        except FileNotFoundError:
            return 1 # No records.csv

        except:
            return 2 # General error
