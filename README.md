Create a timelapse video from image frames.

## Usage
```
usage: pylapse.py [-h] [-o FILE] [-f] [--debug] [--preview] [--resize RESIZE] [--crop CROP] [--ext EXT] [--fps FPS] [--fourcc FOURCC] [--no-colors] [-v] source

Create timelapse video from image frames.

positional arguments:
  source                load image frames from source

optional arguments:
  -h, --help            show this help message and exit
  -f, --force-overwrite
                        force overwrite existing files
  --debug               display verbose debug output
  --no-colors           force uncolored output
  -v, --version         show program's version number and exit

output:
  -o FILE, --output FILE
                        render video to FILE
  --preview             preview (do not write any file)

settings:
  --ext EXT             extension of the final video file. (default: avi)
  --fps FPS             frames per second (default: 30)
  --fourcc FOURCC       FOURCC code of the final video file (default: DIVX)

transform:
  --resize RESIZE       resize images (example: 1920x1080)
                        
                            3840x2160 (16:9) 4K
                            1920x1080 (16:9) Full HD
                            1280x720  (16:9)
                            2880x2160 (4:3)
                            1440x1080 (4:3)
                            640x480   (4:3)
                        
                         
  --crop CROP           crop images (example: 0-1920:0-1080)
```

## Build
Run `make all` to build a standalone executable in `dist/`.
