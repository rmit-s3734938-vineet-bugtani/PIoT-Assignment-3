# PIoT-Assignment-3

## Team Members

Ryan Cassidy (s3740446) - Worked on Task-B and C (API, agent.py, socketing between Pi's, bluetooth, qr, Trello Board, Unit Testing)

Vineet Bugtani (s3734938) - Worked on Task-A and C (API, Site, Google Cloud Database,, qr Unit Testing, Trello Board, Google Maps)

Akshay Sunil Salunke (s3730440) - Worked on Task-A and B (API, Site, Google Voice Recognition, Trello Board, Sphinx Documentation)

Pui Ling Chan (s3561165) - Worked on Task-A (API, Site, Google Cloud Database, Sphinx Documentation, Trello Board)

Screenshots of github and trello board can be found in the Screenshots directory

Trello board: https://trello.com/b/aB9so8Rl/programming-iot-assignment-3

## Feature Description

Group assignment 3 for RMIT Programming Internet of Things 2020
Features a Flask website for administration over assignment 2 features and an agent script for managing engineer features.

Site utilizes google assistant, flask framework and pushbullet.
Agent utilizes qr code packages, opencv and pybluez/bluetooth packages.

Agent/QRCodes contains some QR codes for input into the QR option in the agent.py script

Site can create and delete cars/users/bookings, set cars for repair (along with pushbullet notification), display graphs for manager accounts and display a map for engineers to see where their repair jobs are located.
Google Assistant api is used for providing a means of users using their voice to search for cars/users/bookings in a search bar.

Agent can scan for nearby bluetooth devices in order to authorize an engineer owned device and unlock a nearby car
Agent can also scan a QR code in order to retrieve information about the engineer.

### To run the site
Install requirements under requirements.txt
Set the ip in flask_main.py appropraitely for your device
Navigate to Master and run python3 flask_main.py

### To run the agent
Install requirements under requirements.txt (Make sure to correctly install opencv and bluetooth)
Navigate to Agent
Edit the config.json to your selected car ID and set the IP to the device hosting the site
Run python3 agent.py

### Unit Tests
Separate unit tests can be found in the Agent and Master directories
Agent tests require the site to be running and connectable
Master tests just require the correct packages to be installed.

### Sphinx
Sphinx documentation has been generated and can be viewed in a browser by opening the html under docs/_build/html/index.html

`Master/audio` folder contains a few sample audio clips to test voice search.
To run voice search:
- Run the flask website in one terminal.
- Open second terminal and `python voice_search.py <file>.flac`
