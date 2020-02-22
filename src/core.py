# Standard imports
import argparse
import sys
import os

# 3rd pary imports
import cv2
from colorama import init as colorama_init

# local imports
from src.constants import *
import src.helpers as helpers
from src.helpers import *
from src.preview import do_preview
from src.render import do_render


class ImageSource:
    directory = None
    ext = None
    paths = []


    def __init__(self, path, ext=['*.JPG', '*.jpg', '*.jpeg']):
        if not os.path.isdir(path):
            FATAL('Path "%s" is not a directory. Please point to a valid directory that contains the source files.' % args.sourcepath)

        self.directory = path
        self.ext = ext

        self.__get_image_paths()

    def __get_image_paths(self):
        self.paths = []

        for ext in self.ext:
            self.paths.extend(glob.glob(os.path.join(self.directory,'') + ext))

        self.size = len(self.paths)
        if self.size < 1:
            FATAL('No files found in "%s"' % self.directory)

        INFO('Found %d images in source directory "%s"' % (self.size, self.directory))

    def get_preview(self):
        preview_path = self.paths[int(len(self.paths)/2)] # take from the middle
        return cv2.imread(preview_path)

    def image_generator(self):
        for path in self.paths:
            yield cv2.imread(path)



# Setup routine
def setup():
    colorama_init()

    # Setup ArgumentParser
    parser = argparse.ArgumentParser(description='Create timelapse video from image sources.')

    parser.add_argument('source', help='Path to the folder with source images.')
    parser.add_argument('-o', '--output', metavar='FILENAME',help='Destination of the output video file.')
    parser.add_argument('-f', '--force-overwrite', action='store_true',help='Force overwrite existing files.')
    parser.add_argument('-v', '--verbose', action='store_true',help='Display verbose debug output.')
    parser.add_argument('-p', '--preview', action='store_true',help='Preview (do not write any file).')
    parser.add_argument('-r', '--resize', help='Resize video images. (e.g. "1920x1080")')
    parser.add_argument('-c', '--crop', help='Crop video images. (x1-x2:y1-y2) (e.g. "0-500:0-750"")')
    parser.add_argument('-e', '--ext', help='Extension of the output video file. (default=%s)' % DEFAULT_EXTENSION)
    parser.add_argument('--fps', help='Frames per second. (default=%d)' % DEFAULT_FPS)
    parser.add_argument('--fourcc', help='FOURCC code of the output video file. (default=%s)' % DEFAULT_FOURCC)
    parser.add_argument('--no-colors', action='store_true',help='Force uncolored Output.')
    parser.add_argument('--version', action='version', version=PYTHON_TIMELAPSE_VERSION)

    args = parser.parse_args()

    # Set verbosity status
    helpers.VERBOSE = args.verbose

    # Set output color status
    helpers.COLORS = not args.no_colors

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
    DEBUG('Arguments: %r' % args)

    # Check preconditions    
    #  1.) Source folder existence
    args.sourcepath = os.path.abspath(args.source)
    DEBUG('Sourcepath: %s' % args.sourcepath)
    if not os.path.isdir(args.sourcepath):
        FATAL('Path "%s" is not a directory. Please point to a valid directory that contains the source files.' % args.sourcepath)

    # 2.) Parse resize & crop parameters
    args.resize = parse_resize(args.resize)
    if args.resize: DEBUG('Resize: %dx%d' % args.resize)
    args.crop = parse_crop(args.crop)
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

# Entry point
if __name__ == '__main__':
    args = setup()
    DEBUG('Setup completed.')

    source = ImageSource(args.sourcepath)

    action = None
    if args.preview:
        action = do_preview
    else:
        # default action
        action = do_render

    # call action
    DEBUG('Execute action: %s' % action.__name__)
    action(source, args)

    INFO('Exit.')
    sys.exit(0)


    

        
