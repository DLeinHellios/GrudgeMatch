import tkinter as tk
import tkinter.ttk as ttk
from src.message import *
import os, datetime


class MatchResults:
    def open(self, master, data, match, setup):
        '''Selects the winner of the match and submits the results'''
        self.top = tk.Toplevel(master)
        self.top.title("Ongoing Match")
        self.top.resizable(False,False)
        self.top.wm_attributes("-topmost", True)

        today = datetime.date.today()
        self.match = [today.strftime("%m/%d/%Y")] + match

        self.avatars,self.icons = [],[]
        self.load_players(data, setup, match[1],match[2])

        self.vsFrame = tk.Frame(self.top)
        self.vsImage = tk.PhotoImage(master=self.top, file=os.path.join('img', 'vs.png'))
        self.vs = tk.Label(master=self.vsFrame, image=self.vsImage)

        self.matchText = tk.Label(master=self.top, text=self.match[1] + '\n' + self.match[0])
        self.winner = None

        self.buttonFrame = tk.Frame(self.top)
        self.submit = tk.Button(self.buttonFrame, text="Submit", width=8, state=tk.DISABLED, command=lambda d=data,s=setup: self.submit_confirm(d,s))
        self.cancel = tk.Button(self.buttonFrame, text="Cancel", width=8, command=lambda s=setup: self.cancel_match(s))

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
            self.match.append(self.winner)
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
    def __init__(self, master, data, additions):
        '''Window for quickly adding missing entries from match setup dialog'''
        self.top = tk.Toplevel(master)
        self.top.title("Missing Entries")
        self.top.resizable(False,False)
        self.top.wm_attributes("-topmost", True)

        self.textFrame = tk.Frame(self.top)
        self.head = tk.Label(self.top, text='Entries for match are missing! \nWould you like to add them now?')
        msg = self.create_body_text(additions)
        self.body = tk.Label(self.textFrame, text=msg, justify=tk.LEFT, font="-size 8")

        self.buttonFrame = tk.Frame(self.top)
        self.add = tk.Button(self.buttonFrame, text="Add", width=6, command=lambda m=master, d=data, a=additions: self.action(m,d,a))
        self.cancel = tk.Button(self.buttonFrame, text="Cancel", width=6, command=lambda m=master: self.close(m))

        self.top.bind('<Return>', lambda x=0:self.add.invoke())

        self.position()
        self.top.grab_set()


    def create_body_text(self, additions):
        '''Returns formated string for message body'''
        entryList = []
        if 'g' in additions.keys():
            entryList.append('- Game: ' + additions['g'])
        if 'p1' in additions.keys():
            entryList.append('- Player: ' + additions['p1'])
        if 'p2' in additions.keys():
            entryList.append('- Player: ' + additions['p2'])

        return '\n'.join(entryList)


    def position(self):
        ''''Positions window elements'''
        self.head.pack(padx=6, pady=2)

        self.textFrame.pack(fill=tk.X, pady=2)
        self.body.pack(side=tk.LEFT, padx=24)

        self.cancel.pack(padx=4, pady=4, side=tk.RIGHT)
        self.add.pack(pady=4, side=tk.RIGHT)
        self.buttonFrame.pack()


    def action(self, master, data, additions):
        '''Adds missing entries and begins match'''
        for key, value in additions.items():
            if key == 'g':
                data.games.add(value)
            elif key[0] == 'p':
                data.players.add(value)

        data.save_all()
        self.top.destroy()
        master.deiconify()
        master.grab_set()


    def close(self, master):
        '''Destroys self.top and refocuses on MatchSetup'''
        self.top.destroy()
        master.deiconify()
        master.grab_set()



class MatchSetup:
    def open(self, master, data, menu):
        '''Match setup window'''
        if len(data.players.all) > 1 and len(data.games.all) > 0:
            self.top = tk.Toplevel(master)
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

            self.selectGame = ttk.Combobox(self.gameFrame, width=30, textvariable=self.game)
            self.selectP1 = ttk.Combobox(self.playerFrame, width=14, textvariable=self.p1)
            self.selectP2 = ttk.Combobox(self.playerFrame, width=14, textvariable=self.p2)

            self.selectGame['values'] = list(data.games.all.keys())
            self.selectP1['values'] = list(data.players.all.keys())
            self.selectP2['values'] = list(data.players.all.keys())

            self.labelGame = tk.Label(self.gameFrame, text="Game:")
            self.labelP1 = tk.Label(self.playerFrame, text="Player 1:")
            self.labelP2 = tk.Label(self.playerFrame, text="Player 2:")

            self.tagP1 = tk.Button(self.playerFrame, text='Tag', width=8, height=1)
            self.tagP2 = tk.Button(self.playerFrame, text='Tag', width=8)

            self.separator=ttk.Separator(self.top, orient=tk.HORIZONTAL)

            self.buttonFrame = tk.Frame(self.top)
            self.start = tk.Button(self.buttonFrame, text="Start", width=8, state=tk.DISABLED, command=lambda  m=master,d=data,me=menu: self.action(m,d,me))
            self.cancel = tk.Button(self.buttonFrame, text="Cancel", width=8, command=self.top.destroy)

            self.top.bind('<Escape>', lambda x=0: self.cancel.invoke())
            self.top.bind('<Return>', lambda x=0: self.start.invoke())

            self.position()
            self.top.grab_set()

        else:
            msg = "You must add at least one game and two \nplayers before running a match"
            self.message = Failure(master, msg)


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
        '''Checks if entries from comboboxes are missing from data'''
        missing = False
        if self.game.get() not in data.games.all.keys():
            missing = True
        if self.p1.get() not in data.players.all.keys():
            missing = True
        if self.p2.get() not in data.players.all.keys():
            missing = True

        return missing


    def validate_missing(self, data):
        '''Validates the names entered, but missing'''
        valid = True
        g = self.game.get()
        p1 = self.p1.get()
        p2 = self.p2.get()

        if g not in data.games.all.keys() and data.games.invalidate_name(g):
            valid = False
        elif p1 not in data.players.all.keys() and data.players.invalidate_name(p1):
            valid = False
        elif p2 not in data.players.all.keys() and data.players.invalidate_name(p2):
            valid = False

        return valid


    def add_missing(self, data, menu):
        '''Creates dialog to confirm automatic adding of missing game/player entries'''
        addEntries = {}
        if self.game.get() not in data.games.all.keys():
            addEntries['g'] = self.game.get()
        if self.p1.get() not in data.players.all.keys():
            addEntries['p1'] = self.p1.get()
        if self.p2.get() not in data.players.all.keys():
            addEntries['p2'] = self.p2.get()

        self.message = MatchAddEntry(self.top, data, addEntries)
        self.top.withdraw()


    def action(self, master, data, menu):
        '''Starts match, or prompts to add missing entries'''
        if self.check_missing(data):
            if self.validate_missing(data):
                self.add_missing(data, menu)
            else:
                msg = "Unable to add missing entries.\nEntered names are invalid."
                self.message = Failure(self.top,msg)
        else:
            match = [self.game.get(),self.p1.get(),self.p2.get()]
            menu.matchResults.open(master, data, match, self.top)
            self.top.withdraw()
