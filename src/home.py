import tkinter as tk
import tkinter.ttk as ttk
import os, sys
from src.edit import *


class PlayerIcons:
    def __init__(self, master, data):
        '''Contains all individual player buttons'''
        self.master = master
        self.generate(data)
        self.position(master)


    def generate(self, data):
        '''Generates player icon buttons from data object'''
        self.namelist = []
        self.icons = []
        self.avatars = []
        self.avatars.append(tk.PhotoImage(master=self.master, file=os.path.join('img', 'avatars', 'default.png')))

        for name in data.players.all:
            self.namelist.append(name)
            if os.path.isfile(os.path.join('img', 'avatars', name +  '.png')):
                avatar = tk.PhotoImage(master=self.master, file=os.path.join('img', 'avatars', name +  '.png'))

                if avatar.width() == 100 and avatar.height() == 100: # Only accept 100x100px
                    self.avatars.append(avatar)
                    self.icons.append(ttk.Button(self.master, text=name, image=self.avatars[-1], compound=tk.TOP, width=10))

                else:
                    self.icons.append(ttk.Button(self.master, text=name, image=self.avatars[0], compound=tk.TOP, width=10))

            else:
                self.icons.append(ttk.Button(self.master, text=name, image=self.avatars[0], compound=tk.TOP, width=10))


    def position(self, master):
        '''Repositions all player buttons - can get slow with large rosters'''
        col = master.winfo_width() // 110
        c,r = 0,0
        for t in self.icons:
            t.grid(row=r, column=c)
            c += 1

            if c >= col - 1:
                r += 1
                c = 0


    def append(self, data):
        '''Adds all pending icons to self.icons'''
        for name in data.players.all:
            if name not in self.namelist:
                self.namelist.append(name)
                if os.path.isfile(os.path.join('img', 'avatars', name +  '.png')):
                    avatar = tk.PhotoImage(master=self.master, file=os.path.join('img', 'avatars', name +  '.png'))

                    if avatar.width() == 100 and avatar.height() == 100: # Only accept 100x100px
                        self.avatars.append(avatar)
                        self.icons.append(ttk.Button(self.master, text=name, image=self.avatars[-1], compound=tk.TOP, width=10))

                    else:
                        self.icons.append(ttk.Button(self.master, text=name, image=self.avatars[0], compound=tk.TOP, width=10))

                else:
                    self.icons.append(ttk.Button(self.master, text=name, image=self.avatars[0], compound=tk.TOP, width=10))


    def refresh(self, data):
        '''Regenerates and repositions player icons'''
        self.append(data)
        self.position(self.master)



class Sidebar:
    def __init__(self, master, data, menus, icons):
        '''Class containing the sidebar buttons for the main window'''
        self.runM = tk.Button(master, text="Run Match", width=11)
        self.runS = tk.Button(master, text="Run Set", width=11)
        self.addF = tk.Button(master, text="Add Player", width=11, command=lambda m=master, d=data: menus.addP.open(m,d))
        self.addG = tk.Button(master, text="Add Game", width=11, command=lambda m=master, d=data: menus.addG.open(m,d))
        self.refresh = tk.Button(master, text="Refresh", width=11, command=lambda d=data: icons.refresh(d))
        self.exit = tk.Button(master, text="Exit", width=11, command=sys.exit)
        self.position()


    def position(self):
        '''Positions all sidebar buttons'''
        self.runM.pack(fill=tk.X)
        self.runS.pack(fill=tk.X)
        self.addF.pack(fill=tk.X)
        self.addG.pack(fill=tk.X)

        self.exit.pack(side=tk.BOTTOM, fill=tk.X)
        self.refresh.pack(side=tk.BOTTOM, fill=tk.X)



