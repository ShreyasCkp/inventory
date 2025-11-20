#!/bin/bash
set -e
apt-get update
apt-get install -y libcairo2 libpango-1.0-0 libgdk-pixbuf2.0-0 libgobject-2.0-0 shared-mime-info fonts-liberation
# start gunicorn
exec gunicorn LG.wsgi:application --bind 0.0.0.0:8000 --workers 3
