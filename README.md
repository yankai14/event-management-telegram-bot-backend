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
Run tests
```bash
python manage.py test
```
Start server
```bash
python manage.py runserver
```


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


## API Endpoints

Download and install Postman GUI [here](https://www.postman.com/).
