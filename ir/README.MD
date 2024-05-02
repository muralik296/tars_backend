# TARS Search Engine Backend

Backend code for the TARS Project backend.

## Description

Written in Python and usage of Django framework. On running the webserver, you should have access to the API endpoints to the Django server

## Getting Started

### Dependencies

* Prerequisites
* ex. MacOS, Windows 10, Python 3.7+, Make sure to have internet connection as it connects to elastic cloud

### Installing

* Once you unzipped it, you should add the .env file in the same level as the .env-example.txt file which is at the top most parent directory
* Just copy/paste the credentials in the .env example file to the .env
* If you'd like to use your own elastic cloud cluster, then make sure to run the db_setup file inside the db_utils directory.


### Follow the below steps to setup the project and get started

* Create a virtual environment for your django application

```
virtualenv -p python3 env
```

* Once you have done that, run the following to activate it

```
python ./env/bin/activate
```

* Install the python dependencies 

```
pip install -r requirements.txt
```

* Once successfully installed you should be able to run the below to get your server up and running (at default port and host 8000)

```
python manage.py runserver
```