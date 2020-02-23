# Standard imports

# 3rd pary imports
import cv2

# local imports
from src.constants import *
import src.helpers as helpers
from src.helpers import *


def __process_image(img, args):
    # 1. crop image
    if args.crop:
        dx = args.crop[0]
        dy = args.crop[1]
        img = img[dx[0]:dx[1], dy[0]:dy[1]]

    # 2. transform image
    # TODO: implement e.g. pan, tilt, ...

    # 3. resize image
    if args.resize:
        img = cv2.resize(img, args.resize, interpolation = cv2.INTER_LINEAR)

    return img

# Calculate preview image and show
def do_preview(source, args):
    # Read preview image
    preview = source.get_preview()
    # Process preview image
    preview = __process_image(preview, args)

    # add data
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    cv2.rectangle(preview,(300,120),(10,10),BLACK,-1)
    cv2.putText(preview, 'Images: %d' % source.size, (20,30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, WHITE, 1, cv2.LINE_AA)
    cv2.putText(preview, 'Crop: %r' % [args.crop], (20,50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, WHITE, 1, cv2.LINE_AA)
    cv2.putText(preview, 'FPS: %d' % args.fps, (20,70), cv2.FONT_HERSHEY_SIMPLEX, 0.4, WHITE, 1, cv2.LINE_AA)
    cv2.putText(preview, 'Duration: %d sec(s)' % (source.size/args.fps), (20,90), cv2.FONT_HERSHEY_SIMPLEX, 0.4, WHITE, 1, cv2.LINE_AA)
    cv2.putText(preview, 'Resolution: %r' % [args.resize], (20,110), cv2.FONT_HERSHEY_SIMPLEX, 0.4, WHITE, 1, cv2.LINE_AA)

    # display preview image
    cv2.imshow('pylapse - %s' % source.directory, preview)
    cv2.waitKey(0)

    return True



# Render full timelapse video
def do_render(source, args):
    gen = source.image_generator()

    # Create VideoWriter
    try:
        # determine target video image size
        target_size = None
        if args.resize:
            target_size = args.resize
        elif args.crop:
            dx = (args.crop[0])[1] - (args.crop[0])[0]
            dy = (args.crop[1])[1] - (args.crop[1])[0]
            target_size = (dx, dy)
        else:
            preview = source.get_preview()
            width, height, _ = preview.shape
            target_size = (width, height)

        # create VideoWriter
        out = cv2.VideoWriter(args.output, cv2.VideoWriter_fourcc(*args.fourcc), args.fps, target_size)

        # Iterate over each image and write to video
        for i, img in enumerate(gen):
            # Process image
            img = __process_image(img, args)

            # write image
            out.write(img)

            # Display progress
            img_data = dict()
            img_data['index'] = i
            img_data['total'] = source.size
            img_data['percentage'] = round((i / source.size)*100, 1)
            img_data['progress_bar'] = create_progress_bar(int(img_data['percentage']))
            INFO('[ \x1b[1;32m{percentage}%\x1b[1;0m ] | [ {progress_bar} ] | [ {index} of {total} ]'.format(**img_data), overwrite=True)
        
        INFO('Output file: "%s"' % args.output)

    except KeyboardInterrupt:
        print('\n\n') # avoid \r issues
        out.release()
        choice = input('Aborted by user. Keep outfile "%s"? (y/N): ' % args.output)
        if choice != 'y':
            os.remove(args.output)
        return True
    except Exception as e:
        print('\n\n') # avoid \r issues
        out.release()
        raise e

    out.release()
    return True