#!/bin/sh

# Apply migrations
python manage.py migrate
# Continue
exec "$@"