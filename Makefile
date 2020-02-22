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

setup:
	$(PIP) install -r requirments.txt

clean:
	rm -rf $(DISTPATH)
	rm -rf $(WORKPATH)
