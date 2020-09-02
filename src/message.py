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
