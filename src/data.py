import os, json, sys, sqlite3


class Config:
    def __init__(self):
        '''Holds configuration options'''
        self.path = os.path.join('data', 'config.json')
        self.load()


    def create_default(self):
        '''Creates the default config file is config is missing or damaged'''
        default = {"settings":{
            "hide_sidebar": False,
        }}

        with open(os.path.join(self.path), 'w', encoding='utf-8') as cFile:
            json.dump(default, cFile, ensure_ascii=False, indent=2)

        return default


    def load(self):
        '''Reads data/config.json and builds dict as self.settings'''
        try:
            with open(self.path) as cFile:
                c = json.load(cFile)

        except:
            # Create a blank player file
            c = self.create_default()

        self.settings = c['settings']


    def save(self):
        '''Saves config data to data/config.json'''
        data = {'settings':self.settings}
        with open(self.path, 'w', encoding='utf-8') as cFile:
            json.dump(data, cFile, ensure_ascii=False, indent=2)



class Query:
    def __init__(self,conn,cursor):
        '''Contains methods to query database'''
        self.db = conn
        self.c = cursor


    def all_player_names(self, isActive):
        '''Returns a list of all player names'''
        if isActive: # Only active players
            self.c.execute('SELECT Name FROM Players WHERE IsActive=1;')
            names = self.c.fetchall()
        else: # All players
            self.c.execute('SELECT Name FROM Players;')
            names = self.c.fetchall()

        for i in range(len(names)):
            names[i] = names[i][0]

        return names


    def all_game_names(self, isActive):
        '''Returns a list of all game names'''
        if isActive: # Only active games
            self.c.execute('SELECT Name FROM Games WHERE IsActive=1;')
            names = self.c.fetchall()
        else: # All games
            self.c.execute('SELECT Name FROM Games;')
            names = self.c.fetchall()

        for i in range(len(names)):
            names[i] = names[i][0]

        return names


    def all_player_ids(self):
        '''Returns a dictionary of all players, where key=name, value=id'''
        self.c.execute('SELECT Id, Name FROM Players;')
        results = self.c.fetchall()

        ids = {}
        for r in results:
            ids[r[1]] = r[0]

        return ids


    def all_game_ids(self):
        '''Returns a dictionary of all games, where key=name, value=id'''
        self.c.execute('SELECT Id, Name FROM Games;')
        results = self.c.fetchall()

        ids = {}
        for r in results:
            ids[r[1]] = r[0]

        return ids


    def all_player_status(self):
        '''Returns a dict where key=name, value=IsActive for all players'''
        self.c.execute('SELECT Name, IsActive FROM Players;')
        results = self.c.fetchall()

        # Format as dict
        statuses = {}
        for result in results:
            statuses[result[0]] = result[1]

        return statuses


    def all_game_status(self):
        '''Returns a dict where key=name, value=IsActive for all games'''
        self.c.execute('SELECT Name, IsActive FROM Games;')
        results = self.c.fetchall()

        # Format as dict
        statuses = {}
        for result in results:
            statuses[result[0]] = result[1]

        return statuses


    def all_player_details(self, isActive):
        '''Returns a list of tuples (Id, Name, Wins, Matches, LastMatch) for each player'''
        if isActive:
            active = ('1',)
        else:
            active - ('%',)

        self.c.execute('''
            SELECT
                Players.Id AS Id,
                Players.Name AS Name,
                (SELECT COUNT(*) FROM MatchRecords WHERE WinnerId = Players.Id) as WinCount,
                (SELECT COUNT(*) FROM MatchRecords WHERE Player1Id = Players.Id OR Player2Id = Players.Id) as MatchCount,
                (SELECT MAX(Date) FROM MatchRecords WHERE Player1Id = Players.Id OR Player2Id = Players.Id) as LastMatch

            FROM Players

            WHERE Players.IsActive = ?

            GROUP BY Players.Id;''', active)

        return self.c.fetchall()


    def all_game_details(self, isActive):
        '''Returns a list of tuples (name,nMatches,lastMatch) for each game'''
        if isActive:
            active = ('1',)
        else:
            active - ('%',)

        self.c.execute('''
            SELECT
                Games.Id AS Id,
                Games.Name AS Name,
                (SELECT COUNT(*) FROM MatchRecords WHERE GameId = Games.Id) as MatchCount,
                (SELECT MAX(Date) FROM MatchRecords WHERE GameId = Games.Id) as LastMatch

            FROM Games

            WHERE Games.IsActive = ?

            GROUP BY Games.Id;''', active)

        return self.c.fetchall()


    def match_folders(self):
        '''Returns a sorted list of all games found in match records (id, name)'''
        self.c.execute('''
            SELECT DISTINCT Records.GameId as GameId,
                (SELECT Games.Name FROM Games WHERE Games.Id = Records.GameId) AS GameName
            FROM MatchRecords AS Records, Games
            WHERE Games.IsActive = 1
            ORDER BY Games.Name;''')

        return self.c.fetchall()


    def match_records(self, p1, p2, game):
        '''Accepts ids for p1, p2, and game, returns all matching results from records table, pass '%' for wildcard'''
        args = (p1,p1,p2,p2,game)
        self.c.execute('''
            SELECT
                Records.Id AS RecordId,
                Records.Date AS Date,
                (SELECT Players.Name FROM Players WHERE Players.Id = Records.Player1Id) AS Player1,
                (SELECT Players.Name FROM Players WHERE Players.Id = Records.Player2Id) AS Player2,
                (SELECT Players.Name FROM Players WHERE Players.Id = Records.WinnerId) AS Winner,
                (SELECT Games.Name FROM Games WHERE Games.Id = Records.GameId) AS Game

            FROM MatchRecords as Records

            WHERE (Records.Player1Id LIKE ? OR Records.Player2ID LIKE ?)
                AND (Records.Player1Id LIKE ? OR Player2Id LIKE ?)
                AND Records.GameId LIKE ?

            ORDER BY Game, Date;''', args)

        return self.c.fetchall()



