# Prerequisites

List of things you need to have before you start using the project:

- Docker
- Docker Compose
- Python 3.12
- Node 20
- Postgres 16

# Getting started

Two ways of doing it:

## Option 1: Docker

Simply run the following command at the root of the project:

```bash
docker compose up --build -d
```

Go to the [website](localhost:5173).

## Option 2: Manually

### Python environment

Go to ./dynameat-api and run:

```bash
python -m venv venv
pip install -r requirements
```

In `./dynameat-api/src/core/settings.py`, change the following lines with your postgres info:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'asteroid-db',
        'PORT': '5432',
    }
}
```

Run all the migrations:

```bash
python src/manage.py migrate
```

And start the server:

```bash
python src/manage.py runserver 0.0.0.0:8000
```

### Node environment

Go to `./dynameat-spa` and run:

```bash
npm i
```

Create inside a `.env` file with the following content:

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000/api/
```

And start the server:

```bash
npm run dev
```

Go to the [website](localhost:5173).
