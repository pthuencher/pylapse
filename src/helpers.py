# standard imports
import glob
import sys
import os

# 3rd pary imports
from colorama import Fore, Back, Style

# local imports

# Globals
VERBOSE = False
COLORS = True

# Logging macros
def FATAL(msg):
    ERROR(msg, shutdown=True)
    
def ERROR(msg, shutdown=False):
    if COLORS:
        print('[' + Fore.RED + 'ERROR' + Style.RESET_ALL + '] ' + str(msg))
    else:
        print('[ERROR] ' + str(msg))
    if shutdown:
        sys.exit(1)

def DEBUG(msg):
    if VERBOSE:
        print('[DEBUG] ' + str(msg))

def INFO(msg, color=None, overwrite=False):
    end = '\r' if overwrite else '\n'
    if COLORS:
        print('[' + Fore.YELLOW + 'timelapse' + Style.RESET_ALL + '] ' + str(msg), end=end)
    else:
        print('[timelapse] ' + str(msg), end=end)

def parse_resize(size):
    if not size:
        return None

    d = size.split('x')
    if len(d) != 2:
        FATAL('Invalid resize value "%s". Use e.g. "720x480"' % size)

    return (int(d[0]), int(d[1]))

def parse_crop(crop):
    if not crop:
        return None

    d = crop.split(':')
    if len(d) != 2:
        FATAL('Invalid crop value "%s". Use "x1-x2:y1-y2"' % crop)

    x = d[1].split('-')
    y = d[0].split('-')

    if len(x) != 2 or len(y) != 2:
        FATAL('Invalid crop value "%s". Use "x1-x2:y1-y2"' % crop)

    return ((int(x[0]), int(x[1])), (int(y[0]), int(y[1])))

def create_progress_bar(perc):
    return '\x1b[1;32m#\x1b[1;0m'*perc + '-'*(100-perc)

