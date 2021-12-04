# Event Management Telegram Bot Backend

Backend API for the event management telegram bot project. Build using Django and Postgresql.

## Installation

Follow the below instructions:

To install dependencies


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
Start server
```bash
python manage.py runserver
```

## Run tests

Generate a coverage report
```bash
coverage run --omit='*/venv/*' manage.py test
```

Read coverage report
```bash
coverage report
```

To get a UI coverage report for better analysis,
1. Install Live Server on VS Code (Optional)
2.  Run the command below in your terminal, the folder htmlcov should be generated
```bash
coverage html
```
3. Search for the folder index.html and open it on liveshare or on your file explorercoverage run --omit='*/venv/*' manage.py test


## Docker + Docker compose
Install [docker](https://docs.docker.com/engine/install/ubuntu/) and [docker-compose](https://docs.docker.com/compose/install/) using the official docs given.

Remember to start docker service after installing .docker
```bash
sudo dockerd
```

Build docker image
```bash
sudo docker-compose build
```

In your .env file, the variable POSTGRES_HOST should be of this value POSTGRES_HOST = db.

Run the below commands to make migrations and migrate db
```bash
python3 manage.py makemigrations lms
sudo docker-compose run web python manage.py migrate
```

Run docker image
```bash
sudo docker-compose up
```

To start stripe webhook
./stripe listen --forward-to http://127.0.0.1:8000/event-payment/webhook

## API Endpoints

Download and install Postman GUI [here](https://www.postman.com/).

Download and install Stripe CLI [here](https://stripe.com/docs/stripe-cli)
