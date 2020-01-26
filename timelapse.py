# Standard imports
import argparse
import glob
import sys
import os

# 3rd pary imports
import cv2
import numpy as np
from colorama import init as colorama_init

# local imports
from constants import *
import helpers
from helpers import *



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
    parser.add_argument('-c', '--fourcc', help='FOURCC code of the output video file. (default=%s)' % DEFAULT_FOURCC)
    parser.add_argument('-e', '--ext', help='Extension of the output video file. (default=%s)' % DEFAULT_EXTENSION)
    parser.add_argument('--fps', help='Frames per second. (default=%d)' % DEFAULT_FPS)

    args = parser.parse_args()

    # Determine basepath
    args.basepath = os.getcwd()

    # Set verbosity status
    helpers.VERBOSE = args.verbose
    
    # Apply argument defauls
    args.dimension = parse_dimension(args.dimension)

    if not args.ext:
        args.ext = DEFAULT_EXTENSION
    if not args.fourcc:
        args.fourcc = DEFAULT_FOURCC
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

    DEBUG('Setup completed.')
    return args

# Calculate preview image and show
def do_preview(args):
    
    # Collect all images from source path
    files = glob.glob(os.path.join(args.sourcepath, '*'))
    nfiles = len(files)
    if nfiles < 1:
        ERROR('No files found in "%s"' % args.sourcepath, shutdown=True)
    INFO('Found %d images in source directory "%s"' % (nfiles, args.sourcepath))

    # Read preview image
    preview_path = files[int(len(files)/2)] # take from the middle
    preview_img = cv2.imread(preview_path)
    height, width, _ = preview_img.shape

    INFO('Original dimension: %dx%d' % (width, height))

    while height > 800 and width > 800:
        height /=2; height = int(height)
        width /= 2; width = int(width)

    INFO('Preview dimension: %dx%d' % (width, height))

    # resize image
    preview_img = cv2.resize(preview_img, (width, height), interpolation = cv2.INTER_LINEAR)

    # display preview image
    cv2.imshow('preview', preview_img)
    cv2.waitKey(0)

    return True

# Render full timelapse video
def do_render(args):

    # Collect all images from source path
    files = glob.glob(os.path.join(args.sourcepath, '*'))
    nfiles = len(files)
    if nfiles < 1:
        ERROR('No files found in "%s"' % args.sourcepath, shutdown=True)

    INFO('Found %d images in source directory "%s"' % (nfiles, args.sourcepath))
    INFO('Crop images to %dx%d' % args.dimension)

    # Read preview image
    preview_path = files[int(len(files)/2)] # take from the middle
    preview_img = cv2.imread(preview_path)
    height, width, _ = preview_img.shape

    # Create VideoWriter
    try:
        out = cv2.VideoWriter(args.output, cv2.VideoWriter_fourcc(*args.fourcc), args.fps, (args.dimension[0], args.dimension[1]))
        INFO('Creating output file "%s" FOURCC=%s' % (args.output, args.fourcc))

        # Iterate over each image and write to video
        for i, path in enumerate(files):

            # read image
            orig_img = cv2.imread(path)
            orig_width, orig_height, _ = orig_img.shape

            # TODO: calculate resize factor to avoid image stetch

            # resize image
            resize_img = cv2.resize(orig_img, (args.dimension[0], args.dimension[1]), interpolation = cv2.INTER_LINEAR)
            resize_width, resize_height, _ = resize_img.shape

            # write image
            out.write(resize_img)

            # Display progress
            img_data = dict()
            img_data['index'] = i
            img_data['total'] = nfiles
            img_data['percentage'] = round((i / nfiles)*100, 1)
            img_data['progress_bar'] = create_progress_bar(int(img_data['percentage']))
            INFO('[ \x1b[1;32m{percentage}%\x1b[1;0m ] | [ {progress_bar} ] | [ {index} of {total} ]'.format(**img_data), overwrite=True)
        
        INFO('Output file: "%s"' % args.output)

    except KeyboardInterrupt:
        print('\n') # avoid \r issues
        INFO('Aborted by user')
        return True
    except BaseException as e:
        print('\n\n')
        return e
    finally:
        out.release()

    return True

# Entry point
if __name__ == '__main__':
    args = setup()

    action = None
    if args.preview:
        action = do_preview
    else:
        # default action
        action = do_render

    # call action
    rc = action(args)

    # check return code
    if isinstance(rc, BaseException):
        ERROR('Exception occured')
        raise rc
    else:
        INFO('Exit.')
        sys.exit(0)

    

    

        
