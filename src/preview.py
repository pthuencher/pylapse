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

    # add data
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    cv2.rectangle(preview,(300,120),(10,10),BLACK,-1)
    cv2.putText(preview, 'Images: %d' % source.size, (20,30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, WHITE, 1, cv2.LINE_AA)
    cv2.putText(preview, 'Crop: %r %r' % args.crop, (20,50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, WHITE, 1, cv2.LINE_AA)
    cv2.putText(preview, 'FPS: %d' % args.fps, (20,70), cv2.FONT_HERSHEY_SIMPLEX, 0.4, WHITE, 1, cv2.LINE_AA)
    cv2.putText(preview, 'Duration: %d sec(s)' % (source.size/args.fps), (20,90), cv2.FONT_HERSHEY_SIMPLEX, 0.4, WHITE, 1, cv2.LINE_AA)
    cv2.putText(preview, 'Resolution: %d x %d' % args.resize, (20,110), cv2.FONT_HERSHEY_SIMPLEX, 0.4, WHITE, 1, cv2.LINE_AA)

    # display preview image
    cv2.imshow('pylapse - %s' % source.directory, preview)
    cv2.waitKey(0)

    return True

