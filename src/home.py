import tkinter as tk
import tkinter.ttk as ttk
import os, sys
from src.edit import *
from src.match import *


class PlayerIcons:
    def __init__(self, root, data):
        '''Contains all individual player buttons'''
        self.root = root
        self.icons = {} # Dict of player buttons
        self.avatars = {} # Dict of player avatars
        self.avatars['default'] = tk.PhotoImage(master=self.root, file=os.path.join('img', 'avatars', 'default.png'))

        self.generate(data)
        self.position(self.root, data.config.settings['hide_sidebar'])


    def add_icon(self, name):
        '''Adds one icon to self.icons'''
        useAvatar = False

        if os.path.isfile(os.path.join('img', 'avatars', name +  '.png')):
            avatar = tk.PhotoImage(master=self.root, file=os.path.join('img', 'avatars', name +  '.png'))
            if avatar.width() == 100 and avatar.height() == 100: # Only accept 100x100px
                self.avatars[name] = avatar
                useAvatar = True

        if useAvatar:
            self.icons[name] = ttk.Button(self.root, text=name, image=self.avatars[name], compound=tk.TOP, width=10)
        else:
            self.icons[name] = ttk.Button(self.root, text=name, image=self.avatars['default'], compound=tk.TOP, width=10)


    def remove_icon(self, name):
        '''Removes a single icon'''
        self.icons[name].destroy()
        del self.icons[name]


    def generate(self, data):
        '''Generates initial player icon buttons'''
        for name in data.query.all_player_names(True):
            self.add_icon(name)


    def position(self, root, hideSidebar):
        '''Repositions all player buttons - can get slow with large rosters'''
        if len(self.icons) > 0:
            width = root.winfo_width() // 110
            if hideSidebar:
                width += 1

            # Advance columns
            col,row = 0,0
            for icon in self.icons.values():
                icon.grid(row=row, column=col)
                col += 1

                # Advance rows
                if col >= width - 1:
                    row += 1
                    col = 0


    def trim(self, data):
        '''Removes all player icon buttons not in data.players.all'''
        iconCopy = self.icons.copy()
        for name in iconCopy:
            if name not in data.query.all_player_names(True):
                self.remove_icon(name)


    def append(self, data):
        '''Adds all pending icons to self.icons from data.players.all'''
        for name in data.query.all_player_names(True):
            if name not in self.icons.keys():
                self.add_icon(name)


    def refresh(self, data):
        '''Regenerates and repositions player icons'''
        self.trim(data)
        self.append(data)
        self.position(self.root, data.config.settings['hide_sidebar'])



class Sidebar:
    def __init__(self, root, data, menus, icons):
        '''Class containing the sidebar buttons for the main window'''
        self.runM = tk.Button(root, text="Run Match", command=lambda m=root,d=data,me=menus: menus.matchSetup.open(m,d,me))
        self.records = tk.Button(root, text="Match Records", command=lambda m=root, d=data: menus.matchRecords.open(m,d))
        self.manP = tk.Button(root, text="Manage Players", command=lambda m=root,d=data: menus.manPlayers.open(m,d))
        self.manG = tk.Button(root, text="Manage Games", command=lambda m=root,d=data: menus.manGames.open(m,d))
        self.refresh = tk.Button(root, text="Refresh", command=lambda d=data: icons.refresh(d))
        self.exit = tk.Button(root, text="Exit", command=sys.exit)
        self.separator = ttk.Separator(root, orient=tk.HORIZONTAL)
        self.position()


    def position(self):
        '''Positions all sidebar buttons'''
        self.runM.pack(fill=tk.X)
        self.records.pack(fill=tk.X)
        self.separator.pack(fill=tk.X, padx=6, pady=4)
        self.manP.pack(fill=tk.X)
        self.manG.pack(fill=tk.X)

        self.exit.pack(side=tk.BOTTOM, fill=tk.X)
        self.refresh.pack(side=tk.BOTTOM, fill=tk.X)



class TopMenu:
    def __init__(self, root, data, menus, icons, frames):
        '''Top of the main window menu'''
        self.top = tk.Menu(root)

        self.file = tk.Menu(self.top, tearoff=0)
        #self.file.add_command(label="Save", command=print)
        self.file.add_command(label="Refresh", command=lambda d=data: icons.refresh(d))
        #self.file.add_command(label="Export", command=print)
        self.file.add_separator()
        self.file.add_command(label="Exit", command=sys.exit)
        self.top.add_cascade(label="File", menu=self.file)

        self.edit = tk.Menu(self.top, tearoff=0)
        self.edit.add_command(label="Manage Players", command=lambda m=root,d=data: menus.manPlayers.open(m,d))
        self.edit.add_command(label="Manage Games", command=lambda m=root, d=data: menus.manGames.open(m,d))
        #self.edit.add_command(label="Manage Tags", command=print)

        self.top.add_cascade(label="Edit", menu=self.edit)

        self.run = tk.Menu(self.top, tearoff=0)
        self.run.add_command(label="Run Match", command=lambda m=root,d=data,me=menus: menus.matchSetup.open(m,d,me))
        #self.run.add_command(label="Run Tournament", command=print)
        self.top.add_cascade(label="Run", menu=self.run)

        self.view = tk.Menu(self.top, tearoff=0)
        self.arrange = tk.Menu(self.top, tearoff=0)
        self.arrange.add_radiobutton(label="A-Z")
        self.arrange.add_radiobutton(label="Matches")
        self.arrange.add_radiobutton(label="Recent")
        self.view.add_command(label="Match Records", command=lambda m=root, d=data: menus.matchRecords.open(m,d))
        #self.view.add_cascade(label="Arrange", menu=self.arrange)
        self.view.add_command(label="Toggle Sidebar", command=lambda d=data: frames.toggle_sidebar(d))
        self.top.add_cascade(label="View", menu=self.view)

        self.help = tk.Menu(self.top, tearoff=0)
        #self.help.add_command(label="Help", command=print)
        self.help.add_command(label="About", command=lambda m=root: menus.about.open(m))
        self.top.add_cascade(label="Help", menu=self.help)



