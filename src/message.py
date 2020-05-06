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
        self.ok.pack()


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
        self.ok = tk.Button(self.top, text="Ok", width=6, command=self.top.destroy)

        self.top.bind('<Return>', lambda x=0:self.ok.invoke())

        self.position()

    def position(self):
        ''''Positions text and ok button'''
        self.text.pack(padx=12, pady=6)
        self.ok.pack()



class Confirm: # TODO - Make confirmation work - not implemented
    def __init__(self, master, message, cmd):
        '''A confirm pop-up with a yes and no option'''
        self.top = tk.Toplevel(master)
        self.top.title("Confirm")
        self.top.resizable(False,False)
        self.top.wm_attributes("-topmost", True)

        self.text = tk.Label(self.top, text=message)
        self.yes = tk.Button(self.top, text="Yes", width=6, command=cmd)
        self.no = tk.Button(self.top, text="No", width=6, command=self.close)

        self.position()


    def confirm_close(self):
        self.top.destroy()


    def close(self):
        self.top.destroy()


    def position(self):
        ''''Positions text and ok button'''
        self.text.pack(padx=12, pady=6)
        self.yes.pack(side=tk.LEFT)
        self.no.pack(side=tk.RIGHT)
