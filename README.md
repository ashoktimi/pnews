# The News App
## Pnews site: 
[Pnews](https://web-production-2c27.up.railway.app/)

# API Integration:
This project using a [News API](https://newsapi.org/docs) is a HTTP REST API for searching and retrieving live articles from all over the web.

## Technology Stack:
- Frontend: HTML, CSS, jQuery, ES6, Vanilla JavaScript, Bootstrap
- Backend: Python, Flask, SQLAlchemy, Postgres
- Libraries & modules: WTForms, Bcrypt, requests, unittest
- Templating  engine: jinja2

## Features
- User registration
- User login and logout
- News browsing for non-logged in users
- Searching for the latest news by keyword and filtering by relevancy, popularity and published date
- News for different categories
- News sources
- Adding news to favorites for logged in users
- Searching for the latest news by keyword and date for logged in users

## Getting Started
- Clone the repository: git clone https://github.com/ashoktimi/capstone1.git
- Change into the project directory: cd capstone1
- Create a virtual environment: python -m venv venv
- Activate the virtual environment: source venv/bin/activate
- Install the required packages: pip install -r requirements.txt
- Set the environment variables:

    export FLASK_APP=app
    export FLASK_ENV=development
    
- Create the database: flask db upgrade
- Run the app: flask run
- Visit the app in your browser at http://localhost:5000