class Frames:
    '''Contains all the frames for the main window'''
    def __init__(self, root, data):
        self.mainFrame = tk.Frame(root)
        self.mainCanvas = tk.Canvas(self.mainFrame, bd=0, highlightthickness=0, bg='gray')
        self.scrollbar = tk.Scrollbar(self.mainFrame, orient="vertical", command=self.mainCanvas.yview)
        self.scrollFrame = tk.Frame(self.mainCanvas, bg='gray')
        self.sideFrame = tk.Frame(root, width=110)

        self.mainCanvas.create_window((0, 0), window=self.scrollFrame, anchor="nw")
        self.mainCanvas.configure(yscrollcommand=self.scrollbar.set)

        self.bind(root)
        self.position(data)


    def mouse_wheel(self, event):
        '''Scrolls player widget on Linux and Windows'''
        self.mainCanvas.yview_scroll(int(-1*(event.delta/120)), "units")


    def bind(self, root):
        '''Binds scroll event'''
        self.scrollFrame.bind(
            "<Configure>",
            lambda e: self.mainCanvas.configure(
                scrollregion=self.mainCanvas.bbox("all")
            )
        )

        # Bind scroll for Windows
        root.bind("<MouseWheel>", self.mouse_wheel)
        # Bind scroll for Linux
        root.bind("<Button-4>", self.mouse_wheel)
        root.bind("<Button-5>", self.mouse_wheel)


    def position(self, data):
        '''Positions the frames on the main window'''
        self.mainFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.mainCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.sideFrame.pack_propagate(0)

        if not data.config.settings['hide_sidebar']:
            self.sideFrame.pack(side=tk.RIGHT, fill=tk.Y)


    def toggle_sidebar(self, data):
        '''Switched the sidebar between hidden/shown'''
        if data.config.settings['hide_sidebar']:
            self.sideFrame.pack(side=tk.RIGHT, fill=tk.Y)
            data.config.settings['hide_sidebar'] = False

        else:
            self.sideFrame.pack_forget()
            data.config.settings['hide_sidebar'] = True

        data.config.save()



class Menus:
    def __init__(self):
        '''Class for holding pop-up menu objects'''
        self.manPlayers = ManagePlayers()
        self.manGames = ManageGames()

        self.matchSetup = MatchSetup()
        self.matchResults = MatchResults()

        self.matchRecords = MatchRecords()

        self.about = About()



class Window:
    def __init__(self, data):
        '''Main UI object - contains all UI elements and root Tk window'''
        self.root = tk.Tk()
        self.root.title("GrudgeMatch")
        self.root.resizable(True, True)
        self.root.bind('<Configure>', self.on_resize)
        self.root.minsize(565,390)

        self.data = data # Reference to data object
        self.menus = Menus() # Container for menu objects

        # Set window icon
        icondir = os.path.join('img', 'icon')
        if sys.platform == 'win32': # Windows
            iconfile = os.path.join(icondir, 'gm.ico')
            self.root.wm_iconbitmap(default=iconfile)
        else: # Linux
            ext = '.png' if tk.TkVersion >= 8.6 else '.gif'
            iconfiles = [os.path.join(icondir, 'gm_%d%s' % (size, ext))
                         for size in (16, 32, 48, 64, 128, 256)]
            icons = [tk.PhotoImage(master=self.root, file=iconfile)
                     for iconfile in iconfiles]
            self.root.wm_iconphoto(True, *icons)

        self.frames = Frames(self.root, self.data)
        self.icons = PlayerIcons(self.frames.scrollFrame, self.data)

        self.sidebar = Sidebar(self.frames.sideFrame, self.data, self.menus, self.icons)
        self.menu = TopMenu(self.root, self.data, self.menus, self.icons, self.frames)
        self.root.config(menu=self.menu.top)


    def on_resize(self, event: tk.Event) -> None:
        '''Updates positions on window resize'''
        self.icons.position(self.root, self.data.config.settings['hide_sidebar'])
