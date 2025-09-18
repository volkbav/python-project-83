### Hexlet tests and linter status:
[![Actions Status](https://github.com/volkbav/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/volkbav/python-project-83/actions) [![Test page analizer](https://github.com/volkbav/python-project-83/actions/workflows/my_tests.yml/badge.svg)](https://github.com/volkbav/python-project-83/actions/workflows/my_tests.yml)


# About project
This is a learning project. Completed as part of the python developer course

## demo
To view demo [click here](https://python-project-83-i5ma.onrender.com)

## Technologies Used
[gunicorn](https://docs.gunicorn.org/en/latest/index.html) - Python WSGI HTTP Server for UNIX

[uv](https://github.com/astral-sh/uv) - Python package and project manager

[Flask](https://flask.palletsprojects.com/en/stable/) - Lightweight WSGI web application framework

[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) -  Python library for pulling data out of HTML and XML files

[library os](https://docs.python.org/3/library/os.html) - Miscellaneous operating system interfaces

[library requests](https://requests.readthedocs.io/en/latest/) - Simple HTTP library for Python

[library dotenv](https://pypi.org/project/python-dotenv/) - Reads key-value pairs from a .env file and can set them as environment variables

[module urllib.parse](https://docs.python.org/3/library/urllib.parse.html) - Parse URLs into components

# Installation
For work you need make next step
## 1. Install Python
macOs
```
brew install python3
```
linux (ubuntu)
```
sudo apt install python3
```
## 2. Install uv
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```
If you did not have `curl`:
```
wget -qO- https://astral.sh/uv/install.sh | sh
```
macOs
```
brew install uv
```
linux (ubuntu)
```
brew install uv
```
## 3. Clone repository
```
git clone https://github.com/volkbav/python-project-83.git
```
## 4. Install programm
```
make install
```
# Run project
```
make start
```
To view web interface go to adress in brouser
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)