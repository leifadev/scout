"""
Script Version: v0.1
Author: leifadev

This script applies too all versions of Scout v1.5.1 and under,
to automatically install FFmpeg for Scout AND the system!

This script installs FFmpeg and directs the path to: ... <<---------- FILL IN HERE
This script will be compiled and shipped out directly as such.


NOTE: Make an options available local path and system-wide path

"""

import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
import webbrowser, getpass, wget, os, time, zipfile


class Window:
    def __init__(self, parent):

        self.localPath = ""
        self.systemPath = ""
        self.tempDir = f"C:\\Users\\{getpass.getuser()}\\AppData\\Local\\Temp\\" # ADD TEMP DIR FROM WINDOWS
        self.icon = ""
        self.version = "v0.1"


        parent.title("Scout Windows FFmpeg Installer")

        width=450
        height=350
        screenwidth = parent.winfo_screenwidth()
        screenheight = parent.winfo_screenheight()

        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        parent.geometry(alignstr)
        parent.resizable(width=True, height=True)

        print("Attemping logo downloading...")
        url = "https://raw.githubusercontent.com/leifadev/scout/main/images/scout_logo_windows_installer.png"

        # Download icon for use if not present
        if not os.path.isfile(self.tempDir + "scout_windows_installer.png"):
            wget.download(url, self.tempDir + "scout_windows_installer.png")
        else:
            print("Icon detected!")
        self.icon = PhotoImage(file=self.tempDir + "scout_windows_installer.png")
        parent.tk.call('wm', 'iconphoto', parent._w, self.icon)

        parent.update()   # Updates window at startup to be interactive and lifted


        self.logfield = tk.Text(parent)
        ft = tkFont.Font(family="Courier", size=8)
        self.logfield["font"] = ft
        self.logfield["highlightthickness"] = 0
        self.logfield.insert(END, f"Launched successfully!\nVersion: {self.version}")
        self.logfield["state"] = "disabled"


        self.startB=tk.Button(parent)
        self.startB["text"] = "Install"
        # self.startB["command"] = self.install


        self.cancelB=tk.Button(parent)
        self.cancelB["text"] = "Cancel"
        self.cancelB["command"] = self.cancel

#        |████████████████████████████████| <---- cool B)

        # Gridding

        self.logfield.grid(row=1, column=0, padx=(100, 10))
        self.startB.grid(row=0, column=1, padx=(100, 10))
        self.cancelB.grid(row=0, column=0, padx=(100, 10))


    # Functions!

    def install(self, type: str):
        os.chdir(self.tempDir)
        wget.download("https://evermeet.cx/ffmpeg/getrelease/zip", self.tempDir + "ffmpeg.zip")

        print("\nDownloading latest stable version of ffmpeg, may take several seconds!\n")

        self.logfield.insert("Extracting ffmpeg zip...")
        with ZipFile("ffmpeg.zip", 'r') as zip: # extracts downloaded zip from ffmpegs download API for latest release
            zip.extractall()
        self.logfield.insert("File extracted!")
        print("\nFile extracted...\n")


    # cancels program and "saves"
    def cancel(self):
        print("XDD")
        self.logfield["state"] = "normal"
        self.logfield.insert(END, f"WARNING: Installer program is closing!")
        for i in range(0, 32):
            self.logfield.insert("Saving... |" + (i * "█") + ((31 - i) * " ") + "|")
        self.logfield["state"] = "disabled"
        # quit()




# loop it lol XD

if __name__ == "__main__":
    parent = Tk()
    app = Window(parent)
    parent.mainloop()
