#!/bin/bash

# Check for Python
if ! command -v python3 &> /dev/null
then
    echo "Python could not be found. Please install Python and try again."
    exit
fi

# Setup a virtual environment and install the dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

export FLASK_APP=app.py
flask run