class Data:
    def __init__(self):
        '''Top-level data management object, holds data on players, games, tags, config, and records'''
        self.init_dir()
        self.path = os.path.join('data', 'records.db')

        if os.path.isfile(self.path):
            self.db = sqlite3.connect(self.path) # Connection
            self.c = self.db.cursor() # Cursor
        else:
            self.init_db()

        self.query = Query(self.db, self.c)
        self.config = Config()


    def init_dir(self):
        '''Creates data dir if missing'''
        try:
            if not os.path.exists("data"):
                os.makedirs("data")
        except:
            print('Unable to create data directory! Exiting...')
            sys.exit()


    def init_db(self):
        '''Creates initial db tables'''
        try:
            self.db = sqlite3.connect(self.path) # Connection
            self.c = self.db.cursor() # Cursor

            with open(os.path.join("src", "sql", "create_db_tables.sql")) as script:
                cmd = script.read()
                self.c.executescript(cmd)
                self.db.commit()
        except:
            print("Unable to initialize database! Exiting...")
            sys.exit()


    def new_player(self, name):
        '''Creates a new player record with the provided name'''
        try:
            self.c.execute('INSERT INTO "Players" ("Name") VALUES (?)', (name,))
            self.db.commit()
        except:
            print("Unable to add player! Exiting...")
            sys.exit()


    def new_game(self, name):
        '''Creates a new game record with the provided name'''
        try:
            self.c.execute('INSERT INTO "Games" ("Name") VALUES (?)', (name,))
            self.db.commit()
        except:
            print("Unable to add game! Exiting...")
            sys.exit()


    def activate_player(self, name):
        '''Flips players.is_active to True for provided player'''
        try:
            self.c.execute('UPDATE Players SET IsActive=1 WHERE Name=?', (name,))
            self.db.commit()
        except:
            print("Unable to activate player! Exiting...")
            sys.exit()


    def activate_game(self, name):
        '''Flips games.is_active to True for provided player'''
        try:
            self.c.execute('UPDATE Games SET IsActive=1 WHERE Name=?', (name,))
            self.db.commit()
        except:
            print("Unable to activate game! Exiting...")
            sys.exit()


    def deactivate_player(self, name):
        '''Flips players.is_active to False for provided player'''
        try:
            self.c.execute('UPDATE Players SET IsActive=0 WHERE Name=?', (name,))
            self.db.commit()
        except:
            print("Unable to deactivate player! Exiting...")
            sys.exit()


    def deactivate_game(self, name):
        '''Flips games.is_active to False for provided player'''
        try:
            self.c.execute('UPDATE Games SET IsActive=0 WHERE Name=?', (name,))
            self.db.commit()
        except:
            print("Unable to deactivate game! Exiting...")
            sys.exit()


    def validate_player_name(self, name):
        '''Returns 0 for valid names, 1+ for error codes'''
        reserved = ['0','1','2','3','4','5','6','7','8','9','default','player','name','game','data']
        illegal = [',', '\\', '.', "/", "`", "~"]
        err = 0

        if name in self.query.all_player_names(True): # Name in use
            err = 1

        elif name in self.query.all_player_names(False): # Name in-use, but inactive
            err = 2

        elif name.lower() in reserved: # Name is on reserved list
            err = 3

        elif len(name) > 10: # Name is too long
            err = 4

        elif not err: # Name uses illegal character
            for i in illegal:
                if i in name:
                    err = 5

        return err


    def validate_game_name(self, name):
        '''Returns 0 for valid names, 1+ for error codes'''
        reserved = ['0','1','2','3','4','5','6','7','8','9','default','player','name','game','date']
        illegal = [',', '\\', '.', "/", "`", "~"]
        err = 0

        if name in self.query.all_game_names(True): # Name in-use
            err = 1

        elif name in self.query.all_game_names(False): # Name in-use, but inactive
            err = 2

        elif name.lower() in reserved: # Name is on reserved list
            err = 3

        elif len(name) > 30: # Name is too long
            err = 40

        elif not err:
            for i in illegal:
                if i in name: # Name uses an illegal character
                    err = 5

        return err


    def convert_match(self, match):
        '''Accepts match dict containing names, returns dict of ids'''
        playerIDs = self.query.all_player_ids()
        gameIDs = self.query.all_game_ids()

        converted = {}
        converted['game'] = gameIDs[match['game']]
        converted['p1'] = playerIDs[match['p1']]
        converted['p2'] = playerIDs[match['p2']]
        converted['win'] = playerIDs[match['win']]
        converted['date'] = match['date']

        return converted


    def record_match(self, match):
        '''Records a single match to the Records table'''
        record = self.convert_match(match)
        args = ()
        self.c.execute('''
            INSERT INTO "MatchRecords" (GameId, Player1Id, Player2Id, WinnerId, Date)
            VALUES (?,?,?,?,?)''', (record['game'], record['p1'], record['p2'], record['win'], record['date']))
        self.db.commit()
