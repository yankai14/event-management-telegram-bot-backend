# Event Management Telegram Bot Backend

Backend API for the event management telegram bot project. Build using Django and Postgresql.

## Installation

Follow the below instructions:

To install dependencies

```bash
pip install -r requirements.txt
```

Run postgresql service on localhost

```bash
sudo service postgresql start
```

Create your .env file and fill in according to stub.env

Make migrations and migrate databases
```bash
python manage.py makemigrations lms
python manage.py migrate
```
Run tests
```bash
python manage.py test
```
Start server
```bash
python manage.py runserver
```

## API Endpoints

Download and install Postman GUI [here](https://www.postman.com/).