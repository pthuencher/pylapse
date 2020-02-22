SOURCEDIR = ./src
DISTPATH = ./dist
WORKPATH = ./build

SOURCES = $(wildcard $(SOURCEDIR)/*.py)
ENTRY_SCRIPT = $(SOURCEDIR)/core.py

PYTHON = python
PIP = pip
PYINSTALLER = pyinstaller

APPNAME = pylapse


all: $(SOURCES)
	$(PYINSTALLER) --onefile --name $(APPNAME) $(ENTRY_SCRIPT)
	@echo "Build complete."

setup:
	$(PIP) install -r requirments.txt

clean:
	rm -rf $(DISTPATH)
	rm -rf $(WORKPATH)