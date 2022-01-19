# Scout

A simple but powerful python-based __cross-platform__ youtube video/audio downloader.

**No bloated __javascript__ and __fishy__ redirect ad websites anymore!**

<img src="https://github.com/leifadev/scout/blob/main/doc/images/DEMO.png" alt="Demo" height="300" width="690"/>

## Why Scout?
|              Features             	|      Websites      	|        Scout       |
|:---------------------------------:	|:------------------:	|:------------------:|
| Download videos                   	| :white_check_mark: 	| :white_check_mark: |
| Only  video  or audio             	|          ➖        	| :white_check_mark:|
| No Ads                            	|          ❌         	| :white_check_mark:|
| No fishy redirect links            	|          ❌         	| :white_check_mark:|
|       Application stability       	|          ❌         	| :white_check_mark:|
| Multiple file formats               |          ❌     	    | :white_check_mark:|
|         Dark Mode       	          |         ➖   	      | :white_check_mark:|
|       Download Thumbnails         	|         ➖         	| :white_check_mark:|
|   Download Age-restriced vidoes 	|         ❌         	| :white_check_mark:|


## Native Build Details
```cs
Currently testing on macOS 10.15-16, Windows 10, Linux Mint 20.1/GNU Linux

Tested on Python 3, uses f-strings requiring 3.6+

Using main packages/frameworks/libraries:
- pytube
- ruamel.yaml
- wget
- ttkthemes
- ffmpeg
```

### Supported Versions

| OS Platform | Supported   |
| ------- | ------------------|
| Windows 10 | :white_check_mark:|
| MacOS 10.11-16 | :white_check_mark: |
| Linux   | :white_check_mark: |

*Since this is based only with python it is versatile for OS support*

## Compiling
Compiler: Pyinstaller v4.2 (6/6/21)

Example of [setup.py](https://github.com/leifadev/scout/blob/main/setup.py) output [pyinstaller](https://www.pyinstaller.org/) command:
```cs
pyinstaller --onefile --windowed --icon=scout_logo.png --osx-bundle-identifier="com.leifadev.scout" -n="Scout" scout.py
```
In the makefile, or just using the setup.py you can easily configure and build your own instance of scout. It uses your paths to python and automatically installs all the needed modules and dependcies for Scout (by default), asks for version, name, bundleId, debug, and more!


> <img src="https://github.com/leifadev/scout/blob/main/doc/images/compile%20example.png" alt="Example" height="350" width="560"/>



 ## To-do list
- ~~Release alpha version include barebones of functionality~~
- ~~Great file browser~~
- ~~Error handling with Console~~
- ~~Add customizable settings w/ storage file~~
- ~~Extensive testing on macOS, Windows, and Linux~~
- ~~Dark Mode~~
- ~~Add support for more file types and or resolutions~~
- ~~Add extra video file console logging~~
- ~~Add thumbnail downloading  support~~
- **Add playlist support with video selection**
- **Add custom theme integration (TkkThemes)**
- **Add segmented video download support**

# Help

### Reporting a Vulnerabilitys and Bugs

If you encounter any tiny to fatal bugs or security vulnerabilities, you can do the following:

1. Go to the [Issues page on this repo](https://github.com/leifadev/scout/issues).
2. Fill out bug report template of what you have encountered
3. Wait up to around 1 - 12 hours and you will likely to get a response. Realistically, I won't think you'll be waiting weeks on end obviously.

You can also contribute the the wiki as it is public for writing!

## Other
I also make youtube videos! Check them out if you want:
[https://youtube.com/vanillahowtv](https://youtube.com/vanillahowtv)
