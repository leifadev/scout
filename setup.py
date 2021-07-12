# from sys import platform as _platform
import subprocess
import os
import time

# script compiles scout based on OS from makefile :D

class setup:
    def __init__(self):
        # Main Vars
        self.which = ""
        self.version = ""
        self.debug = ""

        print(os.getcwd())

        print("Starting compile process...")


        self.moveOn = input("For use of python3, press enter, for python, enter any key: ")

        if self.moveOn == "":
            self.version = "python3"
        else:
            self.version = "python"
        print("Your using: " + self.version)
        time.sleep(0.5)
        print("Beginning!")

        self.installmodules()

    def installmodules(self):
        self.which = (input("Are using 'pip' or 'pip3': "))
        print("Your selected: " + self.which)
        if self.which in ("pip","pip3"):
            time.sleep(0.5)
            try:
                os.remove("requirements.txt")
            except:
                pass

            print("Removing requirements.txt in current folder directory...")
            print(os.getcwd() + "is the current executing path. If this isn't, maybe look into the code, and/or submit an issue at the github")
            print("Feezing :)")
            subprocess.run(self.which + " freeze >> requirements.txt", shell=True)
            print("**Installing**\n\n")
            subprocess.run(self.which + " install -r requirements.txt", shell=True)
        else:
            print("Not a valid option! Use pip or pip3\nIf you use another version like pip3.9, try pip3, if that doesn't work contact the developer.")
            return


    def compile(self, debug, icon, name):
        pass

if __name__ == '__main__':
    setup()
