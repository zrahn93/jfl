# JFL
### Welcome to the Jeff Fisher League

This repository contains source code for a ReactJS website running a Flask web server.
The application is containerized for hosting in the cloud
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
    docker run -p 3306:3306 -v mysql-volume:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql/mysql-server
    cd jfl_services
    docker build -t jfl_services .
    docker run --rm -d --network host jfl_services
    cd ../jfl_gui
    docker build -t jfl_gui .
    docker run --rm -d --network host --env REACT_APP_API_IP=http://localhost:5000 jfl_gui
```

### TODO:
* Create League page
* Create Standings page
* NFL team page updates
* Update results to include scores
* APIs & Lambda functions
* Profiles
* Notifications: nice to have
* Team selection with GIFs: nice to have
