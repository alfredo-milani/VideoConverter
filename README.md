Tool to convert media files when they are moved to a directory



In MacOS ecosystem execute the following commands:
    $ export LC_ALL=en_US.UTF-8
    $ export LANG=en_US.UTF-8


Installation:

    [ optional ]
    ### Install required tools in virtual environment
    $ pip install virtualenv
    ### Create virtual environment named VideoConveter
    $ virtualenv VideoConverter  # or $ virtualenv -p /path/python3 VideoConverter
    ### Activate virtual environment
    $ source VideoConverter/bin/activate
    ### Deactivate virtual environment
    $ deactivate


    [ mandatory ]
    $ alias py='python -m pip'
    ### Install required pip-tools for requirements installation
    $ py install pip-tools
    ### Move to root project directory
    $ cd /project_root/
    ### Read requirements to install
    $ pip-compile --output-file requirements.txt requirements.in
    ### Install requierd packages
    $ pip-sync
    ### Start main
    $ python src/Main.py
