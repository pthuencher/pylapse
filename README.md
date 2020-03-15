Create timelapse video from a given image sequence using opencv.

## Usage
```
usage: pylapse.py [-h] [-o FILENAME] [-f] [-v] [-p] [-r RESIZE] [-c CROP]
                  [-e EXT] [--fps FPS] [--fourcc FOURCC] [--no-colors]
                  [--version]
                  source

Create timelapse video from image sources.

positional arguments:
  source                path to the folder with source images.

optional arguments:
  -h, --help            show this help message and exit
  -o FILENAME, --output FILENAME
                        destination of the output video file.
  -f, --force-overwrite
                        force overwrite existing files.
  -v, --verbose         display verbose debug output.
  -p, --preview         preview (do not write any file).
  -r RESIZE, --resize RESIZE
                        resize images. (e.g. "1920x1080")
  -c CROP, --crop CROP  crop images. (x1-x2:y1-y2) (e.g. "0-1920:0-1080"")
  -e EXT, --ext EXT     extension of the output video file. (default=avi)
  --fps FPS             frames per second. (default=24)
  --fourcc FOURCC       FOURCC code of the output video file. (default=DIVX)
  --no-colors           force uncolored Output.
  --version             show program's version number and exit
```

## Build
Run `make all` to build a standalone executable in `dist/`.
