import tkinter as tk
import tkinter.ttk as ttk
from src.message import *
import os, sys


class AddPlayer:
    def open(self, manage, data):
        '''Opens the Add Player window'''
        self.top = tk.Toplevel(manage.top)
        self.top.title("Add Player")
        self.top.resizable(False,False)
        self.top.wm_attributes("-topmost", True)

        self.text = tk.Label(self.top, text="Add a new player:")
        self.promptFrame = tk.Frame(self.top)
        self.name = tk.StringVar()
        self.prompt = tk.Label(self.promptFrame, text="Player:")
        self.entry = tk.Entry(self.promptFrame, textvar=self.name, width=14)
        self.add = tk.Button(self.top, text="Add", width=8, command= lambda m=manage, d=data: self.action(m,d))
        self.cancel = tk.Button(self.top, text="Cancel", width=8, command=self.top.destroy)

        self.top.bind('<Return>', lambda x=0:self.add.invoke())
        self.top.bind('<Escape>', lambda x=0:self.cancel.invoke())

        self.position()
        self.entry.focus()


    def position(self):
        '''Positions window elements'''
        self.text.pack(side=tk.TOP, pady=4)

        self.promptFrame.pack(padx=4)
        self.prompt.pack(side=tk.LEFT)
        self.entry.pack(side=tk.RIGHT)

        self.add.pack(side=tk.LEFT, padx=4, pady=4)
        self.cancel.pack(side=tk.RIGHT, padx=4, pady=4)


    def action(self, manage, data):
        '''Conducts the action of the "Add" button'''
        name = self.entry.get()
        err = data.validate_player_name(name)
        self.top.unbind('<Return>')

        if name == '': # No name entered
            pass

        elif err == 0: # Name is valid
            data.new_player(name)
            msg = 'Player "{}" has been added'.format(name)
            self.message = Success(self.top, msg)
            manage.refresh_tree(data)

        elif err == 1: # Name already in-use
            msg = 'Name "{}" already in-use'.format(name)
            self.message = Failure(self.top, msg)

        elif err == 2: # Name is currently inactive, enable
            data.activate_player(name)
            msg = 'Player "{}" is now active'.format(name)
            self.message = Success(self.top, msg)
            manage.refresh_tree(data)

        elif err == 3: # Name is on list of reserved names
            msg = 'Name "{}" is not allowed'.format(name)
            self.message = Failure(self.top, msg)

        elif err == 4: # Name greater than 14 characters
            msg = 'Name "{}" is too long. Max = 10 characters'.format(name)
            self.message = Failure(self.top, msg)

        elif err == 5: # Name contains an illegal character
            msg = 'Name "{}" contains illegal characters'.format(name)
            self.message = Failure(self.top, msg)

        else:
            msg = 'Error adding player'
            self.message = Failure(self.top, msg)



class RemovePlayer:
    def open(self, manage, data):
        '''Opens the Remove Player window'''
        if not len(data.query.all_player_names(True)):
            msg = "No players found"
            self.message = Failure(manage.top, msg)

        else:
            # References to manage window and data object
            self.manage = manage
            self.data = data

            self.top = tk.Toplevel(self.manage.top)
            self.top.title("Remove Player")
            self.top.resizable(False,False)
            self.top.wm_attributes("-topmost", True)

            self.text = tk.Label(self.top, text="Select a player to remove:")

            self.promptFrame = tk.Frame(self.top)
            self.playerName = tk.StringVar()
            self.playerName.trace('w', self.reset_confirm)
            self.prompt = tk.Label(self.promptFrame, text="Player:")
            self.select = ttk.Combobox(self.promptFrame, width=14, textvariable=self.playerName)
            self.select['values'] = data.query.all_player_names(True)

            self.remove = tk.Button(self.top, text="Remove", width=8, command=self.confirm)
            self.cancel = tk.Button(self.top, text="Cancel", width=8, command=self.top.destroy)

            self.top.bind('<Return>', lambda x=0:self.remove.invoke())
            self.top.bind('<Escape>', lambda x=0:self.cancel.invoke())

            self.position()
            self.select.focus()


    def position(self):
        '''Positions window elements'''
        self.text.pack(side=tk.TOP, pady=4)

        self.promptFrame.pack(padx=4)
        self.prompt.pack(side=tk.LEFT)
        self.select.pack(side=tk.RIGHT)

        self.remove.pack(side=tk.LEFT, padx=4, pady=4)
        self.cancel.pack(side=tk.RIGHT, padx=4, pady=4)


    def reset_confirm(self, *args):
        '''Resets remove button'''
        self.remove['text'] = 'Remove'
        self.remove['command'] = self.confirm


    def confirm(self):
        '''Adds additional confirm dialog to remove button'''
        name = self.playerName.get()
        if name != '' and name in self.data.query.all_player_names(True):
            self.remove['text'] = 'Confirm?'
            self.remove['command'] = self.action


    def action(self):
        '''Conducts the action of the "Remove" button'''
        name = self.playerName.get()

        if name == '': # No name entered
            pass

        elif name in self.data.query.all_player_names(True):
            self.data.deactivate_player(name)
            msg = "Player {} has been removed".format(name)
            self.manage.refresh_tree(self.data)
            self.message = Success(self.top, msg)

        else:
            msg = "Error removing player"
            self.message = Failure(self.top, msg)



