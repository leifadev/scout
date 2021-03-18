import tkinter as tk
import webbrowser
from pytube import YouTube


class App:
    def __init__(self, root):

        self.audioBool = False

        ## UI elements ##
        # initiating elements first!

        # Attributes #

        root.title("Sheath")
        width=845
        height=320
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        # Elements #

        label = tk.Label(root)
        label["justify"] = "left"
        label["text"] = "Scout"
        #        label.pack(padx=1,pady=2)
        label.place(x=390,y=5,width=70,height=25)


        self.urlfield = tk.Entry(root)
        self.urlfield["justify"] = "left"
        self.urlfield["text"] = ""
        self.urlfield.insert(0, '')   # add pre made message
        self.urlfield.place(x=20,y=60,width=624)

        self.downloadButton=tk.Button(root)
        self.downloadButton["justify"] = "center"
        self.downloadButton["text"] = "Download"
        self.downloadButton.place(x=660,y=60,width=170)
        self.downloadButton["command"] = self.downloadButton_command

        self.videoButton=tk.Checkbutton(root)
        self.videoButton["justify"] = "center"
        self.videoButton["text"] = "Video"
        self.videoButton.place(x=730,y=120,width=70,height=25)
        self.videoButton["offvalue"] = "0"
        self.videoButton["onvalue"] = "1"
        self.videoButton["command"] = self.videoButton_command

        self.audioButton=tk.Checkbutton(root)
        self.audioButton["justify"] = "center"
        self.audioButton["text"] = "Audio"
        self.audioButton.place(x=730,y=160,width=70,height=25)
        self.audioButton["onvalue"] = True
        self.audioButton["command"] = self.audioButton_command

        helpButton=tk.Button(root)
        helpButton["justify"] = "center"
        helpButton["text"] = "Help"
        helpButton.place(x=20,y=270,width=70)
        helpButton["command"] = self.helpButton_command

        ###### Hidden File format buttons ######








    ## Triggers and Scripts ##

    def downloadButton_command(self):
        query = self.urlfield.get()
        yt = YouTube(query)
        path = ""
        yt.streams.first().download(path)
                                        # print(yt.title)
        
        print(query)

    def videoButton_command(self):
        if self.audioBool == False:
            self.audioBool = True
        else:
            self.audioBool = False
        print(self.audioBool) # print boolean output


    def audioButton_command(self):
        if self.audioBool == False:
            self.audioBool = True
        else:
            self.audioBool = False

        print(self.audioBool) # print boolean output


    def helpButton_command(root):
        webbrowser.open("https://github.com/leifadev/scout")






# https://www.geeksforgeeks.org/file-explorer-in-python-using-tkinter/ # file browser
# https://python-pytube.readthedocs.io/en/latest/api.html



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
