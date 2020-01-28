Create timelapse video from a given image sequence.

## Usage
```
usage: timelapse.py [-h] [-o FILENAME] [-f] [-v] [-p] [-d DIMENSION]
                    [-c FOURCC] [-e EXT] [--fps FPS] [--version]
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
  -d DIMENSION, --dimension DIMENSION
                        Dimension of the output video file.
                        (default=1920x1080)
  -c FOURCC, --fourcc FOURCC
                        FOURCC code of the output video file. (default=DIVX)
  -e EXT, --ext EXT     Extension of the output video file. (default=avi)
  --fps FPS             Frames per second. (default=24)
  --version             show program's version number and exit
```

## Example
```
$ python timelapse.py "C:\Users\example\Images\TripXY" -o "C:\Users\example\Desktop\out.avi" -d "1920x1080"

[timelapse] Found 2385 images in source directory "C:\Users\example\Images\TripXY"
[timelapse] Crop images to 1920x1080
[timelapse] Creating output file "out.avi" FOURCC=DIVX
[timelapse] [ 50.0% ] | [ #################################------------------------------ ] | [ 1173 of 2385 ]

```
