# Standard imports

# 3rd pary imports
import cv2

# local imports
from src.constants import *
import src.helpers as helpers
from src.helpers import *



# Render full timelapse video
def do_render(args):
    sources = helpers.get_source_files(args.sourcepath)

    # Read preview image
    preview_path = sources[int(len(sources)/2)] # take from the middle
    preview_img = cv2.imread(preview_path)
    height, width, _ = preview_img.shape

    # Create VideoWriter
    try:
        # determine target video image dimension
        dim = None
        if args.resize:
            dim = args.resize
        elif args.crop:
            dx = (args.crop[0])[1] - (args.crop[0])[0]
            dy = (args.crop[1])[1] - (args.crop[1])[0]
            dim = (dx, dy)
        else:
            dim = (width, height)

        # create VideoWriter
        out = cv2.VideoWriter(args.output, cv2.VideoWriter_fourcc(*args.fourcc), args.fps, (dim[0], dim[1]))

        INFO('Creating output file "%s" FOURCC=%s' % (args.output, args.fourcc))
        if args.crop: INFO('Crop video images to %r %r' % args.crop)
        INFO('Resize video images to %dx%d' % dim)

        # Iterate over each image and write to video
        for i, path in enumerate(sources):

            # read image
            orig_img = cv2.imread(path)

            # (optional) crop image
            if args.crop:
                x = args.crop[0]
                y = args.crop[1]
                orig_img = orig_img[x[0]:x[1], y[0]:y[1]]

            orig_width, orig_height, _ = orig_img.shape

            # resize image
            resize_img = cv2.resize(orig_img, (dim[0], dim[1]), interpolation = cv2.INTER_LINEAR)
            resize_width, resize_height, _ = resize_img.shape

            # write image
            out.write(resize_img)

            # Display progress
            img_data = dict()
            img_data['index'] = i
            img_data['total'] = len(sources)
            img_data['percentage'] = round((i / len(sources))*100, 1)
            img_data['progress_bar'] = create_progress_bar(int(img_data['percentage']))
            INFO('[ \x1b[1;32m{percentage}%\x1b[1;0m ] | [ {progress_bar} ] | [ {index} of {total} ]'.format(**img_data), overwrite=True)
        
        INFO('Output file: "%s"' % args.output)

    except KeyboardInterrupt:
        print('\n\n') # avoid \r issues
        INFO('Aborted by user')
        return True
    except Exception as e:
        print('\n\n') # avoid \r issues
        raise e
    finally:
        out.release()

    return True