PYTHON = python3
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

setup: clean
	@echo "Setting up project"
	${PYTHON} -m pip3 install -r requirements.txt
	${PYTHON} -m pip3 install -r ${PROJECT_DIR}/requirements.txt

clean:
	@echo "Cleaning project"
	rm --force --recursive *.pyc
	rm --force --recursive *.pyo
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info
	rm --force --recursive *.build/
	rm --force --recursive *.dist/

build: clean
	@echo "Building standalone application"
	$pyinstaller --onefile --windowed --icon=scout_logo.png  ${PROJECT_MAIN}
