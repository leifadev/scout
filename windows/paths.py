import getpass

user = 'C:\\Users\\' + {getpass.getuser()}
desktop = user + '\\Desktop\\'
appdata = user + '\\Appdata\\Roaming\\'

fileLoc = appdata + '\\Scout\\'
ymldir = fileLoc + 'settings.yml'
logo_loc = fileLoc + 'scout_logo.png'

repo_url = 'https://raw.githubusercontent.com/leifadev/scout/main/'
logo_url = repo_url + 'windows/scout_logo.png'