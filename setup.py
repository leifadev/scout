"""

This is the official compile/build script for Scout, made by leifadev.
If there are ANY errors, *Please* report them informally or formally. This can be through
the github (https://github.com/leifadev/scout/issues) as issues, or a DM even.

It also recommended that you could make a commit or pull request for any issues as well, if
you have a github account :)

Thank you for supporting by downloading Scout :D

"""

import glob
import subprocess
import os
import time # asthetic reasons, slowing down time for verbose messages to be seen!

# script compiles scout based on OS from makefile :D

class setup:
    def __init__(self):
        # Main Vars
        self.which = ""
        self.version = ""
        self.debug = ""
        self.pip = "pi3.3456789 "
        self.python = "python3.6789 "
        self.modFile = ""

        ## Supported image file types for icons ##
        self.extensions = [".png", ".icns", ".ico"]
        ##########################################

        # print(os.getcwd())
        print("\n** THIS SCRIPT REQURIES PYTHON 3.6+ **\n")
        time.sleep(1)
        print("Starting compile process...")


        self.moveOn = (input("What python path/version are you using? (python, python3.8): "))
        if "python" in self.moveOn:
            self.version = "python"
            print("You selected: " + self.version)
            for x in self.version:
                if x not in self.python:
                    print("Your pip version may be outdated or your entry is invalid.")
                    return
            if "3" in self.moveOn:
                print("Ok, you seem to be using a python version of python to python3.9!")
            else:
                pass
        else:
            print("You have to use a supported version of python! (sorry if customized your path to pysnake69, etc.)")
            return
        self.version = self.moveOn
        print(f"\nYour using: {self.version}")


        time.sleep(0.5)
        print("\nBeginning!\n")

        self.installmodules()

    def installmodules(self):
        self.which = (input("What pip version are you using? (pip, pip3): "))
        if "pip" in self.which:
            print("You selected: " + self.which)
            for x in self.which:
                if x not in self.pip:
                    print("Your pip version may be outdated or your entry is invalid.")
                    return
            if "3" in self.which:
                print("Ok, you seem to be using a pip version of pip3 or pip3.9!")
        else:
            print("You have to use pip as your package manager!")
            return
        print(f"\nYour using: {self.which}")

        # Make and/or reset module requirements!
        try:
            import pipdeptree
        except ModuleNotFoundError:
            print("You do not have the module 'pipdeptree'")
            subprocess.run(f'{self.which} install pipdeptree', shell=True)

        if self.which in ("pip","pip3"):
            time.sleep(0.5)
            try:
                os.remove("requirements.txt")
            except FileNotFoundError:
                print(f'requirements.txt is not present as acting for freezing modules. Maybe you have a file for this under a different name?')


            print(f"\nRemoving requirements.txt in current folder directory...\n")
            time.sleep(1)
            print(os.getcwd() + ", is the current executing path. \nIf this isn't, maybe look into the code, and/or submit an issue at the github")
            time.sleep(2)
            print("\nFeezing, NOTE that the file for your freezed modules is coded to use 'requirements.txt'\nModify setup.py code if desired.")
            subprocess.run(f"pipdeptree --warn silence | grep -E '^\w+' >> requirements.txt", shell=True) # using pipdeptree instead of pip's freezing: for
            print("\n**Installing**")
            time.sleep(1.5)
            subprocess.run(self.which + f" install -r requirements.txt", shell=True)
        else:
            print("Not a valid option! Use pip or pip3\nIf you use another version like pip3.9, try pip3, if that doesn't work contact the developer.")
            return

    # Call PyInstaller to compile baby
        self.compile(None, None, None, None) # settings for pyinstaller args


    def compile(self, debug, icon, name, bundleId):
        print("Debug: When enabled will show a verbose logging console for realtime\ntraceback and exception errors.")

        # Asking for compile options
        debug = str(input("\nPress enter for windowed mode, type anything for debug mode: "))

        print(f'\nFound these image files in current working directory\nDetected Possible Icons:')

        options = {}
        count = int()
        count = 0

        for ext in self.extensions:
            files = glob.glob(os.getcwd() + '/**/*' + ext, recursive=True)
            options.update({count:files})
            count += 1

        for key in options:
            print(f'[{key}]: {options.get(key)}')


        icon = str(input("\nPress enter to skip setting an icon, or specify file name: "))

        try:
            if int(icon) in range(0,3):
                for key, value in enumerate(options):
                    if icon == key:
                        icon = options.get(key)
                        print(icon)
                    else:
                        pass
            else:
                print("Not a valid option! If you don't see your icon, it may not be supported!\nAdd your file extension in setup.py at line 32")
                return
        except NameError as e:
            print(f'Detected no specifed icon...')
            print(e)


        name = str(input("Press enter for no name of your app, other wise specify: "))

        bundleId = str(input("Press enter for no bundle ID, other wise specify: "))

        while "." not in bundleId:
            uSure = input("\nYour bundle ID didn't include any periods to seperate the developer \nand the apps name for example.\nDo you want to try again? Y/n: ")
            if uSure in "Yy":
                continue
            elif uSure in "Nn":
                break
            else:
                continue
        else:
            pass

        # config final variable forms
        for x in (icon, name, bundleId):
            if x is None or "":
                print(f'Counted a parameter be none value')
                x = ""
        if debug == "":
            debug = "--windowed"
        else:
            debug = "--console"


        print(f'\n-------------------------------\nYou have configured debug to "{debug}",\nYou have configured your icon to the path: "{icon}",\nYou have configured name to be: "{name}",\nYou configured bundle ID is: "{bundleId}"\n\nSettings saved!\n-------------------------------')
        time.sleep(3)

        print("Are you sure you want to compile?")
        comp = input("Do you want to proceed? Y/n: ")
        if comp in "yY":
            pass
        elif comp in "nN":
            return
        else:
            return
        # compile command
        try:
            # print(f'Compiling configurations: {debug}, {icon}, {name}, {bundleId}')
            subprocess.run(f'{self.version} -m PyInstaller --onefile {debug} --icon={icon} --osx-bundle-identifier={bundleId} -n={name} scout.py', shell=True)

        except ModuleNotFoundError as e:
            print(f'Pyinstaller wasn\'t not found! Try to install it again, must haven\'t worked')


if __name__ == '__main__':
    setup()

# end of script
