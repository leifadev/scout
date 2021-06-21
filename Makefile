PYTHON = python3
PIP = pip3
PROJECT_DIR = /
PROJECT_MAIN = scout.py
VERSION = v1.2

# leifadev, scout.app

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
	@echo "Setting up project"
	${PIP} freeze >> requirements.txt
	${PIP} install -r requirements.txt
	@echo "Launching scout, new files will be generated."
	${PYTHON} ${PROJECT_MAIN} && python ${PROJECT_MAIN}

clean:
	@echo "Cleaning project\n\n--------------------------"
	rm -rf *.pyc
	rm -rf *.pyo
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf *.build/
	rm -rf *.dist/
	rm -rf requirements.txt
	@echo "\nFreezing your project! Updated requirements.txt\n"
	${PIP} freeze >> requirements.txt
	@echo "\n--------------------------"


build:
	@echo "Building standalone application, pip is required!"
	${PIP} install pyinstaller
	${PIP} freeze >> requirements.txt
	$ pyinstaller --onefile --windowed --icon=scout_logo.png --osx-bundle-identifier="com.leifadev.scout" -n="Scout"  ${PROJECT_MAIN}
	@echo "Done building! :)"
