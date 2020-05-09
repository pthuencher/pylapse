SOURCE_DIR = ./src
DIST_DIR = ./dist
WORK_DIR = ./build

SOURCES = $(wildcard $(SOURCE_DIR)/*.py)
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
	rm -rf $(DIST_DIR)
	rm -rf $(WORK_DIR)

.PHONY: test setup
