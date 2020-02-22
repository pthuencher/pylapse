Create timelapse video from a given image sequence using opencv.

## Usage
```
usage: pylapse.py [-h] [-o FILENAME] [-f] [-v] [-p] [-r RESIZE] [-c CROP]
                  [-e EXT] [--fps FPS] [--fourcc FOURCC] [--no-colors]
                  [--version]
                  source

Create timelapse video from image sources.

positional arguments:
  source                Path to the folder with source images.

optional arguments:
  -h, --help            show this help message and exit
  -o FILENAME, --output FILENAME
                        Destination of the output video file.
  -f, --force-overwrite
                        Force overwrite existing files.
  -v, --verbose         Display verbose debug output.
  -p, --preview         Preview (do not write any file).
  -r RESIZE, --resize RESIZE
                        Resize video images. (e.g. "1920x1080")
  -c CROP, --crop CROP  Crop video images. (x1-x2:y1-y2) (e.g. "0-500:0-750"")
  -e EXT, --ext EXT     Extension of the output video file. (default=avi)
  --fps FPS             Frames per second. (default=24)
  --fourcc FOURCC       FOURCC code of the output video file. (default=DIVX)
  --no-colors           Force uncolored Output.
  --version             show program's version number and exit
```

## Build
Run `make all` to build a standalone executable in `dist/`.
