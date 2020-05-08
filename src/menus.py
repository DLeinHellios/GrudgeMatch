import tkinter as tk
import tkinter.ttk as ttk
from src.message import *
import os, sys


class Rebuild:
    def open(self, master, data):
        '''Opens the rebuild data confirmation window'''
        self.top = tk.Toplevel(master)
        self.top.title("Rebuild Player/Game Entries")
        self.top.resizable(False,False)
        self.top.wm_attributes("-topmost", True)

        self.title = tk.Label(self.top, text="Rebuild Player/Game Entries", font="-size 10")
        msg = "- Players and games with no recorded matches will be removed \n- All players and games with recorded matches will be re-added\n"
        self.text = tk.Label(self.top, text=msg, font="-size 8", justify=tk.LEFT)

        self.confirm = tk.Button(self.top, text="Confirm", width=8, command= lambda d=data: self.action(d))
        self.cancel = tk.Button(self.top, text="Cancel", width=8, command=self.top.destroy)

        self.top.bind('<Escape>', lambda x=0:self.cancel.invoke())

        self.position()
        self.top.grab_set()


    def position(self):
        '''Positions window elements'''
        self.title.pack()
        self.text.pack(padx=12)
        self.cancel.pack(side=tk.RIGHT)
        self.confirm.pack(side=tk.RIGHT)


    def action(self, data):
        '''Confirm button action - calls data methods to rebuild p/g'''
        err = data.rebuild()

        if not err:
            msg = "Data has been successfully rebuilt"
            self.message = Success(self.top, msg)

        elif err == 1:
            msg = "Error - Cannot open records file"
            self.message = Failure(self.top, msg)

        else:
            msg = "An error occured while rebuilding"
            self.message=Failure(self.top, msg)
