import tkinter as tk
import tkinter.ttk as ttk


class Success:
    def __init__(self, master, message):
        '''A success pop-up that closes its master window when toplevel is closed'''
        self.top = tk.Toplevel(master)
        self.top.title("Success")
        self.top.resizable(False,False)
        self.top.wm_attributes("-topmost", True)

        self.text = tk.Label(self.top, text=message)
        self.ok = tk.Button(self.top, text="Ok", width=6, command=lambda m=master: self.close(m))

        self.top.bind('<Return>', lambda x=0:self.ok.invoke())

        self.position()


    def position(self):
        ''''Positions text and ok button'''
        self.text.pack(padx=12, pady=6)
        self.ok.pack(pady=6)


    def close(self, master):
        self.top.destroy()
        master.destroy()



class Failure:
    def __init__(self, master, message):
        '''A failure pop-up that does not close its master window upon closing'''
        self.top = tk.Toplevel(master)
        self.top.title("Error")
        self.top.resizable(False,False)
        self.top.wm_attributes("-topmost", True)

        self.text = tk.Label(self.top, text=message)
        self.ok = tk.Button(self.top, text="Ok", width=6, command=lambda m=master: self.action(m))

        self.top.bind('<Return>', lambda x=0:self.ok.invoke())

        self.position()


    def position(self):
        ''''Positions text and ok button'''
        self.text.pack(padx=12, pady=6)
        self.ok.pack(pady=6)


    def action(self, master):
        '''Closes self.top and returns focus to master window'''
        self.top.destroy()



class Rebuild:
    def open(self, master, data):
        '''Opens the rebuild data confirmation window'''
        self.top = tk.Toplevel(master)
        self.top.title("Rebuild Player/Game Entries")
        self.top.resizable(False,False)
        self.top.wm_attributes("-topmost", True)

        self.head = tk.Label(self.top, text="Rebuild Player/Game Entries")
        msg = "- Players and games with no recorded matches will be removed \n- All players and games with recorded matches will be re-added\n"
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
