#!/bin/bash

echo "Apply database migrations"
python src/manage.py migrate --noinput

echo "Starting server"
python src/manage.py runserver 0.0.0.0:8000

