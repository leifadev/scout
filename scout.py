import tkinter as tk
import webbrowser
from tkinter.filedialog import askdirectory
from pytube import YouTube

class App:
    def __init__(self, root):

        self.audioBool = False
        self.videoBool = False
        
        
        self.path = ""

        ## UI elements ##
        # initiating elements first!

        # Attributes #

        root.title("Scout")
        width=845
        height=350
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        




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
        query = self.urlfield.get() # gets entry input
        yt = YouTube(query)

        yt.streams.first().download(self.path)
        
            


    def browseButton_command(self):
        self.path = str(askdirectory())   # Uses tkinter filedialog for prompting a save dir
        print(self.path)
        


    def videoButton_command(self):
        if self.videoBool == False:
            self.videoBool = True
        else:
            self.videoBool = False

#        print(self.videoBool) # print boolean output


    def audioButton_command(self):
    
        if self.audioBool == False:
            self.audioBool = True
        else:
            self.audioBool = False

#        print(self.audioBool) # print boolean output


    def helpButton_command(root):
        webbrowser.open("https://github.com/leifadev/scout")






# https://www.geeksforgeeks.org/file-explorer-in-python-using-tkinter/ # file browser
# https://python-pytube.readthedocs.io/en/latest/api.html



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()


#        if self.audioBool:
#            print("audio")
#            if self.videoBool:
#                print("both on")
#        elif self.videoBool:
#                print("video")
#        else:
#            print("nothing")
