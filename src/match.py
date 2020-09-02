import tkinter as tk
import tkinter.ttk as ttk
from src.message import *
import os, datetime


class MatchResults:
    def open(self, root, data, match, setup):
        '''Selects the winner of the match and submits the results'''
        self.top = tk.Toplevel(root)
        self.top.title("Submit Match")
        self.top.resizable(False,False)
        self.top.wm_attributes("-topmost", True)

        self.avatars,self.icons = [],[]
        self.load_players(data, setup, match["p1"],match["p2"])

        self.vsFrame = tk.Frame(self.top)
        self.vsImage = tk.PhotoImage(master=self.top, file=os.path.join('img', 'vs.png'))
        self.vs = tk.Label(master=self.vsFrame, image=self.vsImage)

        self.matchText = tk.Label(master=self.top, text=match["game"] + '\n' + match["date"])
        self.winner = None

        self.buttonFrame = tk.Frame(self.top)
        self.submit = tk.Button(self.buttonFrame, text="Submit", width=8, state=tk.DISABLED, command=lambda d=data,s=setup: self.submit_confirm(d,s))
        self.cancel = tk.Button(self.buttonFrame, text="Cancel", width=8, command=lambda s=setup: self.cancel_match(s))

        self.match = match # Hold reference to match values for later storage to records
        self.position()
        self.top.grab_set()


    def load_players(self, data, setup, p1, p2):
        '''Creates buttons for both players'''
        n = 0
        for p in [p1,p2]:
            if os.path.isfile(os.path.join('img', 'avatars', p +  '.png')):
                self.avatars.append(tk.PhotoImage(master=self.top, file=os.path.join('img', 'avatars', p +  '.png')))
            else:
                self.avatars.append(tk.PhotoImage(master=self.top, file=os.path.join('img', 'avatars',  'default.png')))

            self.icons.append(tk.Button(self.top, text=p, image=self.avatars[-1], compound=tk.TOP, width=90))
            self.icons[-1]['command'] = lambda d=data,s=setup,p=p,n=n: self.set_winner(d,s,p,n)
            n += 1


    def position(self):
        '''Position window elements'''
        self.icons[0].grid(row=1, column=1, padx=12, pady=6)
        self.icons[1].grid(row=1, column=3, padx=12, pady=6)

        self.vs.grid(row=2, column=1)
        self.vsFrame.grid(row=1, column=2)

        self.matchText.grid(row=2, column=1, columnspan=3)

        self.cancel.pack(padx=4,side=tk.RIGHT)
        self.submit.pack(side=tk.RIGHT)
        self.buttonFrame.grid(row=3, column=1, columnspan=3, pady=4, sticky=tk.E)


    def submit_match(self, data, setup):
        '''Submits match record and returns to setup'''
        if self.winner != None:
            self.match['win'] = self.winner
            data.record_match(self.match)

            self.top.destroy()
            setup.deiconify()
            setup.grab_set()


    def submit_confirm(self, data, setup):
        '''Adds additional confirm dialog to submit button'''
        self.submit['text'] = 'Confirm?'
        self.submit['command'] = lambda d=data, s=setup: self.submit_match(d,s)


    def reset_submit(self, data, setup):
        '''Resets submit button to before confirm'''
        self.submit['text'] = "Submit"
        self.submit['command'] = lambda d=data, s=setup: self.submit_confirm(d,s)


    def set_winner(self, data, setup, name, num):
        '''Accepts winner name and allows submitting record entry'''
        self.winner = name
        self.submit['state'] = tk.NORMAL
        self.reset_submit(data, setup)

        # Color buttons
        for p in self.icons:
            if p['text'] == name:
                p['background'] = 'dark orange'
                p['activebackground'] = 'dark orange'
            else:
                p['background'] = 'light gray'
                p['activebackground'] = 'light gray'


    def cancel_match(self, setup):
        '''Closes the match screen and refocuses match setup'''
        self.top.destroy()
        setup.deiconify()
        setup.grab_set()



