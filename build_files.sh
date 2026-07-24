#!/bin/bash
python -m pip install --upgrade pip --break-system-packages
python -m pip install -r requirements.txt --break-system-packages
python manage.py collectstatic --noinput --ignore=*.pyc || true
