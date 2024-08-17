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

# Get the Flask server's PID
FLASK_PID=$!

# If the script is being run by a CI system
if [ "$CI" = true ] || [ "$TRAVIS" = true ]; then
    # Wait for the Flask server to start
    sleep 5

    # Send HTTP requests to the Flask application and check the responses
    if curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5000 | grep -q "200" &&
       curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5000/budget | grep -q "200" &&
       curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5000/transactions | grep -q "200"
    then
        echo "All checks passed."
    else
        echo "One or more checks failed."
    fi

    # Stop the Flask server
    kill $FLASK_PID
fi