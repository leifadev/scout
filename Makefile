PYTHON = python3
PROJECT_DIR = /
PROJECT_MAIN = scout.py


.DEFAULT_GOAL = help

.PHONY: help setup clean test build upload standalone install run

help:
	@echo "---------------HELP-----------------"
	@echo "make help - display this message"
	@echo "make setup - setup the project for development"
	@echo "make clean - clean the project"
	@echo "make test - run tests on the project"
	@echo "make build - build the project"
	@echo "make upload - upload the project to PyPI"
	@echo "make standalone - build standalone application"
	@echo "make install - install the project to local python installation"
	@echo "make run - run the project"
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

test:
	${PYTHON} -m nose2 -v


build: clean
	@echo "Building project"
	${PYTHON} -m nuitka ${PROJECT_MAIN}


standalone: clean
	@echo "Building standalone application"
	${PYTHON} -m  nuitka --standalone ${PROJECT_MAIN}

install: clean
	@echo "Installing project"
	${PYTHON} -m pip3 install .

run: clean
	@echo "Running project"
	${PYTHON} ${PROJECT_MAIN}