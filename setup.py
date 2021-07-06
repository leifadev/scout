# from sys import platform as _platform
import subprocess
import os

# script compiles scout based on OS from makefile :D

class setup:
    def __init__(self):
        self.which = ""
        self.version = ""
        self.debug = ""

        print(os.getcwd())

        print("Starting compile...")


        self.moveOn = input("For use of python3, press enter, for python, enter any key: ")

        if self.moveOn == "":
            self.version = "python3"
        else:
            self.version = "python"
        print("Your using: " + self.version)


    def installmodules(self):
        self.which = (input("Are using 'pip' or 'pip3': "))
        if "pip" or "pip3" == self.which:
            print("**Freezing**")
            subprocess.run(self.which + " freeze >> requirements.txt", shell=True)
            print("**Installing**")
            subprocess.run(self.which + " install -r requirements.txt", shell=True)
        else:
            print("Not a valid option! pip or pip3")
            return

        self.installmodules()


    def compile(self, debug, icon, name):
        print("\nNow choose your compiler options...:")
        os.getcwd()
        self.debug = input("Would you like to export as a debug mode (console output)?\n")
        self.icon = input("Enter in what icon you would like scout to have.\nWe found the following:" + self.debug)

        if self.debug == "yes":
            self.debug = "--windowed"
        subprocess.run(f"pyinstaller --{self.debug}", shell=True)
        print("Done :D")