class MatchAddEntry:
    def __init__(self, setup, data, missing, inactive):
        '''Window for quickly adding missing entries from match setup dialog'''
        self.top = tk.Toplevel(setup.top)
        self.top.title("Missing Entries")
        self.top.resizable(False,False)
        self.top.wm_attributes("-topmost", True)

        self.textFrame = tk.Frame(self.top)
        self.head = tk.Label(self.top, text='Entries for match are missing! \nWould you like to add them now?')
        msg = self.create_body_text(missing, inactive)
        self.body = tk.Label(self.textFrame, text=msg, justify=tk.LEFT, font="-size 8")

        self.buttonFrame = tk.Frame(self.top)
        self.add = tk.Button(self.buttonFrame, text="Add", width=6, command=lambda s=setup, d=data, m=missing, i=inactive: self.action(s,d,m,i))
        self.cancel = tk.Button(self.buttonFrame, text="Cancel", width=6, command=lambda s=setup: self.close(s))

        self.position()
        self.top.grab_set()


    def create_body_text(self, missing, inactive):
        '''Returns formated string for message body'''
        entryList = []
        for entry in missing + inactive:
            if entry[0] == 'game':
                entryList.append('- Game: ' + entry[1])
            elif entry[0] == 'player':
                entryList.append('- Player: ' + entry[1])

        return '\n'.join(sorted(entryList)) # Return as joined string


    def position(self):
        ''''Positions window elements'''
        self.head.pack(padx=6, pady=2)

        self.textFrame.pack(fill=tk.X, pady=2)
        self.body.pack(side=tk.LEFT, padx=24)

        self.cancel.pack(padx=4, pady=4, side=tk.RIGHT)
        self.add.pack(pady=4, side=tk.RIGHT)
        self.buttonFrame.pack()


    def action(self, setup, data, missing, inactive):
        '''Adds missing entries and begins match'''
        # Create new for missing
        for entry in missing:
            if entry[0] == 'game':
                data.new_game(entry[1])
            elif entry[0] == 'player':
                data.new_player(entry[1])

        # Activate inactive
        for entry in inactive:
            if entry[0] == 'game':
                data.activate_game(entry[1])
            elif entry[0] == 'player':
                data.activate_player(entry[1])

        # Clean-up, return to setup screen
        self.top.destroy()
        setup.refresh_lists(data)
        setup.top.deiconify()
        setup.top.grab_set()


    def close(self, setup):
        '''Destroys self.top and refocuses on MatchSetup'''
        self.top.destroy()
        setup.top.deiconify()
        setup.top.grab_set()



class MatchSetup:
    def open(self, root, data, menu):
        '''Match setup window'''
        self.top = tk.Toplevel(root)
        self.top.title("Match Setup")
        self.top.resizable(False,False)
        self.top.wm_attributes("-topmost", True)

        self.head = tk.Label(self.top, text="Select match options:")

        self.gameFrame = tk.Frame(self.top)
        self.playerFrame = tk.Frame(self.top)

        self.game = tk.StringVar()
        self.game.trace('w', self.start_callback)
        self.p1 = tk.StringVar()
        self.p1.trace('w', self.start_callback)
        self.p2 = tk.StringVar()
        self.p2.trace('w', self.start_callback)

        today = datetime.date.today()
        self.date = today.strftime("%Y-%m-%d")

        self.selectGame = ttk.Combobox(self.gameFrame, width=30, textvariable=self.game)
        self.selectP1 = ttk.Combobox(self.playerFrame, width=14, textvariable=self.p1)
        self.selectP2 = ttk.Combobox(self.playerFrame, width=14, textvariable=self.p2)

        self.refresh_lists(data)

        self.labelGame = tk.Label(self.gameFrame, text="Game:")
        self.labelP1 = tk.Label(self.playerFrame, text="Player 1:")
        self.labelP2 = tk.Label(self.playerFrame, text="Player 2:")

        self.tagP1 = tk.Button(self.playerFrame, text='Tag', width=8, height=1)
        self.tagP2 = tk.Button(self.playerFrame, text='Tag', width=8)

        self.separator=ttk.Separator(self.top, orient=tk.HORIZONTAL)

        self.buttonFrame = tk.Frame(self.top)
        self.start = tk.Button(self.buttonFrame, text="Start", width=8, state=tk.DISABLED, command=lambda  m=root,d=data,me=menu: self.action(m,d,me))
        self.cancel = tk.Button(self.buttonFrame, text="Cancel", width=8, command=self.top.destroy)

        self.top.bind('<Escape>', lambda x=0: self.cancel.invoke())
        self.top.bind('<Return>', lambda x=0: self.start.invoke())

        self.position()
        self.top.grab_set()


    def start_callback(self, *args):
        '''Checks if all fields are populated, prompts entry creation for missing entries'''
        valid = True

        if self.p1.get() == '' or self.p2.get() == '' or self.game.get() == '':
            valid = False
        elif self.p1.get() == self.p2.get():
            valid = False

        if valid:
            self.start['state'] = tk.NORMAL
        else:
            self.start['state'] = tk.DISABLED


    def refresh_lists(self, data):
        '''Refreshes the list of players/games'''
        self.gamesList = data.query.all_game_names(True)
        self.playersList = data.query.all_player_names(True)

        self.selectGame['values'] = sorted(self.gamesList)
        self.selectP1['values'] = self.playersList
        self.selectP2['values'] = self.playersList


    def position(self):
        '''Positions window elements'''
        self.head.pack(pady=4)

        self.gameFrame.pack(padx=12)
        self.labelGame.pack(side=tk.LEFT)
        self.selectGame.pack(side=tk.RIGHT)

        self.separator.pack(padx=32, pady=6, fill=tk.X, expand=True)

        self.labelP1.grid(row=1, column=1)
        self.selectP1.grid(row=1, column=2)
        #self.tagP1.grid(row=1, column=3, padx=12, pady=2)
        self.labelP2.grid(row=2, column=1)
        self.selectP2.grid(row=2, column=2, pady=4)
        #self.tagP2.grid(row=2, column=3, padx=12, pady=2)
        self.playerFrame.pack(padx=14, fill=tk.X)

        self.buttonFrame.pack(anchor=tk.E)
        self.cancel.pack(side=tk.RIGHT, padx=4, pady=4)
        self.start.pack(side=tk.RIGHT,pady=4)


    def check_missing(self, data):
        '''Initial check if any selection is missing/inactive from db, returns list of tuples describing missing items'''
        missing, inactive = [], []

        playerStatus = data.query.all_player_status()
        gameStatus = data.query.all_game_status()

        # Check game
        if self.game.get() in gameStatus.keys():
            if not gameStatus[self.game.get()]:
                inactive.append(('game', self.game.get()))
        else:
            missing.append(('game', self.game.get()))

        # Check P1
        if self.p1.get() in playerStatus.keys():
            if not playerStatus[self.p1.get()]:
                inactive.append(('player', self.p1.get()))
        else:
            missing.append(('player', self.p1.get()))

        # Check P2
        if self.p2.get() in playerStatus.keys():
            if not playerStatus[self.p2.get()]:
                inactive.append(('player', self.p2.get()))
        else:
            missing.append(('player', self.p2.get()))

        return missing, inactive


    def validate_missing(self, data, missing):
        '''Checks missing values are valid to prep adding to db, returns bool'''
        valid = True
        check = [self.game.get(), self.p1.get(), self.p2.get()]

        for entry in missing:
            if entry[0] == 'game':
                if data.validate_game_name(entry[1]):
                    valid = False
            elif entry[0] == 'player':
                if data.validate_player_name(entry[1]):
                    valid = False

        return valid


    def action(self, root, data, menu):
        '''Starts match, or prompts to add missing entries'''
        missing, inactive = self.check_missing(data)
        if missing != []: # Some entries missing
            if self.validate_missing(data, missing):
                self.message = MatchAddEntry(self, data, missing, inactive)
                self.top.withdraw()
            else:
                msg = "Unable to add missing entries.\nEntered names are invalid."
                self.message = Failure(self.top,msg)

        elif inactive != []: # No missing entries, but inactive
            self.message = MatchAddEntry(self, data, [], inactive)
            self.top.withdraw()

        else: # Match is ready to go
            match = {
                "game": self.game.get(),
                "p1": self.p1.get(),
                "p2": self.p2.get(),
                "date": self.date
            }
            menu.matchResults.open(root, data, match, self.top)
            self.top.withdraw()



