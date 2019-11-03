# Table of contents
1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Installation](#installation)
    1. [Optional](#installation-optional)
    2. [Mandatory](#installation-mandatory)
4. [Note](#note)



## 1. Introduction <a name="introduction"></a>
Tool to convert media files when they are moved to a directory

## 2. Requirements <a name="requirements"></a>
The following tools are required:
1. [ffmpeg](https://github.com/FFmpeg/FFmpeg)
2. [python-video-converter](https://github.com/senko/python-video-converter)

## 3. Installation <a name="installation"></a>

### 3.1 Optional <a name="installation-optional"></a>
Install virtualenv package for Python:
```bash
pip install virtualenv
```

Create virtual environment named VideoConveter:
```bash
virtualenv VideoConverter
```
or
```bash
virtualenv -p python3 VideoConverter
```

Activate virtual environment
```bash
source VideoConverter/bin/activate
```

Deactivate virtual environment
```bash
deactivate
```

### 3.2 Mandatory <a name="installation-mandatory"></a>
Install required pip-tools for requirements installation
```bash
alias py='python -m pip'
py install pip-tools
```

Move to root project directory
```bash
cd /project_root/
```

Read requirements to install
```bash
pip-compile --output-file requirements.txt requirements.in
```

Install requierd packages
```bash
pip-sync
```

Start main
```bash
python src/Main.py
```

## 4. Note <a name="note"></a>
* In MacOS ecosystem execute the following commands in a bash shell:
```bash
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```

* [python-video-converter](https://github.com/senko/python-video-converter) is a wrapper for ffmpeg Python by [senko](https://github.com/senko).
