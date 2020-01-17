# Asset Management Application for Parish of the Lord of Divine Mercy

This is the backend application for the Asset Management 

## Prerequisite

* Python v3.xx
* MSSQL installed
* nodemon (NodeJS app for development)

## Pre-Install Instructions

* Craete a virtual phython evnironment `virtualenv penv`
* run the pip install `pip install -r requirements.txt`
* run `flask run` to run server

## Configuration

* if you are configuring as a developer set the flask env to development `export FLASK_ENV=development`
* rename the `internals/config.sample.py` to `internals/config.py` and adjust the database configuration

## Migration

Migration is a tool to help manage the changes in the database. It is similar to git that changes needs to be commited (i.e: migrate) and pushed (i.e: upgrade/downgrade) for changes to reflect on the server

### How it Works

Change the declared table properties in the models folder files.

In the terminal for changing
* `flask db migrate -m "describe the changes done in the db"`
* `flask db upgrate`

### Seeders

Setup initial data to make the program workable for the first time. see `seeders.py`

In the terminal
* `python seeders.py` in the root directory of the project

