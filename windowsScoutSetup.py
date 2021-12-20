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
from tkinter import *
import webbrowser, getpass, wget, sys


class Window:
    def __init__(self, parent):

        self.localPath = ""
        self.systemPath = ""
        self.tempDir = "C://" # ADD TEMP DIR FROM WINDOWS
        self.icon = ""

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









if __name__ == "__main__":
    parent = Tk()
    app = Window(parent)
    parent.mainloop()
