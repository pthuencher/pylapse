# Standard imports
import glob
import sys
import os

# 3rd pary imports
import cv2
from colorama import init as colorama_init

# local imports
import helpers
from helpers import DEBUG, INFO, WARN, ERROR, FATAL
import transform


class PylapseEngine:

    def __init__(self, args):
        self.args = args
        if not os.path.isdir(args.sourcepath):
            FATAL('Path "%s" is not a directory. Please point to a valid directory that contains the source files.' % path)

        self.image_paths = self.__collect_image_paths()
        self.image_count = len(self.image_paths)


    def execute(self):
        if args.preview:
            DEBUG('Execute action: preview')
            self.__do_preview()
        else:
            DEBUG('Execute action: render')
            # default action
            self.__do_render()


    def __collect_image_paths(self):
        paths = []

        for ext in ['*.JPG', '*.jpg', '*.jpeg']:
            paths.extend(glob.glob(os.path.join(self.args.sourcepath,'') + ext))

        count = len(paths)
        if count < 1:
            WARN('No files found in "%s"' % self.args.sourcepath)

        INFO('Found %d images in source directory "%s"' % (count, self.args.sourcepath))
        return paths

    def __get_preview_image(self):
        return cv2.imread(self.image_paths[0])

    def __image_generator(self):
        for path in self.image_paths:
            yield cv2.imread(path)

    def __transform(self, img):
        if self.args.crop:
            img = transform.crop(img, self.args.crop)
        if self.args.resize:
            img = transform.resize(img, self.args.resize)
        
        return img


    def __do_preview(self):
        # Read preview image
        preview = self.__get_preview_image()
        # Apply transformation
        preview = self.__transform(preview)


        # add data
        BLACK = (0,0,0)
        WHITE = (255,255,255)
        cv2.rectangle(preview,(300,120),(10,10),BLACK,-1)
        cv2.putText(preview, 'Images: %d' % self.image_count, (20,30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, WHITE, 1, cv2.LINE_AA)
        cv2.putText(preview, 'FPS: %d' % int(self.args.fps), (20,50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, WHITE, 1, cv2.LINE_AA)
        cv2.putText(preview, 'Duration: %d sec(s)' % (self.image_count/int(self.args.fps)), (20,70), cv2.FONT_HERSHEY_SIMPLEX, 0.4, WHITE, 1, cv2.LINE_AA)
        cv2.putText(preview, 'Crop: %r' % [self.args.crop], (20,90), cv2.FONT_HERSHEY_SIMPLEX, 0.4, WHITE, 1, cv2.LINE_AA)
        cv2.putText(preview, 'Resize: %r' % [self.args.resize], (20,110), cv2.FONT_HERSHEY_SIMPLEX, 0.4, WHITE, 1, cv2.LINE_AA)

        # display preview image
        cv2.imshow('pylapse - %s' % self.args.sourcepath, preview)
        cv2.waitKey(0)

        return True
    
    def __do_render(self):
        gen = self.__image_generator()

        # determine target video image size
        target_size = None
        if args.resize:
            target_size = args.resize
        elif args.crop:
            dx = (args.crop[0])[1] - (args.crop[0])[0]
            dy = (args.crop[1])[1] - (args.crop[1])[0]
            target_size = (dx, dy)
        else:
            preview = self.__get_preview_image()
            height, width, _ = preview.shape
            target_size = (width, height)

        DEBUG("Target video size will be %dx%d" % target_size)

        try:
            # create VideoWriter
            out = cv2.VideoWriter(args.output, cv2.VideoWriter_fourcc(*args.fourcc), int(args.fps), target_size)

            # Iterate over each image and write to video
            for i, img in enumerate(gen):
                # Apply transformation
                img = self.__transform(img)

                # write image
                out.write(img)

                # Display progress
                img_data = dict()
                img_data['index'] = i
                img_data['total'] = self.image_count
                img_data['percentage'] = round((i / self.image_count)*100, 1)
                img_data['progress_bar'] = helpers.print_progress_bar(int(img_data['percentage']))
                INFO('[ \x1b[1;32m{percentage}%\x1b[1;0m ] | [ {progress_bar} ] | [ {index} of {total} ]'.format(**img_data), overwrite=True)
            
            INFO('')
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





if __name__ == '__main__':

    colorama_init()

    print(
        f"""
                     _                      
         _ __  _   _| | __ _ _ __  ___  ___ 
        | '_ \| | | | |/ _` | '_ \/ __|/ _ \\
        | |_) | |_| | | (_| | |_) \__ \  __/
        | .__/ \__, |_|\__,_| .__/|___/\___|
        |_|    |___/        |_|             

        {helpers.VSN}

        """
    )

    args = helpers.parse_args()
    pylapse = PylapseEngine(args)
    pylapse.execute()

    INFO('Exit.')
    sys.exit(0)


    

        
