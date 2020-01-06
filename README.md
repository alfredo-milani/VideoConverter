# Table of contents
1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Installation](#installation)
    1. [Optional](#installation-optional)
    2. [Mandatory](#installation-mandatory)
4. [Usage](#usage)
5. [Note](#note)



## 1. Introduction <a name="introduction"></a>
Tool to convert media files when they are moved to a directory

## 2. Requirements <a name="requirements"></a>
The following tools are required:
1. [ffmpeg](https://github.com/FFmpeg/FFmpeg)
2. [python-video-converter](https://github.com/senko/python-video-converter)

## 3. Installation <a name="installation"></a>

### 3.1 Optional <a name="installation-optional"></a>

```bash
# Install virtualenv package for Python:
pip install virtualenv

# Create virtual environment named VideoConveter:
virtualenv VideoConveter
# or
virtualenv -p python3 VideoConveter

# Activate virtual environment:
source VideoConveter/bin/activate

# Deactivate virtual environment:
deactivate
```

### 3.2 Mandatory <a name="installation-mandatory"></a>

```bash
# Install required pip-tools for requirements installation:
alias py='python -m pip'
py install pip-tools

# Move to root project directory:
cd /project_root/

# Read requirements to install:
pip-compile --output-file requirements.txt requirements.in

# Install required packages:
pip-sync
```

## 4. Usage <a name="usage"></a>

Modify file res/conf/log.ini, section 'handler_file_handler', key 'args', prefix "/var/log/Dispatcher_", to specify a valid base path for log file.

```ini
# Default:
[handler_file_handler]
. . .
args = ("/var/log/Dispatcher_" + time.strftime("%%Y%%m%%d") + ".log", "a")
```

Start main:

```bash
python src/Application.py
```

You could specify a configuration file:
```bash
python src/Application.py /path/custom_config.ini
```

Configurations file example:
```ini
# Legend
#   [opt] := optional parameter
#   [dft] := default value
#   [mnd] := mandatory parameter


[GENERAL]
# [opt] - Configuration file for logging service
# [dft] - res/conf/log.ini
# log.config_file = /Volumes/Ramdisk/log.ini

# [opt] - Directory for temporary files
# [dft] - /tmp
# tmp = /Volumes/Ramdisk/tmp

# [opt] - Processes for conversion handling
processes = 5

[MEDIA]
# [mnd] - Input directory
in.folder = /Volumes/Ramdisk/test/in

# [opt] - Directory where will be moved files after conversion
# NOTE: leave empty this parameter to delete files after conversion
# NOTE: if this parameter will not be specified then not action will be taken
in.converted.folder =
# in.converted.folder = /Volumes/Ramdisk/test/converted

# [opt] - Frequency (seconds) for checking new files
# [dft] - 1
in.timeout = 0.5

# [mnd] - Directory for storing converted files
out.folder = /Volumes/Ramdisk/test

# [mnd] - Conversion format. Follow JSON format
out.format = {
                'format' : 'avi',
                'audio' : {
                    'codec' : 'mp3',
                    'samplerate' : 11025,
                    'channels' : 2
                },
                'video' : {
                    'codec' : 'h264',
                    'width' : 720,
                    # 'height' : 400,
                    # 'fps' : 15
                }
             }

# [opt] - Path of requested binary
# [dft] - Binaries for ffmpeg and ffprobe will be searched in PATH environment variable
ffmpeg = /usr/local/opt/ffmpeg/ffmpeg
ffprobe = /usr/local/opt/ffmpeg/ffprobe
```

## 5. Note <a name="note"></a>
* In MacOS ecosystem execute the following commands in a bash shell:
```bash
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```

* [python-video-converter](https://github.com/senko/python-video-converter) is a wrapper for ffmpeg Python by [senko](https://github.com/senko).
