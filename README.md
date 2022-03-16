# JFL
### Welcome to the Jeff Fisher League

This repository contains source code for a ReactJS website running a Flask web server.
The application is containerized for hosting in AWS
Future: Several Lambda functions query information from NFL & FanDuel APIs

## Installation

To run locally, you will need the following prerequisites: **Python 3, mysql, Flask**

```bash
    sudo apt-get install libmysqlclient-dev
    pip install mysql boto3 Flask
```

## Running the application

To run the back end web server:
```bash
    python run.py
```

To run the front end:
```bash
    npm install
    npm start
```

To containerize and run with docker:
```bash
    docker build -t jfl .
    docker run --rm -d --network host jfl
```

### TODO:
APIs & Lambda functions
Docker containers
Team selection with GIFs: nice to have
