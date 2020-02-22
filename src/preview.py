# Standard imports

# 3rd pary imports
import cv2

# local imports
from src.constants import *
import src.helpers as helpers
from src.helpers import *



# Calculate preview image and show
def do_preview(source, args):
    # Read preview image
    preview = source.get_preview()

    # crop image
    if args.crop:
        dx = args.crop[0]
        dy = args.crop[1]
        preview = preview[dx[0]:dx[1], dy[0]:dy[1]]

    # resize image
    if args.resize:
        preview = cv2.resize(preview, args.resize, interpolation = cv2.INTER_LINEAR)

    # display preview image
    cv2.imshow('preview', preview)
    cv2.waitKey(0)

    return True