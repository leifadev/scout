PYTHON = python3
PIP = pip3
PROJECT_DIR = /
PROJECT_MAIN = scout.py
VERSION = v1.2

# file may need fixes!

.DEFAULT_GOAL = help

.PHONY: help setup clean build

help:
	@echo "---------------HELP-----------------"
	@echo "make help - display this message"
	@echo "make setup - setup the project for development"
	@echo "make clean - clean up files"
	@echo "make build - build the project"
	@echo "------------------------------------"
	@echo "\nCoded by leifadev\nhttps://github.com/leifadev/scout"

setup: setup
	@echo "Setting up project"$
	pip3 freeze >> requirements.txt && pip freeze >> requirements.txt
	pip3 install -r requirements.txt && pip install -r requirements.txt
	@echo "Launching scout, new files will be generated."
	python3 ${PROJECT_MAIN} && python ${PROJECT_MAIN}

clean:
	@echo "Cleaning project\n\n--------------------------"
	rm -rf *.pyc
	rm -rf *.pyo
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf *.build/
	rm -rf *.dist/
	@echo "\nFreezing your project! Updated requirements.txt\n"
	pip3 freeze >> requirements.txt 
	pip freeze >> requirements.txt 	
	@echo "\n--------------------------"


build:
	@echo "Building standalone application"
<<<<<<< HEAD
	$ pyinstaller --onefile --windowed --icon=scout_logo.png --osx-bundle-identifier="com.leifadev.scout" -n="Scout"  ${PROJECT_MAIN}
	@echo "Done building! :)"
=======
	@echo "Installing pyinstaller, you may have to install it your self because it is required."
	@echo "Installed on \"pip\""
	@echo "Installed on \"pip3\""
	$pip3 install pyinstaller
	$python3 -m PyInstaller --onefile --windowed --icon=scout_logo.png --osx-bundle-identifier="com.leifadev.scout" -n="Scout" ${PROJECT_MAIN}
>>>>>>> 278166dd502032a57e51a303689958ff1c3f7f57
