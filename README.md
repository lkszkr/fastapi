# FastAPI API

## Description

FastAPI-based API allows users to create and manage charitable fundraising campaigns.



## Features

- ORM
- PostreSQL database
- Tests
- JWT auth 

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [API Documentation](#api-documentation)
- [Tests](#tests)

## Requirements

- Python 3.11.6
- PstgreSQL

## Installation

1. **Create a virtual environment:**
python -m venv venv
2. **Activate the virtual environment**
venv/Scripts/Activate.ps1
3. **Install the dependencies**
pip install -r requirements.txt

## Configuration
Create .env file in root dicectory with this fields to connect to database:
- DATABASE_HOSTNAME=your_database_hostname (ex. localhost)
- DATABASE_PORT=port_your_database_run_on
- DATABASE_PASSWORD=password_for_accesing_database
- DATABASE_NAME=name_of_your_database
- DATABASE_USERNAME=name_of_database_username
- SECRET_KEY=secret_key_for_token_verification (ex. 09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7)
- ALGORITHM=algorith_for_JWT
- ACCESS_TOKEN_EXPIRE_MINUTES=token_time

## Usage
**Running Aplication**
uvicorn app.main:app --reload or uvicorn app.main:app 
Reload flags enables hot reload but use much more resources
**Api Documentation**
host:8000/docs or host:8000/redoc

## Tests
**Running tests**
pytest -v -s