# Scout

A simple but powerful python-based cross-platform youtube video/audio downloader.
No bloated javascript ad websites anymore!

## Native Build Details
```cs
Currently testing on macOS 10.15-16, Windows 10, Linux Mint 20.1/GNU Linux

Tested python versions: 3.7 - 9.2

Using main packages/frameworks/libraries:
- pytube
- ruamel.yaml
- wget
- ttkthemes
- ffmpeg

Compiler: Pyinstaller v4.2 (6/6/21)
```
**Pyinstaller Command**
```cs
pyinstaller --onefile --windowed --icon=scout_logo.png --osx-bundle-identifier="com.leifadev.scout" --version-file="1.5" -n="Scout" scout.py
```
### Supported Versions

| OS Platform | Supported   |
| ------- | ------------------|
| Windows 10 | :white_check_mark:|
| MacOS 10.11-16 | :white_check_mark: |
| Linux   | :white_check_mark: |

*Since this is based only with python it is versatile for OS support*

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
