# Transaction Analysis API 
This project is a microservice for financial transaction analysis. It is built using FastAPI, PostgreSQL, SQLAlchemy, Celery, and Redis.
## Features
- API for analyzing financial transactions.
- Background task processing with Celery.
- Caching with Redis for improved performance.
- API documentation available at `/docs`.

## Running the Project Locally
## Requirements

- Python 3.10+
- PostgreSQL 13.11
- redis-server 5.0.7
- celery 5.4.0
1. Clone the Repository
```shell
git clone https://github.com/ravverano/TestWork734.git
cd TestWork734
```
2. create a python environment using python-venv and install needed libraries.
```shell
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
3. Request for the Environment Variables (.env) from Admin: You will need to obtain the required environment variables for the application to function properly (such as PostgreSQL and Redis credentials)
4. run the app and open in your browser http://localhost:5080/docs to test if running.
```shell
uvicorn app:app --reload --port=5080 --host=0.0.0.0
```
5. run celery (make sure redis-server is running)
```shell
celery -A workers.celery_worker worker --loglevel=info
```

## Running the Project using Docker
## Requirements

- Docker
- Docker Compose

1. Clone the Repository
```shell
git clone https://github.com/ravverano/TestWork734.git
cd TestWork734
```
2. Request for the Environment Variables (.env) from Admin: You will need to obtain the required environment variables for the application to function properly (such as PostgreSQL and Redis credentials)
3. change environment variable PSQL_HOST to "postgres", REDIS_HOST to 'redis'
4. execute docker compose command
```shell
docker-compose up --build
```
5. Open in your browser http://localhost:5080/docs to test if all is running.
6. To stop all running containers, you can use
```shell
docker-compose down
```
