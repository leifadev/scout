import pytube
from pytube import YouTube, Playlist
from pytube.exceptions import *
import subprocess  # used for ffmpeg (file formatting)
import shutil  # mainly used for detecting ffmpeg installation
import ssl
import urllib.error



class youtube:

    def __init__(self):
        pass

    def run(self):
        playlist = Playlist("")

    def verifyQualities(self, downloadtype: str, streams: pytube.query):
        """


        :param downloadtype: "Video" or "audio": resolution or audio bit rate
        :param streams: A pytube StreamsQuery object that gets the metadata of a video's query
        """
        if downloadtype == "video":
            pass
        elif downloadtype == "audio":
            pass
        else:
            return

        attributes = {
            "res": ["1080p", "720p", "480p", "360p", "240p", "144p"],
            # "fps": [24, 30, 60],
            "abr": ["160kbs", "128kbs", "70kbs", "50kbs"]
        }

        aRes, aFPS, aAbr = [], [], [] # Get lists

        for key in attributes:  # Looping through "attributes" and "streams" to match available ones
            for i in attributes.get(key):
                if str(i) in str(streams):
                    if key == "res":
                        aRes.append(i)  # Put into a list to be printed later
                    else:
                        aFPS.append(i)
        try:
            if self.clickedvq.get() == "Quality":
                res = aRes[0]
        except Exception as e:
            print(
                "\nNo other available values were found to fallback on, check for any stream query objects above!\n" + str(
                    e))

            if audioDown is None:  # This tiny block for error handling no known download settings, suggests them afterwards
                self.logfield.insert(END, f'\nERROR: This video is unavailable with these download settings!\n')

                print("Gathered available quality options: ", aAbr)  # extra verbose input
                suggestMsg = f'\nINFO: Try the {aAbr} resolutions instead\n'
                self.logfield.insert(END, f'{suggestMsg}')

                self.logfield["state"] = "disabled"
                return

    ssl._create_default_https_context = ssl._create_unverified_context  # fixed windows SSL cert issue
