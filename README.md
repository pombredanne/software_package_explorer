# Software Package Explorer via Flask Web App

This web application displays some key information about softwares that a system knows. 
On Debian and Ubuntu Linux distros there is a file /var/lib/dpkg/status that contains various infomration of software packages
that the system knows about. This web app exposes some details of such packages on a web browser by providing a straight-forward
way to explore such packages.

## Getting Started

This web app is built with Python3.6 and Flask + other utility packages that Flask incorporates and gunicorn (all in requirements.txt).
Before cloning this repository install python3.6 or later if you don't already have it.

```
sudo apt-get update
sudo apt-get install python3.6
```

Additionally for package isolation, virtualenv might be useful, so go ahead and install virtual env with pip

```
sudo apt-get install python3-pip
sudo pip3 install virtualenv
```

### Prerequisites

Python3.6 or later

comes with flask
* Click==7.0
* Flask==1.1.1
* itsdangerous==1.1.0
* Jinja2==2.10.3
* MarkupSafe==1.1.1
* Werkzeug==0.16.0

package install
* pip==19.3.1
* setuptools==45.0.0
* wheel==0.33.6

Python Wsgi HTTP server
* gunicorn==20.0.4


### Installing

Install Python3.6 or later
```
sudo apt-get update
sudo apt-get install python3.6
```
Install pip (package installer)
```
sudo apt-get install python3-pip
```
Install virtualenv (package isolation)
```
sudo pip3 install virtualenv 
```
Install git (version control)
```
sudo apt install git
```
Make a project directory
```
mkdir projects
cd projects/
```
clone repo
```
git clone https://github.com/sakkep93/software_package_explorer.git
cd software_package_explorer
```
Create virtualenv
```
virtualenv env --python=python
source env/bin/activate
```
Install packages via pip
```
pip install -r requirements.txt
```
Run locally
```
gunicorn app:app
```
Finally open a browser, go to address showing in terminal (localhost) and wonder


## Deployment

Deployed with Heroku cli and live version is at:
https://software-package-explorer.herokuapp.com/

## Built With

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - The web framework used
* [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) - Template engine (comes with Flask)
* [gunicorn](https://gunicorn.org/) - WSGI HTTP Server for running web app locally and on production (Heroku i.e)
* [MarkupSafe](https://pypi.org/project/MarkupSafe/) - Character escaping for safe HTML and XML (comes with Flask)
* [itsdangerous](https://itsdangerous.palletsprojects.com/en/1.1.x/) - data decode and encode (comes with Flask)
* [Werkzeug](https://palletsprojects.com/p/werkzeug/) - yet another wsgi lib (comes with Flask)

## Authors

* **Sakari Pöyhiä** 