class TopMenu:
    def __init__(self, master, data, menus, icons):
        '''Top of the main window menu'''
        self.top = tk.Menu(master)

        self.file = tk.Menu(self.top, tearoff=0)
        self.file.add_command(label="Save", command=print)
        self.file.add_command(label="Refresh", command=print)
        self.file.add_command(label="Import", command=print)
        self.file.add_command(label="Export", command=print)
        self.file.add_separator()
        self.file.add_command(label="Exit", command=sys.exit)
        self.top.add_cascade(label="File", menu=self.file)

        self.edit = tk.Menu(self.top, tearoff=0)
        self.edit.add_command(label="Add Player", command=lambda m=master, d=data: menus.addP.open(m,d))
        self.edit.add_command(label="Add Game", command=lambda m=master, d=data: menus.addG.open(m,d))
        self.edit.add_separator()
        self.edit.add_command(label="Remove Player", command=print)
        self.edit.add_command(label="Remove Game", command=print)
        self.top.add_cascade(label="Edit", menu=self.edit)

        self.run = tk.Menu(self.top, tearoff=0)
        self.run.add_command(label="Run Match", command=print)
        self.run.add_command(label="Run Set", command=print)
        self.top.add_cascade(label="Run", menu=self.run)

        self.view = tk.Menu(self.top, tearoff=0)
        self.arrange = tk.Menu(self.top, tearoff=0)
        self.arrange.add_radiobutton(label="A-Z")
        self.arrange.add_radiobutton(label="Matches")
        self.arrange.add_radiobutton(label="Recent")
        self.show = tk.Menu(self.top, tearoff=0)
        self.show.add_radiobutton(label="Avatar")
        self.show.add_radiobutton(label="Name")
        self.show.add_radiobutton(label="Both")
        self.view.add_command(label="Game List", command=print)
        self.view.add_cascade(label="Arrange", menu=self.arrange)
        self.view.add_cascade(label="Show", menu=self.show)
        self.view.add_checkbutton(label="Hide Sidebar")
        self.top.add_cascade(label="View", menu=self.view)

        self.help = tk.Menu(self.top, tearoff=0)
        self.help.add_command(label="About", command=print)
        self.top.add_cascade(label="Help", menu=self.help)



class Frames:
    '''Contains all the frames for the main window'''
    def __init__(self, master):
        self.mainFrame = tk.Frame(master)
        self.mainCanvas = tk.Canvas(self.mainFrame, bd=0, highlightthickness=0, bg='gray')
        self.scrollbar = tk.Scrollbar(self.mainFrame, orient="vertical", command=self.mainCanvas.yview)
        self.scrollFrame = tk.Frame(self.mainCanvas, bg='gray')
        self.sideFrame = tk.Frame(master)

        self.mainCanvas.create_window((0, 0), window=self.scrollFrame, anchor="nw")
        self.mainCanvas.configure(yscrollcommand=self.scrollbar.set)

        self.bind(master)
        self.position()


    def mouse_wheel(self, event):
        '''Scrolls player widget on Linux and Windows'''
        self.mainCanvas.yview_scroll(int(-1*(event.delta/120)), "units")


    def bind(self, master):
        '''Binds scroll event'''
        self.scrollFrame.bind(
            "<Configure>",
            lambda e: self.mainCanvas.configure(
                scrollregion=self.mainCanvas.bbox("all")
            )
        )

        # Bind scroll for Windows
        master.bind_all("<MouseWheel>", self.mouse_wheel)
        # Bing scroll for Linux
        master.bind_all("<Button-4>", self.mouse_wheel)
        master.bind_all("<Button-5>", self.mouse_wheel)


    def position(self):
        '''Positions the frames on the main window'''
        self.mainFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.mainCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.sideFrame.pack(side=tk.RIGHT, fill=tk.Y)



class Menus:
    def __init__(self):
        '''Class for holding pop-up menu objects'''
        self.addP = AddPlayer()
        self.addG = AddGame()



class Window:
    def __init__(self, data):
        '''Class contianing the Tk root window and that handles it's maintenance'''
        self.root = tk.Tk()
        self.root.title("GrudgeMatch")
        self.root.resizable(True, True)
        self.root.bind('<Configure>', self.on_resize)
        self.root.minsize(570,388)

        self.data = data # Reference to data object
        self.menus = Menus() # Container for menu objects

        # Set window icon
        icondir = os.path.join('img', 'icon')
        if sys.platform == 'win32':
            iconfile = os.path.join(icondir, 'gm.ico')
            self.root.wm_iconbitmap(default=iconfile)
        else:
            ext = '.png' if tk.TkVersion >= 8.6 else '.gif'
            iconfiles = [os.path.join(icondir, 'gm_%d%s' % (size, ext))
                         for size in (16, 32, 48, 64, 128, 256)]
            icons = [tk.PhotoImage(master=self.root, file=iconfile)
                     for iconfile in iconfiles]
            self.root.wm_iconphoto(True, *icons)


        self.frames = Frames(self.root)
        self.icons = PlayerIcons(self.frames.scrollFrame, self.data)

        self.sidebar = Sidebar(self.frames.sideFrame, self.data, self.menus, self.icons)
        self.menu = TopMenu(self.root, self.data, self.menus, self.icons)
        self.root.config(menu=self.menu.top)


    def on_resize(self, event: tk.Event) -> None:
        '''Updates positions on window resize'''
        self.icons.position(self.root)
