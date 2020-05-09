import tkinter as tk
import tkinter.ttk as ttk
from src.message import *
import os, sys


class AddPlayer:
    def open(self, master, data):
        '''Opens the Add Player window'''
        self.top = tk.Toplevel(master)
        self.top.title("Add a Player")
        self.top.resizable(False,False)
        self.top.wm_attributes("-topmost", True)

        self.name = tk.StringVar()
        self.prompt = tk.Label(self.top, text="Player:")
        self.entry = tk.Entry(self.top, textvar=self.name)
        self.add = tk.Button(self.top, text="Add", width=8, command= lambda d=data: self.action(d))
        self.cancel = tk.Button(self.top, text="Cancel", width=8, command=self.top.destroy)

        self.top.bind('<Return>', lambda x=0:self.add.invoke())
        self.top.bind('<Escape>', lambda x=0:self.cancel.invoke())

        self.position()
        self.top.grab_set()
        self.entry.focus()


    def position(self):
        '''Positions window elements'''
        self.prompt.grid(row=2, column=1, padx=4, pady=4, sticky=tk.W)
        self.entry.grid(row=2, column=2, columnspan=2, pady=4, sticky=tk.W)
        self.add.grid(row=3, column=2, pady=4)
        self.cancel.grid(row=3, column=3, padx=4, pady=4)


    def action(self, data):
        '''Conducts the action of the "Add" button'''
        name = self.entry.get()
        inv = data.players.invalidate_name(name)
        self.top.unbind('<Return>') # TODO - better solution for Windows not focusing pop-up

        if name == '': # No name entered
            pass

        elif inv == 0: # Name is valid
            data.players.add(name)
            data.players.save()
            msg = 'Player "{}" has been added'.format(name)
            self.message = Success(self.top, msg)

        elif inv == 1: # Name already in-use
            msg = 'Name "{}" already in-use'.format(name)
            self.message = Failure(self.top, msg)

        elif inv == 2: # Name is on list of reserved names
            msg = 'Name "{}" is not allowed'.format(name)
            self.message = Failure(self.top, msg)

        elif inv == 3: # Name contains an illegal character
            msg = 'Name "{}" contains illegal characters'.format(name)
            self.message = Failure(self.top, msg)

        elif inv == 4: # Name greater than 14 characters
            msg = 'Name "{}" is too long. Max = 14 characters'.format(name)
            self.message = Failure(self.top, msg)

        else:
            msg = 'Error adding player'
            self.message = Failure(self.top, msg)



class AddGame:
    def open(self, master, data):
        '''Opens the Add Game window'''
        self.top = tk.Toplevel(master)
        self.top.title("Add a Game")
        self.top.resizable(False,False)
        self.top.wm_attributes("-topmost", True)

        self.name = tk.StringVar()
        self.prompt = tk.Label(self.top, text="Game:")
        self.entry = tk.Entry(self.top, textvar=self.name)
        self.add = tk.Button(self.top, text="Add", width=8, command= lambda d=data: self.action(d))
        self.cancel = tk.Button(self.top, text="Cancel", width=8, command=self.top.destroy)

        self.top.bind('<Return>', lambda x=0:self.add.invoke())
        self.top.bind('<Escape>', lambda x=0:self.cancel.invoke())

        self.position()
        self.top.grab_set()
        self.entry.focus()

    def position(self):
        '''Positions window elements'''
        self.prompt.grid(row=2, column=1, padx=4, pady=4, sticky=tk.W)
        self.entry.grid(row=2, column=2, columnspan=2, pady=4, sticky=tk.W)
        self.add.grid(row=3, column=2, pady=4)
        self.cancel.grid(row=3, column=3, padx=4, pady=4)



    def action(self, data):
        '''Conducts the action of the "Add" button'''
        name = self.entry.get()
        inv = data.games.invalidate_name(name)
        self.top.unbind('<Return>') # TODO - better solution for Windows not focusing pop-up

        if name == '': # No name entered
            pass

        elif inv == 0: # Name is valid
            data.games.add(name)
            data.games.save()
            msg = 'Game "{}" has been added'.format(name)
            self.message = Success(self.top, msg)

        elif inv == 1: # Name already in-use
            msg = 'Name "{}" already in-use'.format(name)
            self.message = Failure(self.top, msg)

        elif inv == 2: # Name is on list of reserved names
            msg = 'Name "{}" is not allowed'.format(name)
            self.message = Failure(self.top, msg)

        elif inv == 3: # Name contains an illegal character
            msg = 'Name "{}" contains illegal characters'.format(name)
            self.message = Failure(self.top, msg)

        elif inv == 4: # Name greater than 30 characters
            msg = 'Name "{}" is too long. Max = 30 characters'.format(name)
            self.message = Failure(self.top, msg)

        else:
            msg = 'Error adding game'
            self.message = Failure(self.top, msg)



