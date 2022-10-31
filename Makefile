PY = python3
PIP = pip3 --require-virtualenv


# help: default            - Display this help statement
.PHONEY: default
default: help

# help: help               - Display this help statement
.PHONEY: help
help:
	@echo
	@echo "##################################"
	@echo "# GSComms Makefile Help Statment #"
	@echo "##################################"
	@echo
	@grep "^# help\:" Makefile | sed 's/\# help: //'
	@echo


# help: build              - Create a source distribution of GSComms
.PHONEY: build
build:
	@${PY} setup.py sdist


# help: install            - Install GSComms into the current python enviornment
.PHONEY: install
install:
	@${PIP} install .


# help: dev                - Install GSComms in development mode
.PHONEY: dev
dev:
	@${PIP} install -e .[dev]


# help: test               - Run the test suite
.PHONEY: test
test:
	@${PY} -m pytest


# help: style              - Auto style the code base
.PHONEY: style
style:
	@${PY} -m isort ./gscomms
	@${PY} -m black ./gscomms
