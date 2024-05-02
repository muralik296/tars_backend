# TARS Search Engine

Backend code for the TARS Project backend.

## Description
* Tech Stack: 
Backend: Django,Python
Frontend: React.js
Database: Elastic Search Cloud


## Getting Started

### Dependencies

* Prerequisites
* ex. MacOS, Windows 10, Node.js v21.4+, Node package manager (npm) , Python 3.7+, Make sure to have internet connection as it connects to elastic cloud

### Installing

* Once you unzipped it, you should add the .env file in the same level as the .env-example.txt file which is at the top most parent directory
* Just copy/paste the credentials in the .env example file to the .env
* If you'd like to use your own elastic cloud cluster, then make sure to run the db_setup file inside the db_utils directory.


### Follow the below steps to setup the backend project and get started

* Create a virtual environment for your django application

```
virtualenv -p python3 env
```

* (optional) If the above doesn't create a virtual environment successfully, run the below command

```
python3 -m venv venv
```

* Once you have done that, run the following to activate it

```
source ./env/bin/activate
```

* Install the python dependencies 

```
pip install -r requirements.txt
```


* cd (navigate) over to the 'ir' project directory

```
cd ir
```

* Once successfully installed you should be able to run the below to get your server up and running (at default port and host 8000)
```
python manage.py runserver
```

* The above should running your webserver at 'http://localhost:8000' and be able to accept requests

### Follow the below steps to setup the react frontend project and get started


* Once you have the backend up and running successfully, in a new terminal window navigate to the IR_Project folder

```
cd 
```

* Once you are in the build folder, if you already have **serve** package installed, you can skip this step. the below will install serve

```
npm install -g serve
```

* After successfully installing serve, you can type the below command in the terminal from the IR_Project directory to serve the static files

```
serve -s build 
```

* The above should start your frontend at 'http://localhost:3000' -> you can access this from your browser