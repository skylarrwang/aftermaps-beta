# AfterMaps (Release Candidate 1)

**Team Members:** Mason Abrell, Pratiksha Bhattacharyya, Kevin Jin, Skylar Wang

**NetIDs:** mma88, pb794, kwj9, srw74

## Description

AfterMaps is a web application that crowdsources user-contributed reports of road blockages, designed to be used in disaster response situations. The RC1 version of AfterMaps contains an interactive map for input and output. A user submits a report of a road blockage by clicking a location on the map; this location is associated with a specific locational structure (or "way") in our database. The app calculates the user's credibility based on past reports and associates it with the report. User reports are then displayed on the interactive map.

## Installation

1. Install the required Python packages by executing the command:
    * `pip install -r requirements.txt`
2. To run the server, execute the command:
    * `python runserver.py [port]`

## Usage

To access the server, click the link given in the Flask output. Follow the given instructions to create an account and begin submitting reports.

The user-facing version of AfterMaps will be accessible as a web app hosted on Amazon Web Services.
