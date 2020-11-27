# standard imports
from argparse import ArgumentParser, RawTextHelpFormatter
import sys
import os

# 3rd pary imports
from colorama import Fore, Back, Style

# local imports



# Globals
VERBOSE = False
COLORS = True

# Version
VSN = '2020.11.27'

# Defaults
DEFAULT_FPS = 24
DEFAULT_FOURCC = 'DIVX'
DEFAULT_EXTENSION = 'avi'
DEFAULT_OUTPUT_FILENAME = 'out'



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

def WARN(msg):
    if COLORS:
        print('[' + Fore.YELLOW + 'timelapse' + Style.RESET_ALL + '] '+ Fore.RED + 'Warning: ' + Style.RESET_ALL + str(msg))
    else:
        print('[timelapse] Warning: ' + str(msg))

def INFO(msg, overwrite=False):
    end = '\r' if overwrite else '\n'
    if COLORS:
        print('[' + Fore.YELLOW + 'timelapse' + Style.RESET_ALL + '] ' + str(msg), end=end)
    else:
        print('[timelapse] ' + str(msg), end=end)


# Argument parsing
def parse_args():

    # setup ArgumentParser
    parser = ArgumentParser(
        description='Create timelapse video from image frames.', 
        formatter_class=RawTextHelpFormatter)

    # add argument groups
    output_group = parser.add_argument_group('output')
    settings_group = parser.add_argument_group('settings')
    transform_group = parser.add_argument_group('transform')

    parser.add_argument(
        'source', 
        help='load image frames from source')

    output_group.add_argument(
        '-o', '--output',
        default=DEFAULT_OUTPUT_FILENAME,
        metavar='FILE',
        help='render video to FILE')

    parser.add_argument(
        '-f', '--force-overwrite', 
        action='store_true',
        help='force overwrite existing files')

    parser.add_argument(
        '--debug',
        dest="verbose",
        action='store_true',
        help='display verbose debug output')

    output_group.add_argument(
        '--preview', 
        action='store_true',
        help='preview (do not write any file)')

    transform_group.add_argument(
        '--resize',
        help='resize images (example: 1920x1080)\n\n    3840x2160 (16:9) 4K\n    1920x1080 (16:9) Full HD\n    1280x720  (16:9)\n    2880x2160 (4:3)\n    1440x1080 (4:3)\n    640x480   (4:3)\n\n ')

    transform_group.add_argument(
        '--crop', 
        help='crop images (example: 0-1920:0-1080)')

    settings_group.add_argument(
        '--ext',
        default=DEFAULT_EXTENSION,
        help='extension of the final video file. (default: %(default)s)')

    settings_group.add_argument(
        '--fps',
        default=30,
        help='frames per second (default: %(default)s)')

    settings_group.add_argument(
        '--fourcc', 
        default=DEFAULT_FOURCC,
        help='FOURCC code of the final video file (default: %(default)s)')

    parser.add_argument(
        '--no-colors', 
        action='store_true', 
        help='force uncolored output')

    parser.add_argument(
        '-v', '--version', 
        action='version', 
        version="pylapse - " + VSN)

    args = parser.parse_args()

    # Set verbosity status
    global VERBOSE
    VERBOSE = args.verbose

    # Set output color status
    global COLORS
    COLORS = not args.no_colors

    # fix output path
    _, ext = os.path.splitext(args.output)
    if not ext:
        args.output = '%s.%s' % (args.output, args.ext)
    
    # Type conversion
    DEBUG('Arguments: %r' % args)
    return __assert_args(args)

def __assert_args(args):

    # Check preconditions    
    #  1.) Source folder existence
    args.sourcepath = os.path.abspath(args.source)
    DEBUG('Sourcepath: %s' % args.sourcepath)
    if not os.path.isdir(args.sourcepath):
        FATAL('Path "%s" is not a directory. Please point to a valid directory that contains the source files.' % args.sourcepath)

    # 2.) Parse resize & crop parameters
    args.resize = __parse_resize(args.resize)
    if args.resize: DEBUG('Resize: %dx%d' % args.resize)
    args.crop = __parse_crop(args.crop)
    if args.crop: DEBUG('Crop: %r %r' % args.crop)

    #  3.) Output file existence (if not preview)
    if (args.preview): return args

    args.outputpath = os.path.abspath(args.output)
    DEBUG('Outputpath: %s' % args.outputpath)
    if os.path.exists(args.outputpath):
        if args.force_overwrite:
            INFO('Overwriting existing file "%s"' % args.outputpath)
        else:
            choice = input('File "%s" already exists. Overwrite? (y/N): ' % args.outputpath)
            if choice != 'y':
                FATAL('Aborted. Use -o to specify another output filename.')
    
    return args

def __parse_resize(size):
    if not size:
        return None

    d = size.split('x')
    if len(d) != 2:
        WARN('Invalid resize value "%s". Use e.g. "720x480"' % size)
        return None

    try:
        width = int(d[0])
        height = int(d[1])
    except ValueError:
        # no integers given
        WARN('Invalid resize value "%s". Use e.g. "720x480"' % size)
        return None

    return (width, height)

def __parse_crop(crop):
    if not crop:
        return None

    d = crop.split(':')
    if len(d) != 2:
        WARN('Invalid crop value "%s". Use e.g. "x1-x2:y1-y2"' % crop)
        return None

    x = d[1].split('-')
    y = d[0].split('-')

    if len(x) != 2 or len(y) != 2:
        WARN('Invalid crop value "%s". Use e.g. "x1-x2:y1-y2"' % crop)
        return None

    try:
        dx = (int(x[0]), int(x[1]))
        dy = (int(y[0]), int(y[1]))
    except ValueError:
        # no integers given
        WARN('Invalid crop value "%s". Use e.g. "x1-x2:y1-y2"' % crop)
        return None

    return (dx, dy)



# Progress
def print_progress_bar(perc):
    return '\x1b[1;32m#\x1b[1;0m'*perc + '-'*(100-perc)




