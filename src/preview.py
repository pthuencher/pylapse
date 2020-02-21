# Standard imports

# 3rd pary imports
import cv2

# local imports
from src.constants import *
import src.helpers as helpers
from src.helpers import *



# Calculate preview image and show
def do_preview(args):
    sources = helpers.get_source_files(args.sourcepath)

    # Read preview image
    preview_path = sources[int(len(sources)/2)] # take from the middle
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