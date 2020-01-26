# 3rd pary imports
from colorama import Fore, Back, Style

# Globals
VERBOSE = False

# Logging macros
def ERROR(msg, shutdown=False):
    print('[' + Fore.RED + 'ERROR' + Style.RESET_ALL + '] ' + str(msg))
    if shutdown:
        sys.exit(1)

def DEBUG(msg):
    if VERBOSE:
        print('[DEBUG] ' + str(msg))

def INFO(msg, color=None, overwrite=False):
    end = '\r' if overwrite else '\n'
    print('[' + Fore.YELLOW + 'timelapse' + Style.RESET_ALL + '] ' + str(msg), end=end)

def parse_dimension(dim):
    if not dim:
        return None
    
    d = dim.split('x')
    if len(d) != 2:
        ERROR('Failed to parse dimension "%s". Use e.g. 720x480' % dim, shutdown=True)

    return (int(d[0]), int(d[1]))

def create_progress_bar(perc):
    return '\x1b[1;32m#\x1b[1;0m'*perc + '-'*(100-perc)