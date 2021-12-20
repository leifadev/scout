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
import webbrowser, getpass, wget, sys, time, zipfile


class Window:
    def __init__(self, parent):

        self.localPath = ""
        self.systemPath = ""
        self.tempDir = "C://" # ADD TEMP DIR FROM WINDOWS
        self.icon = ""
        self.version = "v0.1"

        parent.title("Scout Windows FFmpeg Installer")

        width=450
        height=350
        screenwidth = parent.winfo_screenwidth()
        screenheight = parent.winfo_screenheight()

        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        parent.geometry(alignstr)
        parent.resizable(width=False, height=False)

        print("Attemping logo downloading...")
        url = "https://raw.githubusercontent.com/leifadev/scout/main/images/scout_logo_windows_installer.png"

        # Download icon for use if not present
        if not os.path.isfile(self.tempDir + "scout_logo.png"):
            wget.download(url, self.tempDir + "scout_windows_installer.png")
        self.icon = PhotoImage(file=self.tempDir + "scout_windows_installer.png")
        parent.tk.call('wm', 'iconphoto', parent._w, self.icon)

        parent.update()   # Updates window at startup to be interactive and lifted


        self.logfield = tk.Text(parent)
        self.logfield.place(x=20,y=100,width=540, height=180)
        ft = tkFont.Font(family="Courier", size=8)
        self.logfield["font"] = ft
        self.logfield["highlightthickness"] = 0
        self.logfield.insert(END, f"Launched successfully!\nVersion: {self.version}\n\n NOTE: ")
        self.logfield["state"] = "disabled"


        self.startB=ttk.Button(parent)
        self.startB["text"] = "Install"
        self.startB.place(x=570,y=59,width=120)
        self.startB["command"] = self.install


        self.cancelB=ttk.Button(parent)
        self.cancelB["text"] = "Cancel"
        self.cancelB["command"] = self.cancel
        self.cancelB.place(x=690,y=59,width=140)

#        |████████████████████████████████| <---- cool B)

        # Gridding

        self.logfield.grid(row=0, column=0, padx=(100, 10))
        self.startB.grid(row=0, column=0, padx=(100, 10))
        self.cancelB.grid(row=0, column=0, padx=(100, 10))


        def install(self, type: str):
            os.chdir(self.tempDir)
            wget.download("https://evermeet.cx/ffmpeg/getrelease/zip", self.tempDir + "ffmpeg.zip")

            print("\nDownloading latest stable version of ffmpeg, may take several seconds!\n")

            with ZipFile("ffmpeg.zip", 'r') as zip: # extracts downloaded zip from ffmpegs download API for latest release
                zip.extractall()
            print("\nFile extracted...\n")


        # cancels program and "saves"
        def cancel(self):
            self.logfield.insert(END, f"WARNING: Installer program is closing!")
            for i in range(0, 32):
                self.logfield.delete("2.0", "2.0")
                self.logfield.insert("Saving... |" + (i * "█") + ((31 - i) * " ") + "|")
                time.sleep(0.5)
            quit()




# loop it lol XD

if __name__ == "__main__":
    parent = Tk()
    app = Window(parent)
    parent.mainloop()