class RemovePlayer:
    def open(self, master, data):
        '''Opens the Add Game window'''
        if not len(data.players.all):
            msg = "No players found"
            self.message = Failure(master, msg)

        else:
            self.top = tk.Toplevel(master)
            self.top.title("Remove a Player")
            self.top.resizable(False,False)
            self.top.wm_attributes("-topmost", True)

            self.name = tk.StringVar()
            self.prompt = tk.Label(self.top, text="Player:")
            self.select = tk.OptionMenu(self.top, self.name, *data.players.all.keys())
            self.rm = tk.Button(self.top, text="Remove", width=8, command= lambda d=data: self.action(d))
            self.cancel = tk.Button(self.top, text="Cancel", width=8, command=self.top.destroy)

            self.top.bind('<Escape>', lambda x=0:self.cancel.invoke())

            self.position()
            self.top.grab_set()


    def position(self):
        '''Positions window elements'''
        self.prompt.grid(row=2, column=1, padx=4, sticky=tk.W)
        self.select.grid(row=2, column=2, columnspan=2, pady=4, sticky=tk.W + tk.E)
        self.rm.grid(row=3, column=2, pady=4)
        self.cancel.grid(row=3, column=3, padx=4, pady=4)


    def action(self, data):
        '''Conducts the action of the "Remove" button'''
        name = self.name.get()

        if name == '': # No name entered
            pass

        elif name in data.players.all.keys():
            data.players.remove(name)
            data.players.save()
            msg = "Player {} has been removed".format(name)
            self.message = Success(self.top, msg)

        else:
            msg = "Error removing player"
            self.message = Failure(self.top, msg)



class RemoveGame:
    def open(self, master, data):
        '''Opens the Remove Game window'''
        if not len(data.games.all):
            msg = "No games found"
            self.message = Failure(master, msg)

        else:
            self.top = tk.Toplevel(master)
            self.top.title("Remove a Game")
            self.top.resizable(False,False)
            self.top.wm_attributes("-topmost", True)

            self.name = tk.StringVar()
            self.prompt = tk.Label(self.top, text="Game:")
            self.select = tk.OptionMenu(self.top, self.name, *data.games.all.keys())
            self.rm = tk.Button(self.top, text="Remove", width=8, command= lambda d=data: self.action(d))
            self.cancel = tk.Button(self.top, text="Cancel", width=8, command=self.top.destroy)

            self.top.bind('<Escape>', lambda x=0:self.cancel.invoke())

            self.position()
            self.top.grab_set()


    def position(self):
        '''Positions window elements'''
        self.prompt.grid(row=2, column=1, padx=4, sticky=tk.W)
        self.select.grid(row=2, column=2, columnspan=2, pady=4, sticky=tk.W + tk.E)
        self.rm.grid(row=3, column=2, pady=4)
        self.cancel.grid(row=3, column=3, padx=4, pady=4)


    def action(self, data):
        '''Conducts the action of the "Remove" button'''
        name = self.name.get()

        if name == '': # No name entered
            pass

        elif name in data.games.all.keys():
            data.games.remove(name)
            data.games.save()
            msg = "{} has been removed from the game list".format(name)
            self.message = Success(self.top, msg)

        else:
            msg = "Error removing game"
            self.message = Failure(self.top, msg)