class MatchRecords:
    def open(self, root, data):
        '''Match records display window'''
        self.top = tk.Toplevel(root)
        self.top.title("Match Records")

        self.mainFrame = tk.Frame(self.top)
        self.tree = self.build_tree(self.mainFrame, data)
        self.scrollbar = ttk.Scrollbar(self.mainFrame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.exit = tk.Button(self.top, width=8, text="Exit", command=self.top.destroy)

        self.position()


    def build_tree(self, root, data):
        '''Builds treeview widget'''
        tree = ttk.Treeview(root)
        tree['columns'] = ('d','p1','p2','w','g')
        tree['displaycolumns'] = ('d','p1','p2','w')

        tree.tag_configure('folder', background='light gray')
        tree.tag_configure('0', background='#E8E8E8')
        tree.tag_configure('1', background='#DFDFDF')

        tree.column('#0',width=150,minwidth=25)
        tree.column('d', width=100,minwidth=25)
        tree.column('p1',width=100,minwidth=25)
        tree.column('p2',width=100,minwidth=25)
        tree.column('w',width=100,minwidth=25)
        tree.column('g', width=200,minwidth=25)

        tree.heading('#0', text='Game', anchor=tk.W)
        tree.heading('d', text="Date",anchor=tk.W)
        tree.heading('p1', text="P1",anchor=tk.W)
        tree.heading('p2', text="P2",anchor=tk.W)
        tree.heading('w', text="Winner",anchor=tk.W)
        tree.heading('g', text="Game",anchor=tk.W)

        folders = {} # Holds folders for later match placement
        for f in data.query.match_folders():
            folders[f[1]] = tree.insert('', -1, text=f[1], tag='folder')

        for r in data.query.match_records("%","%","%"): # TODO: FILTER HERE
            tree.insert(folders[r[5]], -1, text=r[0], values=r[1:5], tag='1') #TODO: Fix row color tags

        return tree


    def position(self):
        '''Positions window elements'''
        self.mainFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.exit.pack(side=tk.RIGHT, padx=4, pady=4)