class ManagePlayers:
    def __init__(self):
        '''Top-level window for player management'''
        self.add = AddPlayer()
        self.remove = RemovePlayer()


    def open(self, root, data):
        '''Opens player management window'''
        self.top = tk.Toplevel(root)
        self.top.title("Manage Players")
        self.top.wm_attributes("-topmost", True)

        self.mainFrame = tk.Frame(self.top)
        self.tree = self.build_tree(self.mainFrame, data)
        self.scrollbar = ttk.Scrollbar(self.mainFrame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.sideFrame = tk.Frame(self.top, width=80)
        self.addButton = tk.Button(self.sideFrame, text="Add", command=lambda m=self, d=data: self.add.open(m,d))
        self.remButton = tk.Button(self.sideFrame, text="Remove", command=lambda m=self, d=data: self.remove.open(m,d))
        self.refresh = tk.Button(self.sideFrame, text="Refresh", command=lambda d=data: self.refresh_tree(d))
        self.exit = tk.Button(self.sideFrame, text="Exit", command=self.top.destroy)

        self.top.bind('<Escape>', lambda x=0:self.exit.invoke())

        self.position()
        self.top.grab_set()


    def build_tree(self, root, data):
        '''Builds player data tree'''
        tree = ttk.Treeview(root)
        tree['columns'] = ('wins','matches','last')

        tree.tag_configure('0', background='#E8E8E8')
        tree.tag_configure('1', background='#DFDFDF')

        tree.column('#0',width=100)
        tree.column('wins',width=60)
        tree.column('matches',width=80)
        tree.column('last',width=80)

        tree.heading('#0', text='Player', anchor=tk.W)
        tree.heading('wins', text='Wins', anchor=tk.W)
        tree.heading('matches', text='Matches', anchor=tk.W)
        tree.heading('last', text='Last', anchor=tk.W)

        c = 0
        for p in data.query.all_player_details(True):
            tree.insert('', tk.END, text=p[1], values=[p[2],p[3],p[4]], tag=str(c%2))
            c += 1

        return tree


    def refresh_tree(self, data):
        '''Rebuilds and re-packs the tree'''
        self.tree.destroy()
        self.tree = self.build_tree(self.mainFrame, data)
        self.scrollbar.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


    def position(self):
        '''Positions window elements'''
        self.mainFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.sideFrame.pack(side=tk.RIGHT,fill=tk.Y)
        self.sideFrame.pack_propagate(0)
        self.addButton.pack(side=tk.TOP,fill=tk.X)
        self.remButton.pack(side=tk.TOP,fill=tk.X)
        self.exit.pack(side=tk.BOTTOM,fill=tk.X)
        self.refresh.pack(side=tk.BOTTOM, fill=tk.X)



class AddGame:
    def open(self, manage, data):
        '''Opens the Add Game window'''
        self.manage = manage
        self.data = data

        self.top = tk.Toplevel(manage.top)
        self.top.title("Add Game")
        self.top.resizable(False,False)

        self.text = tk.Label(self.top, text="Add a new game:")
        self.promptFrame = tk.Frame(self.top)
        self.nameVar = tk.StringVar()
        self.nameVar.trace('w', self.reset_name_entry)
        self.nameLabel = tk.Label(self.promptFrame, text="Name:")
        self.nameEntry = tk.Entry(self.promptFrame, textvar=self.nameVar, width=18)
        self.devVar = tk.StringVar()
        self.devLabel = tk.Label(self.promptFrame, text="Developer:")
        self.devEntry = tk.Entry(self.promptFrame, textvar=self.devVar, width=18)
        self.platformVar = tk.StringVar()
        self.platformLabel = tk.Label(self.promptFrame, text="Platform:")
        self.platformEntry = tk.Entry(self.promptFrame, textvar=self.platformVar, width=18)
        self.yearVar = tk.StringVar()
        self.yearLabel = tk.Label(self.promptFrame, text="Release Year:")
        self.yearEntry = tk.Entry(self.promptFrame, textvar=self.yearVar, width=18)

        self.add = tk.Button(self.top, text="Add", width=8, command= self.action)
        self.cancel = tk.Button(self.top, text="Cancel", width=8, command=self.top.destroy)

        self.top.bind('<Return>', lambda x=0:self.add.invoke())
        self.top.bind('<Escape>', lambda x=0:self.cancel.invoke())

        self.position()
        self.top.grab_set()
        self.nameEntry.focus()


    def position(self):
        '''Positions window elements'''
        self.text.pack(side=tk.TOP, pady=4)

        self.promptFrame.pack(padx=4)
        self.nameLabel.grid(row=1, column=1, padx=2, pady=2)
        self.nameEntry.grid(row=1, column=2, padx=2, pady=2)

        self.devLabel.grid(row=2, column=1, padx=2, pady=2)
        self.devEntry.grid(row=2, column=2, padx=2, pady=2)

        self.platformLabel.grid(row=3, column=1, padx=2, pady=2)
        self.platformEntry.grid(row=3, column=2, padx=2, pady=2)

        self.yearLabel.grid(row=4, column=1, padx=2, pady=2)
        self.yearEntry.grid(row=4, column=2, padx=2, pady=2)

        self.add.pack(side=tk.LEFT, padx=4, pady=4)
        self.cancel.pack(side=tk.RIGHT, padx=4, pady=4)


    def reset_name_entry(self, *args):
        '''Resets name entry bg color'''
        self.nameEntry.config(bg='white')


    def action(self):
        '''Conducts the action of the "Add" button'''
        name = self.nameVar.get()
        developer = self.devVar.get()
        platform = self.platformVar.get()

        # Release year to int
        try:
            release = int(self.yearVar.get())

        except:
            release = None

        # Fix blank values
        if developer == '':
            developer = None

        if platform == '':
            platform = None

        # Validate name and proceed
        err = self.data.validate_game_name(name)
        self.top.unbind('<Return>') # TODO - better solution for Windows not focusing pop-up

        if name == '': # No name entered
            self.nameEntry.config(bg='red2')

        elif err == 0: # Name is valid
            self.data.new_game(name, developer, platform, release)
            msg = 'Game "{}" has been added'.format(name)
            self.manage.refresh_tree(self.data)
            self.message = Success(self.top, msg)

        elif err == 1: # Name already in-use
            msg = 'Name "{}" already in-use'.format(name)
            self.message = Failure(self.top, msg)
            self.nameEntry.config(bg='red2')

        elif err == 2: # Name is currently inactive, enable
            self.data.activate_game(name)
            msg = 'Game "{}" has been reactivated.\nPlease update game information with the edit function'.format(name)
            self.message = Success(self.top, msg)
            self.manage.refresh_tree(self.data)

        elif err == 3: # Name is on list of reserved names
            msg = 'Name "{}" is not allowed'.format(name)
            self.message = Failure(self.top, msg)
            self.nameEntry.config(bg='red2')

        elif err == 4: # Name contains an illegal character
            msg = 'Name "{}" contains illegal characters'.format(name)
            self.message = Failure(self.top, msg)
            self.nameEntry.config(bg='red2')

        elif err == 5: # Name greater than 30 characters
            msg = 'Name "{}" is too long. Max = 30 characters'.format(name)
            self.message = Failure(self.top, msg)
            self.nameEntry.config(bg='red2')

        else:
            msg = 'Error adding game'
            self.message = Failure(self.top, msg)



class EditGame:
    def open(self, manage, data):
        self.manage = manage
        self.data = data
        self.selected = manage.get_selection()
        self.info = data.query.game_info(self.selected['text'])

        self.top = tk.Toplevel(self.manage.top)
        self.top.title("Edit Game")
        self.top.resizable(False,False)

        self.text = tk.Label(self.top, text="Editing game: {}".format(self.selected['text']))
        self.promptFrame = tk.Frame(self.top)

        self.devVar = tk.StringVar()
        self.devLabel = tk.Label(self.promptFrame, text="Developer:")
        self.devEntry = tk.Entry(self.promptFrame, textvar=self.devVar, width=18)

        self.platformVar = tk.StringVar()
        self.platformLabel = tk.Label(self.promptFrame, text="Platform:")
        self.platformEntry = tk.Entry(self.promptFrame, textvar=self.platformVar, width=18)

        self.yearVar = tk.StringVar()
        self.yearLabel = tk.Label(self.promptFrame, text="Release Year:")
        self.yearEntry = tk.Entry(self.promptFrame, textvar=self.yearVar, width=18)

        self.populate_fields()

        self.update = tk.Button(self.top, text="Update", width=8, command=self.action)
        self.cancel = tk.Button(self.top, text="Cancel", width=8, command=self.top.destroy)

        self.top.bind('<Return>', lambda x=0:self.update.invoke())
        self.top.bind('<Escape>', lambda x=0:self.cancel.invoke())

        self.position()
        self.top.grab_set()


    def position(self):
        '''Positions window elements'''
        self.text.pack(side=tk.TOP, pady=4)

        self.promptFrame.pack(padx=4)

        self.devLabel.grid(row=2, column=1, padx=2, pady=2)
        self.devEntry.grid(row=2, column=2, padx=2, pady=2)

        self.platformLabel.grid(row=3, column=1, padx=2, pady=2)
        self.platformEntry.grid(row=3, column=2, padx=2, pady=2)

        self.yearLabel.grid(row=4, column=1, padx=2, pady=2)
        self.yearEntry.grid(row=4, column=2, padx=2, pady=2)

        self.update.pack(side=tk.LEFT, padx=4, pady=4)
        self.cancel.pack(side=tk.RIGHT, padx=4, pady=4)


    def populate_fields(self):
        '''Fills info fields with existing data'''
        # Prepare values
        dev = self.info[0]
        platform = self.info[1]
        year = self.info[2]

        if dev == None:
            dev = ''
        if platform == None:
            platform = ''
        if year == None:
            year = ''

        # Set values
        self.devVar.set(dev)
        self.platformVar.set(platform)
        self.yearVar.set(year)


    def action(self):
        '''Updates game info in db, for Update button press'''
        # Prepare values
        dev = self.devVar.get()
        platform = self.platformVar.get()
        year = self.yearVar.get()

        if dev == '':
            dev = None

        if platform == '':
            platform = None

        try:
            year = int(year)
        except:
            year = None

        # Update db
        self.data.update_game_info(self.selected['text'], [dev,platform,year])

        self.top.destroy()



class RemoveGame:
    def open(self, manage, data):
        '''Opens the Remove Game window'''
        self.manage = manage
        self.data = data
        self.selected = manage.get_selection()

        self.top = tk.Toplevel(self.manage.top)
        self.top.title("Remove Game")
        self.top.resizable(False,False)

        self.text = tk.Label(self.top, text="Remove game: {}?".format(self.selected['text']))
        self.remove = tk.Button(self.top, text="Remove", width=8, command=self.confirm)
        self.cancel = tk.Button(self.top, text="Cancel", width=8, command=self.top.destroy)

        self.top.bind('<Return>', lambda x=0:self.remove.invoke())
        self.top.bind('<Escape>', lambda x=0:self.cancel.invoke())

        self.position()
        self.top.grab_set()


    def position(self):
        '''Positions window elements'''
        self.text.pack(side=tk.TOP, padx=4, pady=4)
        self.cancel.pack(side=tk.RIGHT, padx=4, pady=4)
        self.remove.pack(side=tk.RIGHT, padx=4)


    def confirm(self):
        '''Adds additional confirm dialog to remove button'''
        name = self.selected['text']
        if name != '' and name in self.data.query.all_game_names(True):
            self.remove['text'] = 'Confirm?'
            self.remove['command'] = self.action


    def action(self):
        '''Conducts the action of the "Remove" button'''
        name = self.selected['text']

        if name in self.data.query.all_game_names(True):
            self.data.deactivate_game(name)
            msg = "{} has been removed".format(name)
            self.manage.refresh_tree(self.data)
            self.message = Success(self.top, msg)

        else:
            msg = "Error removing game"
            self.message = Failure(self.top, msg)



class ManageGames:
    def __init__(self):
        '''Top-level window for game management'''
        self.add = AddGame()
        self.edit = EditGame()
        self.remove = RemoveGame()


    def open(self, root, data):
        '''Opens data management window'''
        self.top = tk.Toplevel(root)
        self.top.title("Manage Games")
        self.top.minsize(450,250)

        # Use these later, remove pointless args
        self.root = root
        self.data = data

        self.mainFrame = tk.Frame(self.top)
        self.tree = self.build_tree(self.mainFrame, data)
        self.scrollbar = ttk.Scrollbar(self.mainFrame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.sideFrame = tk.Frame(self.top, width=80)
        self.addButton = tk.Button(self.sideFrame, text="Add", command=lambda m=self, d=data: self.add.open(m,d))
        self.editButton = tk.Button(self.sideFrame, text="Edit", command=lambda m=self, d=data: self.edit.open(m,d))
        self.remButton = tk.Button(self.sideFrame, text="Remove", command=lambda m=self, d=data: self.remove.open(m,d))
        self.refresh = tk.Button(self.sideFrame, text="Refresh", command=lambda d=data: self.refresh_tree(d))
        self.exit = tk.Button(self.sideFrame, text="Exit", command=self.top.destroy)

        self.tree.bind('<<TreeviewSelect>>', self.check_selection)
        self.top.bind('<Escape>', lambda x=0:self.exit.invoke())

        self.position()
        self.check_selection()


    def build_tree(self, root, data):
        '''Builds game data tree'''
        tree = ttk.Treeview(root)
        tree['columns'] = ('matches','last')

        tree.tag_configure('0', background='#E8E8E8')
        tree.tag_configure('1', background='#DFDFDF')

        tree.column('#0',width=180)
        tree.column('matches',width=80)
        tree.column('last',width=80)

        tree.heading('#0', text='Game', anchor=tk.W)
        tree.heading('matches', text='Matches', anchor=tk.W)
        tree.heading('last', text='Last', anchor=tk.W)

        c = 0
        for g in data.query.all_game_details(True):
            tree.insert('', tk.END, text=g[1], values=[g[2],g[3]], tag=str(c%2))
            c += 1

        return tree


    def refresh_tree(self, data):
        '''Rebuilds and re-packs the tree'''
        self.tree.destroy()
        self.tree = self.build_tree(self.mainFrame, data)
        self.scrollbar.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.check_selection()
        self.tree.bind('<<TreeviewSelect>>', self.check_selection)


    def position(self):
        '''Positions window elements'''
        self.mainFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.sideFrame.pack(side=tk.RIGHT,fill=tk.Y)
        self.sideFrame.pack_propagate(0)
        self.addButton.pack(side=tk.TOP,fill=tk.X)
        self.editButton.pack(side=tk.TOP,fill=tk.X)
        self.remButton.pack(side=tk.TOP,fill=tk.X)
        self.exit.pack(side=tk.BOTTOM,fill=tk.X)
        self.refresh.pack(side=tk.BOTTOM, fill=tk.X)


    def check_selection(self, *args):
        '''Checks if game is selected, enables/disables edit and remove buttons'''
        selected = self.tree.selection()

        if len(selected) == 1:
            self.editButton['state'] = tk.NORMAL
            self.remButton['state'] = tk.NORMAL

        else:
            self.editButton['state'] = tk.DISABLED
            self.remButton['state'] = tk.DISABLED


    def get_selection(self):
        '''Returns currently selected single row as treeview item'''
        selected = self.tree.focus()
        item = self.tree.item(selected)

        return item
