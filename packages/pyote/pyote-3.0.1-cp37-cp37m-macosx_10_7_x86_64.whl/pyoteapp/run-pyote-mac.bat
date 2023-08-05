#!/bin/bash

# NOTE: If you're seeing this file in an editor, it's because you have not
#       yet asked MacOS to open this file using the terminal.app !!! To fix:
#       Right click on this file, select Get Info, and in Open with: select
#                      Terminal.app
        
cd Anaconda3

# Create/overwrite python script for starting up pyote
echo "from pyoteapp import pyote" >  run-pyote.py
echo "pyote.main()"               >> run-pyote.py

# Activate the Anaconda3 (base) environment
source activate

# Use python to execute the startup script created above
python run-pyote.py
