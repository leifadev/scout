# CURRENTLY THIS MAKEFILE IS BROKEN, MAKE AN ISSUE ON GITHUB FOR MORE INFO

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
	@echo "Modify your '{PIP}' variable in your Makefile to match your current one"
	@${PIP} install -r requirements.txt
	@git pull
	@echo "Launching scout, new files will be generated."

clean:
	@echo "Cleaning project\n\n--------------------------\n"
	rm -rf *.pyc
	rm -rf *.pyo
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf *.build/
	rm -rf *.dist/
	rm -rf __pycache__/
	rm -rf requirements.txt
	@echo "\nFreezing your project! Updated requirements.txt"
	@echo "\n--------------------------"


build:
	@echo "Building standalone application, pip is required!"
	@echo "Change your PYTHON path in Makefile accordingly if I fail!"
	@${PYTHON} setup.py
	@echo "Done with session! :)"
