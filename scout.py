import tkinter as tk
from tkinter import *
import webbrowser
from tkinter.filedialog import askdirectory
from pytube import YouTube
from pytube.exceptions import RegexMatchError


# python3 setup.py py2app -A
# The whole app with its enity is in class App. Didn't deel the need to make more or something... lol

class App:
    def __init__(self, root):
        self.audioBool = False
        self.videoBool = False
        self.changedDefaultDir = False
        self.path = ""

        
        ## UI elements ##


        # Attributes #

        root.title("Scout")
        width=845
        height=350
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)



        # Menu items

        menubar = Menu(root)
        filemenu = Menu(menubar)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Cut", accelerator="Command+X", command=lambda: root.focus_get().event_generate('<<Cut>>'))
        
        filemenu.add_command(label="Copy", accelerator="Command+C", command=lambda: root.focus_get().event_generate('<<Copy>>'))
        
        filemenu.add_command(label="Paste", accelerator="Command+V", command=lambda: root.focus_get().event_generate('<<Paste>>'))
        
        filemenu.add_separator()
        
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)


        helpmenu = Menu(menubar)
        
        helpmenu.add_command(label="About", command=self.dummy)
        helpmenu.add_command(label="Help", command=self.helpButton_command)
        
        helpmenu.add_separator()
        
        helpmenu.add_command(label="Settings", command=self.settings_button)
        menubar.add_cascade(label="About", menu=helpmenu)

        root.config(menu=menubar)
        

        # Elements #

        #        label = tk.Label(root)
        #        label["justify"] = "left"
        #        label["text"] = "Scout"
        #        #        label.pack(padx=1,pady=2)
        #        label.place(x=390,y=5,width=70,height=25)


        self.urlfield = tk.Entry(root)
        self.urlfield["justify"] = "left"
        self.urlfield["text"] = ""
        self.urlfield.insert(0, '')   # add pre made message
        self.urlfield.place(x=20,y=60,width=540)

        self.downloadButton=tk.Button(root)
        self.downloadButton["justify"] = "center"
        self.downloadButton["text"] = "Download"
        self.downloadButton.place(x=570,y=59,width=120)
        self.downloadButton["command"] = self.downloadButton_command


        self.browseButton=tk.Button(root)
        self.browseButton["text"] = "File Destination"
        self.browseButton["command"] = self.browseButton_command
        self.browseButton.place(x=690,y=59,width=140)


        self.videoButton=tk.Checkbutton(root)
        self.videoButton["justify"] = "center"
        self.videoButton["text"] = "Video"
        self.videoButton.place(x=720,y=120,width=70,height=25)
        self.videoButton["offvalue"] = "0"
        self.videoButton["onvalue"] = "1"
        self.videoButton["command"] = self.videoButton_command

        self.audioButton=tk.Checkbutton(root)
        self.audioButton["justify"] = "center"
        self.audioButton["text"] = "Audio"
        self.audioButton.place(x=720,y=160,width=70,height=25)
        self.audioButton["onvalue"] = True
        self.audioButton["command"] = self.audioButton_command

        helpButton=tk.Button(root)
        helpButton["justify"] = "center"
        helpButton["text"] = "Help"
        helpButton.place(x=20,y=300,width=70)
        helpButton["command"] = self.helpButton_command

        ###### Hidden File format buttons ######






    ## Triggers and Scripts ##

    def downloadButton_command(self):
        
        if self.videoBool and self.audioBool:
            query = self.urlfield.get() # gets entry input
            yt = YouTube(query)
            yt.streams.filters().first().download(self.path)
            
        elif self.audioBool:  # Audio only
            query = self.urlfield.get() # gets entry input
            yt = YouTube(query)
            yt.streams.filters(only_audio=True).first().download(self.path)

        elif self.audioBool == False and self.videoBool: # Video only
            print("video only mmmmzaaddyyyy")
            
        else:
            print("ERROR: Invalid selection, you need download some form of media!")

        
        

    def browseButton_command(self):
        if self.changedDefaultDir:
            self.path = str(askdirectory(initialdir=self.path))
        else:
            self.path = str(askdirectory(initialdir='~/Desktop/'))
        
        ## READ THIS OK: ADD IN SETTINGS PANEL CHANGE YOUR DEFAULT DIR OPTION


    def videoButton_command(self):
        if self.videoBool == False:
            self.videoBool = True
        else:
            self.videoBool = False



    def audioButton_command(self):
        if self.audioBool == False:
            self.audioBool = True
        else:
            self.audioBool = False
            

    def helpButton_command(self):
        webbrowser.open("https://github.com/leifadev/scout")
        
        
        
        
    def settings_button(self):
        sWin = Toplevel()
        sWin.title("Settings")
        width=550
        height=400
        screenwidth = sWin.winfo_screenwidth()
        screenheight = sWin.winfo_screenheight()
        sWin_alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        sWin.geometry(sWin_alignstr)
        sWin.resizable(width=False, height=False)

        defaultDirButton=tk.Button(sWin)
        defaultDirButton["justify"] = "center"
        defaultDirButton["text"] = "Choose"
        defaultDirButton.place(x=280,y=168,width=120)
        defaultDirButton["command"] = self.defaultDir_command

        defaultDirTip = tk.Label(sWin)
        defaultDirTip = Label(sWin, text="Set Default Directory")
        defaultDirTip.place(x=140,y=170,width=140)

        defaultDirTip = tk.Label(sWin)
        defaultDirTip = Label(sWin, text="Settings")
        defaultDirTip.place(x=200,y=60,width=140)



    def defaultDir_command(self):
        self.path = str(askdirectory())   # Uses tkinter filedialog for prompting a save dir
        self.changedDefaultDir = True

        
    def dummy(self):
        pass




# https://www.geeksforgeeks.org/file-explorer-in-python-using-tkinter/ # file browser
# https://python-pytube.readthedocs.io/en/latest/api.html



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

