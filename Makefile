SOURCEDIR = ./src
DISTPATH = ./dist
WORKPATH = ./build

SOURCES = $(wildcard $(SOURCEDIR)/*.py)
SPECFILE = pylapse.spec

PYTHON = python
PIP = pip
PYINSTALLER = pyinstaller

APPNAME = pylapse


all: $(SOURCES)
	$(PYINSTALLER) $(SPECFILE)
	@echo "Build complete."

test:
	$(PYTHON) -m unittest test\test_parser.py

setup:
	$(PIP) install -r requirments.txt

clean:
	rm -rf $(DISTPATH)
	rm -rf $(WORKPATH)

.PHONY: test setup
