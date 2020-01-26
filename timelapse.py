# Standard imports
import argparse
import glob
import sys
import os

# 3rd pary imports
import cv2
import numpy as np
from colorama import init as colorama_init, Fore, Back, Style

# Defaults
DEFAULT_FPS = 24
DEFAULT_OUTPUT_SIZE = (1920, 1080) # full HD
DEFAULT_OUTPUT_EXT = 'avi'
DEFAULT_OUTPUT_FILENAME = 'out'

# Globals
VERBOSE = False
PREVIEW = False

# Logging macros
def ERROR(msg, shutdown=False):
    print('[' + Fore.RED + 'ERROR' + Style.RESET_ALL + '] ' + str(msg))
    if shutdown:
        sys.exit(1)

def DEBUG(msg):
    global VERBOSE
    if VERBOSE:
        print('[DEBUG] ' + str(msg))

def INFO(msg, color=None, overwrite=False):
    end = '\r' if overwrite else '\n'
    print('[' + Fore.YELLOW + 'timelapse' + Style.RESET_ALL + '] ' + str(msg), end=end)

def parse_dimension(dim):
    if not dim:
        return DEFAULT_OUTPUT_SIZE
    
    d = dim.split('x')
    if len(d) != 2:
        ERROR('Failed to parse dimension "%s". Use e.g. 720x480' % dim, shutdown=True)

    return (int(d[0]), int(d[1]))

def create_progress_bar(perc):
    return '\x1b[1;32m#\x1b[1;0m'*perc + '-'*(100-perc)


# Setup routine
def setup():
    colorama_init()

    # Setup ArgumentParser
    parser = argparse.ArgumentParser(description='Create timelapse video from image sources.')

    parser.add_argument('source', help='Path to the folder with source photos.')
    parser.add_argument('-o', '--output', metavar='FILENAME',help='Destination of the output video file.')
    parser.add_argument('-f', '--force-overwrite', action='store_true',help='Force overwrite existing files.')
    parser.add_argument('-v', '--verbose', action='store_true',help='Display verbose debug output.')
    parser.add_argument('-p', '--preview', action='store_true',help='Preview (do not write any file).')
    parser.add_argument('-d', '--dimension', help='Dimension of the output video file. (default=1920x1080)')
    parser.add_argument('--ext', help='Format of the output video file. (default=%s)' % DEFAULT_OUTPUT_EXT)
    parser.add_argument('--fps', help='Frames per second. (default=%d)' % DEFAULT_FPS)

    args = parser.parse_args()

    # Determine basepath
    args.basepath = os.getcwd()

    # Set verbosity status
    global VERBOSE
    VERBOSE = args.verbose
    global PREVIEW
    PREVIEW = args.preview
    
    # Apply argument defauls
    args.dimension = parse_dimension(args.dimension)

    if not args.ext:
        args.ext = DEFAULT_OUTPUT_EXT
    if not args.fps:
        args.fps = DEFAULT_FPS
    if not args.output:
        args.output = '%s.%s' % (DEFAULT_OUTPUT_FILENAME, args.ext)
    elif '.' not in args.output:
        args.output = '%s.%s' % (args.output, args.ext)
    
    # Type conversion
    args.fps = int(args.fps)
    DEBUG(args)

    # Check preconditions    
    #  1.) Source folder existence
    args.sourcepath = args.source if os.path.isabs(args.source) else os.path.join(args.basepath, args.source)
    if not os.path.isdir(args.sourcepath):
        ERROR('Path "%s" is not a directory. Please point to a valid directory that contains the source files.' % args.sourcepath, shutdown=True)

    #  2.) Source folder content
    if not os.listdir(args.sourcepath):
        ERROR('Directory "%s" does not contain any image file.' % args.sourcepath, shutdown=True)

    #  3.) Output file existence (if not preview)
    if (args.preview): return args

    args.outputpath = args.output if os.path.isabs(args.output) else os.path.join(args.basepath, args.output)
    if os.path.exists(args.outputpath):
        if args.force_overwrite:
            INFO('Overwriting existing file "%s"' % args.outputpath)
        else:
            choice = input('File "%s" already exists. Overwrite? (y/N): ' % args.outputpath)
            if choice != 'y':
                ERROR('Aborted. Use -o to specify another output filename.', shutdown=True)

    return args

# Entry point
if __name__ == '__main__':
    args = setup()

    # Collect all images from source path
    files = glob.glob(os.path.join(args.sourcepath, '*'))
    nfiles = len(files)
    if nfiles < 1:
        ERROR('No files found in "%s"' % args.sourcepath, shutdown=True)

    INFO('Found %d images in source directory "%s"' % (nfiles, args.sourcepath))
    INFO('Target dimension: %dx%d' % (args.dimension[0], args.dimension[1]))

    # Create VideoWriter
    try:
        if not PREVIEW: 
            out = cv2.VideoWriter(args.output, cv2.VideoWriter_fourcc(*'DIVX'), args.fps, args.dimension)

        # Iterate over each image and write to video
        for i, path in enumerate(files):

            img = cv2.imread(path)
            width, height, _ = img.shape

            # resize image
            resize_img = cv2.resize(img, args.dimension, interpolation = cv2.INTER_LINEAR)
            resize_width, resize_height, _ = resize_img.shape

            if PREVIEW:
                cv2.imshow('preview', resize_img)
                cv2.waitKey(0)
                break

            img_data = dict()
            img_data['index'] = i
            img_data['total'] = nfiles
            img_data['percentage'] = round((i / nfiles)*100, 1)
            img_data['width'] = width
            img_data['height'] = height
            img_data['resize_width'] = resize_width
            img_data['resize_height'] = resize_height
            img_data['progress_bar'] = create_progress_bar(int(img_data['percentage']))
            INFO('[ \x1b[1;32m{percentage}%\x1b[1;0m ] | [ {progress_bar} ] | [ {index} of {total} ]'.format(**img_data), overwrite=True)

            # write image
            if not PREVIEW:
                out.write(resize_img)
        
        INFO('Processing.. Done')
        if not args.preview: INFO('Output file: "%s"' % args.output)

    except BaseException as e:
        print('\n\n')
        raise e
    finally:
        if not PREVIEW: 
            out.release()

        
