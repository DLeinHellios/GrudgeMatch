import tkinter as tk
import tkinter.ttk as ttk
import os


class Success:
    def __init__(self, root, message):
        '''A success pop-up that closes its root window when toplevel is closed'''
        self.top = tk.Toplevel(root)
        self.top.title("Success")
        self.top.resizable(False,False)
        self.top.wm_attributes("-topmost", True)

        self.text = tk.Label(self.top, text=message)
        self.ok = tk.Button(self.top, text="Ok", width=6, command=lambda m=root: self.close(m))

        self.top.bind('<Return>', lambda x=0:self.ok.invoke())

        self.position()


    def position(self):
        ''''Positions text and ok button'''
        self.text.pack(padx=12, pady=6)
        self.ok.pack(pady=6)


    def close(self, root):
        self.top.destroy()
        root.destroy()



class Failure:
    def __init__(self, root, message):
        '''A failure pop-up that does not close its root window upon closing'''
        self.top = tk.Toplevel(root)
        self.top.title("Error")
        self.top.resizable(False,False)
        self.top.wm_attributes("-topmost", True)

        self.text = tk.Label(self.top, text=message)
        self.ok = tk.Button(self.top, text="Ok", width=6, command=self.top.destroy)

        self.top.bind('<Return>', lambda x=0:self.ok.invoke())

        self.position()


    def position(self):
        ''''Positions text and ok button'''
        self.text.pack(padx=12, pady=6)
        self.ok.pack(pady=6)



class Rebuild:
    def open(self, root, data):
        '''Opens the rebuild data confirmation window'''
        self.top = tk.Toplevel(root)
        self.top.title("Rebuild Player/Game Entries")
        self.top.resizable(False,False)
        self.top.wm_attributes("-topmost", True)

        self.head = tk.Label(self.top, text="Rebuild Player/Game Entries")
        msg = "- W/L records will be recalculated to equal matches on record \n- Missing players/games with recorded matches will be added\n- Players/games with no matches on record will not be removed\n"
        self.body = tk.Label(self.top, text=msg, font="-size 8", justify=tk.LEFT)

        self.confirm = tk.Button(self.top, text="Confirm", width=8, command= lambda d=data: self.action(d))
        self.cancel = tk.Button(self.top, text="Cancel", width=8, command=self.top.destroy)

        self.top.bind('<Escape>', lambda x=0: self.cancel.invoke())

        self.position()
        self.top.grab_set()


    def position(self):
        '''Positions window elements'''
        self.head.pack(pady=2)
        self.body.pack(padx=12)
        self.cancel.pack(side=tk.RIGHT, padx=4, pady=4)
        self.confirm.pack(side=tk.RIGHT, pady=4)


    def action(self, data):
        '''Confirm button action - calls data methods to rebuild p/g'''
        err = data.rebuild()

        if not err:
            msg = "Data has been successfully rebuilt"
            self.message = Success(self.top, msg)

        elif err == 1:
            msg = "Unable to open records file"
            self.message = Failure(self.top, msg)

        else:
            msg = "An error occured while rebuilding"
            self.message = Failure(self.top, msg)



class About:
    def open(self, root):
        '''Opens the about window'''
        self.top = tk.Toplevel(root)
        self.top.title("About")
        self.top.resizable(False,False)
        self.top.wm_attributes("-topmost", True)

        self.mainFrame = tk.Frame(self.top)

        self.version = "ALPHA"
        self.title = tk.Label(self.mainFrame, font="-size 12", text="GrudgeMatch v." + self.version)

        self.license = tk.Label(self.mainFrame, font="-size 8", text="Copyright 2020 DLeinHellios\nApache License 2.0")

        self.logoFrame = tk.Frame(self.mainFrame)
        self.logoImage = tk.PhotoImage(master=self.mainFrame, file=os.path.join('img', 'logo_sm.png'))
        self.logo = tk.Label(master=self.logoFrame, image=self.logoImage)

        self.close = tk.Button(self.mainFrame, text="OK", width=6, command=self.top.destroy)

        self.position()
        self.top.grab_set()

    def position(self):
        '''Positions window elements'''
        self.mainFrame.pack(padx=10, pady=4)

        self.logoFrame.pack()
        self.logo.pack()

        self.title.pack()
        self.license.pack()
        self.close.pack()
